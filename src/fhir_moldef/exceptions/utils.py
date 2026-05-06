# Allele Utils


class InvalidVRSAlleleError(Exception):
    """Raised when the expression is not a valid VRS Allele."""


class InvalidAlleleProfileError(Exception):
    """Raised when the expression is not a valid FHIR Allele."""


class InvalidSequenceTypeError(Exception):
    """Raised when the RefSeq identifier has an unrecognized prefix."""


class InvalidAccessionError(Exception):
    """Raised when the provided RefSeq ID does not match the expected format."""


class InvalidCoordinateSystemError(Exception):
    """Raised when an invalid coordinate system is specified."""
