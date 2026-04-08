import re

from exceptions.utils import (
    InvalidAccessionError,
    InvalidSequenceTypeError,
)


def refseq_to_fhir_id(refseq_accession):
    """Convert a RefSeq accession to a FHIR-compatible ID.

    Args:
        refseq_accession (str): A RefSeq accession string (e.g., 'NM_001200.3').

    Returns:
        str: A normalized FHIR-compatible ID (e.g., 'nm001200').
    """
    return refseq_accession.split(".", 1)[0].replace("_", "").lower()


def detect_sequence_type(sequence_id: str) -> str:
    """Translate the prefix of the RefSeq identifier to the type of sequence.

    Args:
        sequence_id (str): The RefSeq identifier.

    Raises:
        ValueError: If the prefix doesn't match any known sequence type.

    Returns:
        str: The type of sequence

    """
    prefix_to_type = {
        "NC_": "DNA",
        "NG_": "DNA",
        "NW_": "DNA",
        "NT_": "DNA",
        "NM_": "RNA",
        "NR_": "RNA",
        "NP_": "protein",
    }

    for prefix, seq_type in prefix_to_type.items():
        if sequence_id.startswith(prefix):
            return seq_type

    raise InvalidSequenceTypeError(f"Unknown sequence type for input: {sequence_id}")


def validate_accession(refseq_id: str) -> str:
    """Validate the given RefSeq ID to ensure it matches the expected format.

    Args:
        refseq_id (str): The RefSeq ID to be validated.

    Raises:
        ValueError: If the RefSeq ID does not match the expected format.

    Returns:
        str: The validated RefSeq ID.
    """
    refseq_pattern = re.compile(r"^(NC_|NG_|NM_|NR_|NP_)\d+\.\d+$")

    if not refseq_pattern.match(refseq_id):
        raise InvalidAccessionError(
            f"Invalid accession number: {refseq_id}. Must be a valid NCBI RefSeq ID (e.g., NM_000769.4)."
        )

    return refseq_id


def translate_sequence_id(dp, expression):
    """Translate a sequence ID using SeqRepo and return the RefSeq ID.

    Args:
        dp (SeqRepo DataProxy): The data proxy used to translate the sequence.
        expression: An object containing sequence location info.

    Raises:
        ValueError: If translation fails or if format is unexpected.

    Returns:
        str: A valid RefSeq identifier (e.g., NM_000123.3).
    """
    sequence = f"ga4gh:{expression.location.get_refget_accession()}"
    translated_ids = dp.translate_sequence_identifier(sequence, namespace="refseq")
    if not translated_ids:
        raise ValueError(f"No RefSeq ID found for sequence ID '{sequence}'.")

    translated_id = translated_ids[0]
    if not translated_id.startswith("refseq:"):
        raise ValueError(f"Unexpected ID format in '{translated_id}'")

    _, refseq_id = translated_id.split(":")
    return refseq_id
