from copy import deepcopy

import pytest
from fhir.resources.reference import Reference

from exceptions.fhir import (
    # MissingFocusCodingSystem,
    InvalidFocusCodingDisplay,
    InvalidMoleculeTypeError,
    MemberStateNotAllowedError,
    MissingAlternativeState,
    MissingFocus,
    MissingFocusCoding,
    MissingFocusCodingCode,
    MissingReferenceState,
    MissingRepresentation,
    MultipleContextState,
    MultipleLocation,
)
from profiles.variation import Variation as FhirVariation


@pytest.fixture
def valid_fhir_variation():
    return {
        "resourceType": "MolecularDefinition",
        "moleculeType": {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecule-type",
                    "code": "dna",
                    "display": "DNA Sequence",
                }
            ]
        },
        "location": [
            {
                "sequenceLocation": {
                    "sequenceContext": {
                        "reference": "#ref-to-nc000019",
                        "type": "MolecularDefinition",
                        "display": "NC_000019.10",
                    },
                    "coordinateInterval": {
                        "coordinateSystem": {
                            "system": {
                                "coding": [
                                    {
                                        "system": "http://loinc.org",
                                        "code": "LA30100-4",
                                        "display": "0-based interval counting",
                                    }
                                ]
                            },
                            "origin": {
                                "coding": [
                                    {
                                        "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
                                        "code": "sequence-start",
                                        "display": "Sequence start",
                                    }
                                ]
                            },
                            "normalizationMethod": {
                                "coding": [
                                    {
                                        "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
                                        "code": "fully-justified",
                                        "display": "Fully justified",
                                    }
                                ]
                            },
                        },
                        "startQuantity": {"value": 44908821.0},
                        "endQuantity": {"value": 44908822.0},
                    },
                }
            }
        ],
        "representation": [
            {
                "focus": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus",
                            "code": "reference-state",
                            "display": "Reference State",
                        }
                    ]
                },
                "literal": {"value": "C"},
            },
            {
                "focus": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus",
                            "code": "alternative-state",
                            "display": "Alternative State",
                        }
                    ]
                },
                "literal": {"value": "T"},
            },
        ],
    }


def assert_raises_message(exception_type, msg, fn, *args, **kwargs):
    with pytest.raises(exception_type) as exception_info:
        fn(*args, **kwargs)
    assert str(exception_info.value) == msg


def test_member_state_not_allowed(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)
    data["memberState"] = Reference(display="test")
    assert_raises_message(
        MemberStateNotAllowedError,
        "`memberState` is not allowed in Variation.",
        FhirVariation,
        **data,
    )


@pytest.mark.parametrize("molType", [None, {}])
def test_present_of_molecularType(valid_fhir_variation, molType):
    data = deepcopy(valid_fhir_variation)
    data["moleculeType"] = molType
    assert_raises_message(
        InvalidMoleculeTypeError,
        "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Variation.",
        FhirVariation,
        **data,
    )


@pytest.mark.parametrize("loc", [None, []])
def test_location_cardinality(valid_fhir_variation, loc):
    data = deepcopy(valid_fhir_variation)
    data["location"] = loc
    assert_raises_message(
        MultipleLocation,
        "The `location` field must contain exactly one item. `location` has a 1..1 cardinality for Variation.",
        FhirVariation,
        **data,
    )


@pytest.mark.parametrize("rep", [None, []])
def test_missing_representation(valid_fhir_variation, rep):
    data = deepcopy(valid_fhir_variation)
    if rep is None:
        data.pop("representation", None)
    else:
        data["representation"] = rep
    assert_raises_message(
        MissingRepresentation,
        "The `representation` field must contain one or more items. `representation` has a 1..* cardinality for Variation.",
        FhirVariation,
        **data,
    )


def test_missing_focus_in_representation(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)
    data["representation"][0].pop("focus")
    assert_raises_message(
        MissingFocus,
        "representation[0].focus is required when slicing by focus CodeableConcept.",
        FhirVariation,
        **data,
    )


def test_missing_focus_coding_list(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)
    data["representation"][0]["focus"]["coding"] = []
    assert_raises_message(
        MissingFocusCoding,
        "representation[0].focus.coding must contain at least one entry.",
        FhirVariation,
        **data,
    )


def test_missing_coding_code(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)
    data["representation"][0]["focus"]["coding"][0].pop("code")
    assert_raises_message(
        MissingFocusCodingCode,
        "representation[0].focus.coding is missing a 'code' element.",
        FhirVariation,
        **data,
    )


def test_invalid_display_for_reference_state(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)

    for rep in data["representation"]:
        for coding in rep["focus"]["coding"]:
            if coding["code"] == "reference-state":
                coding["display"] = "Test-Incorrect-Display"
                break

    assert_raises_message(
        InvalidFocusCodingDisplay,
        "The Coding with code='reference-state' must have display='Reference State', found 'Test-Incorrect-Display'.",
        FhirVariation,
        **data,
    )


def test_invalid_display_for_alternative_state(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)

    for rep in data["representation"]:
        for coding in rep["focus"]["coding"]:
            if coding["code"] == "alternative-state":
                coding["display"] = "Test-Incorrect-Display"
                break

    assert_raises_message(
        InvalidFocusCodingDisplay,
        "The Coding with code='alternative-state' must have display='Alternative State', found 'Test-Incorrect-Display'.",
        FhirVariation,
        **data,
    )


def test_multiple_reference_state_globally(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)
    data["representation"].append(
        {
            "focus": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus",
                        "code": "reference-state",
                        "display": "Reference State",
                    }
                ]
            }
        }
    )

    assert_raises_message(
        MissingReferenceState,
        "Exactly one 'reference-state' must be present across 'representation' (cardinality 1..1).",
        FhirVariation,
        **data,
    )


def test_multiple_alternative_state_globally(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)
    data["representation"].append(
        {
            "focus": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus",
                        "code": "alternative-state",
                        "display": "Alternative State",
                    }
                ]
            }
        }
    )

    assert_raises_message(
        MissingAlternativeState,
        "Exactly one 'alternative-state' must be present across 'representation' (cardinality 1..1).",
        FhirVariation,
        **data,
    )


def test_multiple_context_state_globally(valid_fhir_variation):
    data = deepcopy(valid_fhir_variation)
    data["representation"].append(
        {
            "focus": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus",
                        "code": "context-state",
                        "display": "Context State",
                    }
                ]
            }
        }
    )
    data["representation"].append(
        {
            "focus": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus",
                        "code": "context-state",
                        "display": "Context State",
                    }
                ]
            }
        }
    )
    assert_raises_message(
        MultipleContextState,
        "At most one 'context-state' is allowed across 'representation' (cardinality 0..1).",
        FhirVariation,
        **data,
    )
