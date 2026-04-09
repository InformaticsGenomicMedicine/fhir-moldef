import pytest
from deepdiff import DeepDiff
from pydantic import ValidationError

from resources.moleculardefinition import MolecularDefinition


@pytest.fixture
def example_molecular_definition():
    return {
        "resourceType": "MolecularDefinition",
        "id": "example-allele1",
        "meta": {"profile": ["http://hl7.org/fhir/StructureDefinition/allele"]},
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
                        "reference": "MolecularDefinition/example-sequence-lrg584",
                        "type": "MolecularDefinition",
                        "display": "Starting Sequence Resource: LRG_584",
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
                                ],
                                "text": "0-based interval counting",
                            }
                        },
                        "startQuantity": {"value": 5001},
                        "endQuantity": {"value": 97867},
                    },
                }
            }
        ],
        "representation": [
            # The extracted portion of this example was made up to make sure the new schema developed is functioning properly
            {
                "extracted": {
                    "startingMolecule": {"display": "test"},
                    "coordinateInterval": {
                        "coordinateSystem": {
                            "system": {
                                "coding": [
                                    {
                                        "system": "http://loinc.org",
                                        "code": "LA30100-4",
                                        "display": "0-based interval counting",
                                    }
                                ],
                                "text": "0-based interval counting",
                            }
                        },
                        "start": 5123,
                        "end": 5124,
                    },
                }
            },
            {
                "relative": {
                    "startingMolecule": {
                        "reference": "MolecularDefinition/example-sequence-lrg584",
                        "type": "MolecularDefinition",
                        "display": "Starting Sequence Resource: LRG_584",
                    },
                    "edit": [
                        {
                            "coordinateInterval": {
                                "coordinateSystem": {
                                    "system": {
                                        "coding": [
                                            {
                                                "system": "http://loinc.org",
                                                "code": "LA30100-4",
                                                "display": "0-based interval counting",
                                            }
                                        ],
                                        "text": "0-based interval counting",
                                    }
                                },
                                "start": 5123,
                                "end": 5124,
                            },
                            "replacementMolecule": {
                                "reference": "MolecularDefinition/example-sequence-t",
                                "type": "MolecularDefinition",
                                "display": "Replacement Sequence Resource: T",
                            },
                            "replacedMolecule": {
                                "reference": "MolecularDefinition/example-sequence-c",
                                "type": "MolecularDefinition",
                                "display": "Replaced Sequence Resource: C",
                            },
                        }
                    ],
                }
            },
        ],
    }


def test_molecular_definition_full_validation(example_molecular_definition):
    moldef = MolecularDefinition(**example_molecular_definition)
    model_dumped = moldef.model_dump()
    differences = DeepDiff(
        example_molecular_definition, model_dumped, ignore_order=True
    )

    assert differences == {}, f"Differences found: {differences}"


def impl_molecular_definition_1(moldef_instance):
    assert moldef_instance.id == "example-allele1"
    assert (
        moldef_instance.meta.profile[0]
        == "http://hl7.org/fhir/StructureDefinition/allele"
    )

    # moleculeType field checks
    molecule_type_coding = moldef_instance.moleculeType.coding[0]
    assert molecule_type_coding.system == "http://hl7.org/fhir/sequence-type"
    assert molecule_type_coding.code == "dna"
    assert molecule_type_coding.display == "DNA Sequence"

    # location field checks
    location = moldef_instance.location[0].sequenceLocation
    assert (
        location.sequenceContext.reference
        == "MolecularDefinition/example-sequence-lrg584"
    )
    assert location.sequenceContext.type == "MolecularDefinition"
    assert location.sequenceContext.display == "Starting Sequence Resource: LRG_584"

    # coordinateInterval field checks
    coordinate_interval = location.coordinateInterval
    assert (
        coordinate_interval.coordinateSystem.system.coding[0].system
        == "http://loinc.org"
    )
    assert coordinate_interval.coordinateSystem.system.coding[0].code == "LA30100-4"
    assert (
        coordinate_interval.coordinateSystem.system.coding[0].display
        == "0-based interval counting"
    )
    assert (
        coordinate_interval.coordinateSystem.system.text == "0-based interval counting"
    )
    assert coordinate_interval.startQuantity.value == 5001
    assert coordinate_interval.endQuantity.value == 97867

    # extracted field checks
    rep_extracted = moldef_instance.representation[0].extracted
    assert rep_extracted.startingMolecule.display == "test"
    assert (
        rep_extracted.coordinateInterval.coordinateSystem.system.coding[0].system
        == "http://loinc.org"
    )
    assert (
        rep_extracted.coordinateInterval.coordinateSystem.system.coding[0].code
        == "LA30100-4"
    )
    assert (
        rep_extracted.coordinateInterval.coordinateSystem.system.coding[0].display
        == "0-based interval counting"
    )
    assert (
        rep_extracted.coordinateInterval.coordinateSystem.system.text
        == "0-based interval counting"
    )
    assert rep_extracted.coordinateInterval.start == 5123
    assert rep_extracted.coordinateInterval.end == 5124

    # releative field checks
    rep_relative = moldef_instance.representation[1].relative
    assert (
        rep_relative.startingMolecule.reference
        == "MolecularDefinition/example-sequence-lrg584"
    )
    assert rep_relative.startingMolecule.type == "MolecularDefinition"
    assert (
        rep_relative.startingMolecule.display == "Starting Sequence Resource: LRG_584"
    )

    # edit field checks
    edit = rep_relative.edit[0]
    assert (
        edit.coordinateInterval.coordinateSystem.system.coding[0].system
        == "http://loinc.org"
    )
    assert edit.coordinateInterval.coordinateSystem.system.coding[0].code == "LA30100-4"
    assert (
        edit.coordinateInterval.coordinateSystem.system.coding[0].display
        == "0-based interval counting"
    )
    assert (
        edit.coordinateInterval.coordinateSystem.system.text
        == "0-based interval counting"
    )
    assert edit.coordinateInterval.start == 5123
    assert edit.coordinateInterval.end == 5124
    assert (
        edit.replacementMolecule.reference == "MolecularDefinition/example-sequence-t"
    )
    assert edit.replacementMolecule.type == "MolecularDefinition"
    assert edit.replacementMolecule.display == "Replacement Sequence Resource: T"
    assert edit.replacedMolecule.reference == "MolecularDefinition/example-sequence-c"
    assert edit.replacedMolecule.type == "MolecularDefinition"
    assert edit.replacedMolecule.display == "Replaced Sequence Resource: C"


def test_molecular_definition(example_molecular_definition):
    moldef = MolecularDefinition(**example_molecular_definition)
    impl_molecular_definition_1(moldef)


def test_molecular_definition_missing_sequence_context(example_molecular_definition):
    # Create invalid data by removing the required `sequenceContext` field: sequenceContext has a cardinality of 1..1.
    invalid_data = example_molecular_definition.copy()
    del invalid_data["location"][0]["sequenceLocation"]["sequenceContext"]

    with pytest.raises(ValidationError):
        MolecularDefinition(**invalid_data)
