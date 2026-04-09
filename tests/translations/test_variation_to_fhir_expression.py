import pytest

from translators.variation_to_fhir import VariationToFhirTranslator

# Example from vrs-python translation test module

# https://www.ncbi.nlm.nih.gov/clinvar/variation/17848/?new_evidence=true
sub_input = {
    "hgvs": "NC_000019.10:g.44908822C>T",
    "spdi": "NC_000019.10:44908821:1:T",
}

sub_expected_hgvs = {
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
                                    "code": "LA30102-0",
                                    "display": "1-based character counting",
                                }
                            ]
                        },
                        "origin": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
                                    "code": "feature-start",
                                    "display": "Feature start",
                                }
                            ]
                        },
                        "normalizationMethod": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
                                    "code": "right-shift",
                                    "display": "Right shift",
                                }
                            ]
                        },
                    },
                    "startQuantity": {"value": 44908822.0},
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

sub_expected_spdi = {
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

# https://www.ncbi.nlm.nih.gov/clinvar/variation/1373966/?new_evidence=true
del_input = {
    "hgvs": "NC_000013.11:g.20003097del",
    "spdi": [
        "NC_000013.11:20003096:C:",
        "NC_000013.11:20003096:1:",
    ],  # check if these two would equal each other.
}

del_expected_hgvs = {
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
                    "reference": "#ref-to-nc000013",
                    "type": "MolecularDefinition",
                    "display": "NC_000013.11",
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
                            ]
                        },
                        "origin": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
                                    "code": "feature-start",
                                    "display": "Feature start",
                                }
                            ]
                        },
                        "normalizationMethod": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
                                    "code": "right-shift",
                                    "display": "Right shift",
                                }
                            ]
                        },
                    },
                    "startQuantity": {"value": 20003097.0},
                    "endQuantity": {"value": 20003097.0},
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
            "literal": {"value": ""},
        },
    ],
}

del_expected_spdi = {
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
                    "reference": "#ref-to-nc000013",
                    "type": "MolecularDefinition",
                    "display": "NC_000013.11",
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
                    "startQuantity": {"value": 20003096.0},
                    "endQuantity": {"value": 20003097.0},
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
            "literal": {"value": ""},
        },
    ],
}

# https://www.ncbi.nlm.nih.gov/clinvar/variation/1687427/?new_evidence=true
ins_input = {
    "hgvs": "NC_000013.11:g.20003010_20003011insG",
    "spdi": ["NC_000013.11:20003010::G", "NC_000013.11:20003010:0:G"],
}

ins_expected_hgvs = {
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
                    "reference": "#ref-to-nc000013",
                    "type": "MolecularDefinition",
                    "display": "NC_000013.11",
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
                            ]
                        },
                        "origin": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
                                    "code": "feature-start",
                                    "display": "Feature start",
                                }
                            ]
                        },
                        "normalizationMethod": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
                                    "code": "right-shift",
                                    "display": "Right shift",
                                }
                            ]
                        },
                    },
                    "startQuantity": {"value": 20003010.0},
                    "endQuantity": {"value": 20003011.0},
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
            "literal": {"value": ""},
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
            "literal": {"value": "G"},
        },
    ],
}

ins_expected_spdi = {
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
                    "reference": "#ref-to-nc000013",
                    "type": "MolecularDefinition",
                    "display": "NC_000013.11",
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
                    "startQuantity": {"value": 20003010.0},
                    "endQuantity": {"value": 20003010.0},
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
            "literal": {"value": ""},
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
            "literal": {"value": "G"},
        },
    ],
}

# https://www.ncbi.nlm.nih.gov/clinvar/variation/1264314/?new_evidence=true
dup_input = {
    "hgvs": "NC_000013.11:g.19993838_19993839dup",
    "spdi": "NC_000013.11:19993837:GT:GTGT",
}

dup_expected_hgvs = {
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
                    "reference": "#ref-to-nc000013",
                    "type": "MolecularDefinition",
                    "display": "NC_000013.11",
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
                            ]
                        },
                        "origin": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/coordinate-origin",
                                    "code": "feature-start",
                                    "display": "Feature start",
                                }
                            ]
                        },
                        "normalizationMethod": {
                            "coding": [
                                {
                                    "system": "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/normalization-method",
                                    "code": "right-shift",
                                    "display": "Right shift",
                                }
                            ]
                        },
                    },
                    "startQuantity": {"value": 19993838.0},
                    "endQuantity": {"value": 19993839.0},
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
            "literal": {"value": "GT"},
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
            "literal": {"value": "GTGT"},
        },
    ],
}

dup_expected_spdi = {
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
                    "reference": "#ref-to-nc000013",
                    "type": "MolecularDefinition",
                    "display": "NC_000013.11",
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
                    "startQuantity": {"value": 19993837.0},
                    "endQuantity": {"value": 19993839.0},
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
            "literal": {"value": "GT"},
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
            "literal": {"value": "GTGT"},
        },
    ],
}


@pytest.fixture
def variation_translator():
    return VariationToFhirTranslator()


def test_from_hgvs(variation_translator):
    assert (
        variation_translator.translate(sub_input["hgvs"], fmt="hgvs").model_dump()
        == sub_expected_hgvs
    )
    assert (
        variation_translator.translate(del_input["hgvs"], fmt="hgvs").model_dump()
        == del_expected_hgvs
    )
    assert (
        variation_translator.translate(ins_input["hgvs"], fmt="hgvs").model_dump()
        == ins_expected_hgvs
    )
    assert (
        variation_translator.translate(dup_input["hgvs"], fmt="hgvs").model_dump()
        == dup_expected_hgvs
    )


def test_from_spdi(variation_translator):
    assert (
        variation_translator.translate(sub_input["spdi"], fmt="spdi").model_dump()
        == sub_expected_spdi
    )

    del_results = [
        variation_translator.translate(spdi_input, fmt="spdi").model_dump()
        for spdi_input in del_input["spdi"]
    ]
    assert del_results[0] == del_results[1]
    assert del_results[0] == del_expected_spdi

    ins_results = [
        variation_translator.translate(spdi_input, fmt="spdi").model_dump()
        for spdi_input in ins_input["spdi"]
    ]
    assert ins_results[0] == ins_results[1]
    assert ins_results[0] == ins_expected_spdi

    assert (
        variation_translator.translate(dup_input["spdi"], fmt="spdi").model_dump()
        == dup_expected_spdi
    )
