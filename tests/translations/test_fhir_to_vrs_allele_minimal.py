import pytest

from profiles.allele import Allele as FhirAllele
from translators.minimal_allele import MinimalFhirAlleleToVrsAlleleTranslator


@pytest.fixture
def example():
    return {
        "resourceType": "MolecularDefinition",
        "contained": [
            {
                "resourceType": "MolecularDefinition",
                "moleculeType": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sequence-type",
                            "code": "dna",
                            "display": "DNA Sequence",
                        }
                    ]
                },
                "representation": [
                    {
                        "code": [
                            {
                                "coding": [
                                    {
                                        "system": "http://www.ncbi.nlm.nih.gov/refseq",
                                        "code": "NC_000002.12",
                                    }
                                ]
                            }
                        ]
                    }
                ],
            }
        ],
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
                        "reference": "MolecularDefinition/example-sequence-nc000002-url",
                        "type": "MolecularDefinition",
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
                            }
                        },
                        "startQuantity": {"value": 27453448},
                        "endQuantity": {"value": 27453449},
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
                "literal": {"value": "T"},
            }
        ],
    }


@pytest.fixture
def allele_translator():
    return MinimalFhirAlleleToVrsAlleleTranslator()


@pytest.fixture
def allele_profile(example):
    return FhirAllele(**example)


@pytest.fixture
def vrs_expected_outputs():
    return {
        True: {
            "id": "ga4gh:VA.xfKU4c8mG_yegL5ZOL26JDiznySNkoMl",
            "type": "Allele",
            "digest": "xfKU4c8mG_yegL5ZOL26JDiznySNkoMl",
            "location": {
                "id": "ga4gh:SL.y0ckc1_lhMYKnh0f6FAEoEpgHyfX13OW",
                "type": "SequenceLocation",
                "digest": "y0ckc1_lhMYKnh0f6FAEoEpgHyfX13OW",
                "sequenceReference": {
                    "type": "SequenceReference",
                    "refgetAccession": "SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g",
                },
                "start": 27453448,
                "end": 27453449,
            },
            "state": {"type": "LiteralSequenceExpression", "sequence": "T"},
        },
        False: {
            "type": "Allele",
            "location": {
                "type": "SequenceLocation",
                "sequenceReference": {
                    "type": "SequenceReference",
                    "refgetAccession": "SQ.pnAqCRBrTsUoBghSD1yp_jXWSmlbdh4g",
                },
                "start": 27453448,
                "end": 27453449,
            },
            "state": {"type": "LiteralSequenceExpression", "sequence": "T"},
        },
    }


@pytest.mark.parametrize("normalize", [True, False])
def test_translate_allele_profile(
    allele_translator, allele_profile, vrs_expected_outputs, normalize
):
    output_dict = allele_translator.translate(
        allele_profile, normalize=normalize
    ).model_dump(exclude_none=True)

    assert output_dict == vrs_expected_outputs[normalize]