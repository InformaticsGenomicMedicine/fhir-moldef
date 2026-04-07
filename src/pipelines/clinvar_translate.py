import argparse
import gzip
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import orjson
from ga4gh.vrs.models import Allele

from translators.vrs_to_fhir_allele import VrsToFhirAlleleTranslator


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
        self, inputfile, outputfile, invalid_allele_path, invalid_fhir_path, limit=None
    ):
        started_at_wall = datetime.now()
        t0 = time.perf_counter()

        invalid_allele_log = open(invalid_allele_path, "ab")
        invalid_fhir_trans_log = open(invalid_fhir_path, "ab")
        stats = open("runtime_stats.txt", "wb")

        total_translated = 0
        failed_vrs_allele_validation = 0
        failed_vrs_to_fhir_translation = 0
        total_lines_read = 0
        vrs_allele_seen = 0
        allele_type = {"lse_count": 0, "rle_count": 0, "other_count": 0}

        try:
            with open(outputfile, "ab") as out_f:
                with gzip.open(inputfile, "rt", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if limit is not None and line_num > limit:
                            break

                        total_lines_read += 1

                        try:
                            obj = orjson.loads(line)
                            members = obj.get("members", [])
                        except orjson.JSONDecodeError:
                            logging.warning(
                                "[Line %d] Skipping: JSON decode error", line_num
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

                                invalid_allele = {
                                    "line": line_num,
                                    "error": str(e),
                                    "member": member,
                                }
                                invalid_allele_log.write(
                                    orjson.dumps(invalid_allele) + b"\n"
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
                                fhir_obj = self.vrs_translator.translate(
                                    vo
                                )

                                valid_translation = {
                                    "line": line_num,
                                    "vrs_allele": vo.model_dump(exclude_none=True),
                                    "fhir_allele": fhir_obj.model_dump(
                                        exclude_none=True
                                    ),
                                }
                                total_translated += 1
                                out_f.write(orjson.dumps(valid_translation) + b"\n")

                            except Exception as e:
                                failed_vrs_to_fhir_translation += 1

                                invalid_translation = {
                                    "line": line_num,
                                    "error": str(e),
                                    "vrs_allele": vo.model_dump(exclude_none=True),
                                }
                                invalid_fhir_trans_log.write(
                                    orjson.dumps(invalid_translation) + b"\n"
                                )
        finally:
            t1 = time.perf_counter()
            ended_at_wall = datetime.now()
            duration = max(t1 - t0, 1e-9)

            final_stats = ClinvarTranslationSummary(
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

            stats.write(orjson.dumps(final_stats, option=orjson.OPT_INDENT_2) + b"\n")
            stats.close()

            invalid_allele_log.close()
            invalid_fhir_trans_log.close()

    def main(self):
        parser = argparse.ArgumentParser(
            prog="allele-to-fhir-translator",
            description="Load a dataset and translate allele expressions (tabular) or VRS 'out' objects (jsonl) to FHIR",
        )
        parser.add_argument("input_gzip", help="Path to gzipped JSONL file")
        parser.add_argument("--invalid-allele-log", default="invalid_vrs_alleles.jsonl")
        parser.add_argument("--invalid-fhir-log", default="invalid_trans_to_fhir.jsonl")
        parser.add_argument(
            "--limit", type=int, help="Process only this many lines from input"
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Enable detailed logging"
        )

        args = parser.parse_args()

        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
        logging.info("Starting Translation Job")

        self.run(
            inputfile=args.input_gzip,
            outputfile="vrs_to_fhir_translations.jsonl",
            invalid_allele_path=args.invalid_allele_log,
            invalid_fhir_path=args.invalid_fhir_log,
            limit=args.limit,
        )


if __name__ == "__main__":
    ClinvarTranslationPipeline().main()
