from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding


def _cc(system: str, code: str, display: str) -> CodeableConcept:
    return CodeableConcept(coding=[Coding(system=system, code=code, display=display)])


# ------------------------------------------------------------
# SYSTEMS
# ------------------------------------------------------------
ZERO_BASE_INTERVAL_SYSTEM = _cc(
    "http://loinc.org", "LA30100-4", "0-based interval counting"
)

ONE_BASE_INTERVAL_SYSTEM = _cc(
    "http://loinc.org", "LA30102-0", "1-based character counting"
)

# ------------------------------------------------------------
# ORIGINS
# ------------------------------------------------------------
SEQUENCE_START_ORIGIN = _cc(
    "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
    "sequence-start",
    "Sequence start",
)

FEATURE_START_ORIGIN = _cc(
    "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
    "feature-start",
    "Feature start",
)

# ------------------------------------------------------------
# NORMALIZATION METHODS
# ------------------------------------------------------------
FULLY_JUSTIFIED_NORMALIZATION = _cc(
    "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
    "fully-justified",
    "Fully justified",
)

RIGHT_SHIFT_NORMALIZATION = _cc(
    "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
    "right-shift",
    "Right shift",
)

# ------------------------------------------------------------
# METHODS
# ------------------------------------------------------------


def spdi_coordinate_interval():
    return (
        ZERO_BASE_INTERVAL_SYSTEM,
        SEQUENCE_START_ORIGIN,
        FULLY_JUSTIFIED_NORMALIZATION,
    )


def vrs_coordinate_interval():
    return (
        ZERO_BASE_INTERVAL_SYSTEM,
        SEQUENCE_START_ORIGIN,
        FULLY_JUSTIFIED_NORMALIZATION,
    )


def hgvs_coordinate_interval(molType):
    if molType == "DNA":
        return (
            ONE_BASE_INTERVAL_SYSTEM,
            FEATURE_START_ORIGIN,
            RIGHT_SHIFT_NORMALIZATION,
        )

    elif molType in ("RNA", "protein"):
        return (
            ONE_BASE_INTERVAL_SYSTEM,
            SEQUENCE_START_ORIGIN,
            RIGHT_SHIFT_NORMALIZATION,
        )

    else:
        raise ValueError(f"Unsupported molecular type: {molType}")
