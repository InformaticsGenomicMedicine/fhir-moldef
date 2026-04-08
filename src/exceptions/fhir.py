class FHIRException(Exception):
    """Base exception for FHIR-related errors."""


class ElementNotAllowedError(FHIRException):
    """Raised when a certain field is disallowed in a profile."""


class MemberStateNotAllowedError(FHIRException):
    """Raised when 'memberState' is set in Allele but should not be."""


class InvalidMoleculeTypeError(FHIRException):
    """Raised when 'moleculeType' does not meet its 1..1 cardinality requirement."""


class InvalidTypeError(FHIRException):
    """Raised when 'type' does not meet its 1..1 cardinality requirement."""


####################### Location #############################################
class LocationError(FHIRException):
    """Base class for 'Location' validation errors."""


class MultipleLocation(LocationError):
    """Raised when 'location' does not meet its 1..1 cardinality requirement."""


####################### Representation ########################################
class RepresentationError(FHIRException):
    """Base class for 'representation' validation errors."""


class MissingRepresentation(RepresentationError):
    """Raised when 'representation' is missing (cardinality 1..*)."""


class MissingAlleleState(RepresentationError):
    """Raised when no 'allele-state' is present in 'representation' (cardinality 1..1)."""


class MultipleContextState(RepresentationError):
    """Raised when more than one 'context-state' is present in 'representation' (cardinality 0..1)."""


class MissingReferenceState(RepresentationError):
    """Raised when no 'reference-state' is present in 'representation' (cardinality 1..1)."""


class MissingAlternativeState(RepresentationError):
    """Raised when no 'alternative-state' is present in 'representation' (cardinality 1..1)."""


####################### FOCUS #############################################
class FocusError(FHIRException):
    """Base class for representation.focus-related validation errors."""


class MissingFocus(FocusError):
    """Raised when 'representation.focus' is missing (cardinality 1..1)."""


class MissingFocusCoding(FocusError):
    """Raised when 'focus.coding' is missing or improperly defined in representation."""


class MissingFocusCodingCode(FocusError):
    """Raised when 'focus.coding.code' is missing (cardinality 1..1)."""


class MissingFocusCodingSystem(FocusError):
    """Raised when 'focus.coding.system' is missing (cardinality 1..1)."""


class InvalidFocusCodingSystem(FocusError):
    """Raised when 'focus.coding.system' does not match its fixed value."""


class InvalidFocusCodingDisplay(FocusError):
    """Raised when 'focus.coding.display' does not match its fixed value."""
