import argparse
import dataclasses
import gzip
import logging
import time
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import orjson
from ga4gh.vrs.models import Allele

from fhir_moldef.translators.vrs_to_fhir_allele import VrsToFhirAlleleTranslator

logger = logging.getLogger(__name__)


@dataclass
class ClinvarTranslationSummary:
    file_name: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    duration_seconds: float
    total_lines_read: int
    vrs_allele_seen: int
    vrs_allele_types: dict
    total_translated: int
    failed_vrs_allele_validation: int
    failed_vrs_to_fhir_translation: int
    total_failed: int


class ClinvarTranslationPipeline:
    def __init__(self):
        self.vrs_translator = VrsToFhirAlleleTranslator()

    def run(
        self,
        inputfile: str,
        outputfile: str,
        invalid_allele_path: str,
        invalid_fhir_path: str,
        stats_path: str,
        mode: str = "wb",
        limit: int | None = None,
    ) -> ClinvarTranslationSummary:
        
        started_at_wall = datetime.now()
        t0 = time.perf_counter()

        total_translated = 0
        failed_vrs_allele_validation = 0
        failed_vrs_to_fhir_translation = 0
        total_lines_read = 0
        vrs_allele_seen = 0
        allele_type = {"lse_count": 0, "rle_count": 0, "other_count": 0}

        with ExitStack() as stack:
            out_f = stack.enter_context(open(outputfile, mode))
            invalid_allele_log = stack.enter_context(open(invalid_allele_path, mode))
            invalid_fhir_trans_log = stack.enter_context(open(invalid_fhir_path, mode))

            try:
                with gzip.open(inputfile, "rt", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if limit is not None and line_num > limit:
                            break

                        total_lines_read += 1

                        try:
                            obj = orjson.loads(line)
                            members = obj.get("members", [])
                        except orjson.JSONDecodeError:
                            logger.warning(
                                "[Line %d] Skipping: JSON decode error. Raw: %.200s",
                                line_num,
                                line.strip(),
                            )
                            continue

                        for member in members:
                            if not (
                                isinstance(member, dict)
                                and member.get("type") == "Allele"
                            ):
                                continue

                            vrs_allele_seen += 1
                            try:
                                vo = Allele(**member)
                            except Exception as e:
                                failed_vrs_allele_validation += 1
                                invalid_allele_log.write(
                                    orjson.dumps(
                                        {
                                            "line": line_num,
                                            "error": str(e),
                                            "member": member,
                                        }
                                    )
                                    + b"\n"
                                )
                                logger.debug(
                                    "[Line %d] VRS allele validation failed: %s",
                                    line_num,
                                    e,
                                    exc_info=True,
                                )
                                continue

                            state_type = vo.state.type
                            if "LiteralSequenceExpression" in state_type:
                                allele_type["lse_count"] += 1
                            elif "ReferenceLengthExpression" in state_type:
                                allele_type["rle_count"] += 1
                            else:
                                allele_type["other_count"] += 1

                            try:
                                fhir_obj = self.vrs_translator.translate(vo)
                                out_f.write(
                                    orjson.dumps(
                                        {
                                            "line": line_num,
                                            "vrs_allele": vo.model_dump(
                                                exclude_none=True
                                            ),
                                            "fhir_allele": fhir_obj.model_dump(
                                                exclude_none=True
                                            ),
                                        }
                                    )
                                    + b"\n"
                                )
                                total_translated += 1

                            except Exception as e:
                                failed_vrs_to_fhir_translation += 1
                                invalid_fhir_trans_log.write(
                                    orjson.dumps(
                                        {
                                            "line": line_num,
                                            "error": str(e),
                                            "vrs_allele": vo.model_dump(
                                                exclude_none=True
                                            ),
                                        }
                                    )
                                    + b"\n"
                                )
                                logger.debug(
                                    "[Line %d] VRS→FHIR translation failed: %s",
                                    line_num,
                                    e,
                                    exc_info=True,
                                )

            finally:
                t1 = time.perf_counter()
                ended_at_wall = datetime.now()
                duration = max(t1 - t0, 1e-9)

                summary = ClinvarTranslationSummary(
                    file_name=Path(inputfile).name,
                    start_date=started_at_wall.date().isoformat(),
                    start_time=started_at_wall.time().isoformat(timespec="seconds"),
                    end_date=ended_at_wall.date().isoformat(),
                    end_time=ended_at_wall.time().isoformat(timespec="seconds"),
                    duration_seconds=round(duration, 2),
                    total_lines_read=total_lines_read,
                    vrs_allele_seen=vrs_allele_seen,
                    vrs_allele_types=allele_type,
                    total_translated=total_translated,
                    failed_vrs_allele_validation=failed_vrs_allele_validation,
                    failed_vrs_to_fhir_translation=failed_vrs_to_fhir_translation,
                    total_failed=failed_vrs_allele_validation
                    + failed_vrs_to_fhir_translation,
                )

                stats_bytes = orjson.dumps(
                    dataclasses.asdict(summary), option=orjson.OPT_INDENT_2
                )

                stats_path_obj = Path(stats_path)
                stats_path_obj.write_bytes(stats_bytes + b"\n")

                logger.info("Translation complete. Stats written to %s", stats_path)
                logger.info(
                    "Translated: %d | Failed validation: %d | Failed translation: %d",
                    total_translated,
                    failed_vrs_allele_validation,
                    failed_vrs_to_fhir_translation,
                )

        return summary

    def main(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )

        parser = argparse.ArgumentParser(
            prog="vrs-allele-to-fhir-translator",
            description="Translate ClinVar VRS alleles to FHIR MolecularDefinition allele profile.",
        )
        parser.add_argument("input_gzip", help="Path to gzipped JSONL input file")

        parser.add_argument(
            "--output",
            default="vrs_to_fhir_translations.jsonl",
            help="Path for translated output JSONL (default: vrs_to_fhir_translations.jsonl)",
        )
        parser.add_argument(
            "--stats-log",
            default="runtime_stats.json",
            help="Path for runtime stats JSON (default: runtime_stats.json)",
        )
        parser.add_argument(
            "--invalid-allele-log",
            default="invalid_vrs_alleles.jsonl",
            help="Path for invalid VRS allele log (default: invalid_vrs_alleles.jsonl)",
        )
        parser.add_argument(
            "--invalid-fhir-log",
            default="invalid_translation_to_fhir.jsonl",
            help="Path for failed FHIR translation log (default: invalid_trans_to_fhir.jsonl)",
        )
        parser.add_argument(
            "--append",
            action="store_true",
            help="Append to existing output files instead of overwriting them",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Process only this many lines (useful for testing)",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable DEBUG-level logging (includes full tracebacks)",
        )

        args = parser.parse_args()

        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        logger.info("Starting Translation Job | input=%s", args.input_gzip)

        self.run(
            inputfile=args.input_gzip,
            outputfile=args.output,
            invalid_allele_path=args.invalid_allele_log,
            invalid_fhir_path=args.invalid_fhir_log,
            stats_path=args.stats_log,
            mode="ab" if args.append else "wb",
            limit=args.limit,
        )


if __name__ == "__main__":
    ClinvarTranslationPipeline().main()
