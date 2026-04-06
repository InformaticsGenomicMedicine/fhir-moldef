from exceptions.utils import (
    InvalidAlleleProfileError,
    InvalidVRSAlleleError,
)
from profiles.allele import Allele as FhirAllele


def validate_vrs_allele(expression):
    """Validation step to ensure that the expression is a valid VRS Allele object.

    Args:
        expression (object): An object representing a VRS Allele.

    Raises:
        InvalidVRSAlleleError: If the expression is not a valid VRS Allele object.

    """
    valid_state_types = ["LiteralSequenceExpression", "ReferenceLengthExpression"]

    conditions = [
        (expression.type == "Allele", "The expression type must be 'Allele'."),
        (
            expression.location.type == "SequenceLocation",
            "The location type must be 'SequenceLocation'.",
        ),
        (
            expression.state.type in valid_state_types,
            "The state type must be 'LiteralSequenceExpression' or 'ReferenceLengthExpression'.",
        ),
    ]
    for condition, error_message in conditions:
        if not condition:
            raise InvalidVRSAlleleError(error_message)


def validate_allele_profile(expression: object):
    """Validates if the given expression is a valid Allele.

    Args:
        expression (object): The expression to validate.

    Raises:
        TypeError: If the expression is not an instance of Allele.

    """
    if not isinstance(expression, FhirAllele):
        raise InvalidAlleleProfileError(
            "Invalid expression type: expected an instance of Allele."
        )
