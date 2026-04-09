from copy import deepcopy

import pytest
from fhir.resources.reference import Reference

from exceptions.fhir import (
    # MissingFocusCodingSystem,
    InvalidFocusCodingDisplay,
    InvalidMoleculeTypeError,
    MemberStateNotAllowedError,
    MissingAlleleState,
    MissingFocus,
    MissingFocusCoding,
    MissingFocusCodingCode,
    MissingRepresentation,
    MultipleContextState,
    MultipleLocation,
)
from profiles.allele import Allele as FhirAllele


@pytest.fixture()
def valid_allele():
    return {
        "resourceType": "MolecularDefinition",
        "id": "example-allelesliced-cyp2c19-1016",
        "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/allelesliced"]},
        "moleculeType": {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/sequence-type",
                    "code": "dna",
                    "display": "DNA Sequence",
                }
            ]
        },
        "location": [
            {
                "sequenceLocation": {
                    "sequenceContext": {
                        "reference": "MolecularDefinition/example-sequence-nm0007694-url",
                        "type": "MolecularDefinition",
                        "display": "Starting Sequence Resource: (CYP2C19), mRNA, NM_000769.4",
                    },
                    "coordinateInterval": {
                        "coordinateSystem": {
                            "system": {
                                "coding": [
                                    {
                                        "system": "http://loinc.org",
                                        "code": "LA30102-0",
                                        "display": "1-based character counting",
                                    }
                                ],
                                "text": "1-based character counting",
                            }
                        },
                        "startQuantity": {"value": 1016},
                    },
                }
            }
        ],
        "representation": [
            {
                "focus": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/moleculardefinition-focus",
                            "code": "allele-state",
                            "display": "Allele State",
                        }
                    ]
                },
                "code": [
                    {
                        "coding": [
                            {
                                "system": "https://www.pharmvar.org",
                                "code": "*1",
                                "display": "*1",
                            }
                        ]
                    }
                ],
                "literal": {"value": "G"},
            },
            {
                "focus": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/moleculardefinition-focus",
                            "code": "context-state",
                            "display": "Context State",
                        }
                    ]
                },
                "literal": {"value": "A"},
            },
        ],
    }


def assert_raises_message(exception_type, msg, fn, *args, **kwargs):
    with pytest.raises(exception_type) as exception_info:
        fn(*args, **kwargs)
    assert str(exception_info.value) == msg


def test_member_state_not_allowed(valid_allele):
    data = deepcopy(valid_allele)
    data["memberState"] = Reference(display="test")
    assert_raises_message(
        MemberStateNotAllowedError,
        "`memberState` is not allowed in Allele.",
        FhirAllele,
        **data,
    )


@pytest.mark.parametrize("molType", [None, {}])
def test_present_of_molecularType(valid_allele, molType):
    data = deepcopy(valid_allele)
    data["moleculeType"] = molType
    assert_raises_message(
        InvalidMoleculeTypeError,
        "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Allele.",
        FhirAllele,
        **data,
    )


@pytest.mark.parametrize("loc", [None, []])
def test_location_cardinality(valid_allele, loc):
    data = deepcopy(valid_allele)
    data["location"] = loc
    assert_raises_message(
        MultipleLocation,
        "The `location` field must contain exactly one item. `location` has a 1..1 cardinality for Allele.",
        FhirAllele,
        **data,
    )


@pytest.mark.parametrize("rep", [None, []])
def test_missing_representation(valid_allele, rep):
    data = deepcopy(valid_allele)
    if rep is None:
        data.pop("representation", None)
    else:
        data["representation"] = rep
    assert_raises_message(
        MissingRepresentation,
        "The `representation` field must contain one or more items. `representation` has a 1..* cardinality for Allele.",
        FhirAllele,
        **data,
    )


def test_missing_focus_in_representation(valid_allele):
    data = deepcopy(valid_allele)
    data["representation"][0].pop("focus")
    assert_raises_message(
        MissingFocus,
        "representation[0].focus is required when slicing by focus CodeableConcept.",
        FhirAllele,
        **data,
    )


def test_missing_focus_coding_list(valid_allele):
    data = deepcopy(valid_allele)
    data["representation"][0]["focus"]["coding"] = []
    assert_raises_message(
        MissingFocusCoding,
        "representation[0].focus.coding must contain at least one entry.",
        FhirAllele,
        **data,
    )


def test_missing_coding_code(valid_allele):
    data = deepcopy(valid_allele)
    data["representation"][0]["focus"]["coding"][0].pop("code")
    assert_raises_message(
        MissingFocusCodingCode,
        "representation[0].focus.coding is missing a 'code' element.",
        FhirAllele,
        **data,
    )


# NOTE: not yet implemented, it is currently # in allele.py
# def test_allele_state_requires_system(valid_allele):
#     data = deepcopy(valid_allele)
#     data["representation"][0]["focus"]["coding"][0].pop("system")
#     assert_raises_message(
#         MissingFocusCodingSystem,
#         "representation[0].focus.coding (code='allele-state') must define 'system'.",
#         FhirAllele,
#         **data)


def test_invalid_display_for_allele_state(valid_allele):
    data = deepcopy(valid_allele)

    for rep in data["representation"]:
        for coding in rep["focus"]["coding"]:
            if coding["code"] == "allele-state":
                coding["display"] = "Test-Incorrect-Display"
                break

    assert_raises_message(
        InvalidFocusCodingDisplay,
        "The Coding with code='allele-state' must have display='Allele State', found 'Test-Incorrect-Display'.",
        FhirAllele,
        **data,
    )


def test_invalid_display_for_context_state(valid_allele):
    data = deepcopy(valid_allele)

    for rep in data["representation"]:
        for coding in rep["focus"]["coding"]:
            if coding["code"] == "context-state":
                coding["display"] = "Test-Incorrect-Display"
                break

    assert_raises_message(
        InvalidFocusCodingDisplay,
        "The Coding with code='context-state' must have display='Context State', found 'Test-Incorrect-Display'.",
        FhirAllele,
        **data,
    )


def test_multiple_allele_state_globally(valid_allele):
    data = deepcopy(valid_allele)
    data["representation"].append(
        {
            "focus": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus",
                        "code": "allele-state",
                        "display": "Allele State",
                    }
                ]
            }
        }
    )
    assert_raises_message(
        MissingAlleleState,
        "Exactly one 'allele-state' must be present across 'representation' (cardinality 1..1).",
        FhirAllele,
        **data,
    )


def test_multiple_context_state_globally(valid_allele):
    data = deepcopy(valid_allele)
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
        FhirAllele,
        **data,
    )
