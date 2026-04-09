from copy import deepcopy

import pytest
from fhir.resources.reference import Reference

from exceptions.fhir import ElementNotAllowedError, InvalidMoleculeTypeError
from profiles.sequence import Sequence as FhirSequence


@pytest.fixture
def valid_sequence():
    return {
        "resourceType": "MolecularDefinition",
        "id": "example-sequence-c",
        "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/sequence"]},
        "moleculeType": {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/sequence-type",
                    "code": "dna",
                    "display": "DNA Sequence",
                }
            ]
        },
        "representation": [{"literal": {"value": "C"}}],
    }


def assert_raises_message(exception_type, msg, fn, *args, **kwargs):
    with pytest.raises(exception_type) as exception_info:
        fn(*args, **kwargs)
    assert str(exception_info.value) == msg


def test_member_state_not_allowed(valid_sequence):
    data = deepcopy(valid_sequence)
    data["memberState"] = Reference(display="Test")
    assert_raises_message(
        ElementNotAllowedError,
        "`memberState` is not allowed in Sequence.",
        FhirSequence,
        **data,
    )


def test_location_not_allowed(valid_sequence):
    data = deepcopy(valid_sequence)
    data["location"] = []
    assert_raises_message(
        ElementNotAllowedError,
        "`location` is not allowed in Sequence.",
        FhirSequence,
        **data,
    )


@pytest.mark.parametrize("molType", [None, {}])
def test_present_of_molecularType(valid_sequence, molType):
    data = deepcopy(valid_sequence)
    data["moleculeType"] = molType
    assert_raises_message(
        InvalidMoleculeTypeError,
        "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Allele.",
        FhirSequence,
        **data,
    )
