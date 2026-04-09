# source: https://github.com/cancervariants/metakb/blob/staging/server/tests/conftest.py#L548
vrs_synthetic_data = {
    "id": "ga4gh:VA.j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
    "type": "Allele",
    "name": "V600E",
    "description": "BRAF V600E variant",
    "digest": "j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
    "expressions": [
        {
            "id": "expression:1",
            "syntax": "hgvs.p",
            "value": "NP_004324.2:p.Val600Glu",
            "syntax_version": "21.0",
            "extensions": [
                {
                    "id": "sub-expression:1",
                    "name": "expression.name.1",
                    "value": "expression.value.1",
                    "description": "expression.description.1",
                    "extensions": [
                        {
                            "id": "sub-sub-expression:2",
                            "name": "expression.sub.name.2",
                            "value": "expression.sub.value,2",
                            "description": "expression.description.2",
                        }
                    ],
                }
            ],
        }
    ],
    "aliases": ["VAL600GLU", "V640E", "VAL640GLU"],
    # TODO: A translation was not created for this yet
    # "extensions": [
    #     {
    #         "name": "civic_variant_url",
    #         "value": "civicdb.org/links/variants/12",
    #         "description": "CIViC Variant URL",
    #         "extensions": [
    #             {
    #                 "id": "extension.sub_extension:1",
    #                 "name": "extension.sub_extension.name",
    #                 "value": "extension.sub_extension.value",
    #                 "description": "extension.sub_extension.description"
    #             }
    #         ]
    #     }
    # ],
    "location": {
        "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "name": "NP_004324.2",
        "description": "My location description",
        "digest": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "type": "SequenceLocation",
        "sequenceReference": {
            "id": "sequence_reference.id",
            "name": "sequence_reference.name",
            "aliases": ["sequence_reference.aliase"],
            "description": "sequence_reference.description",
            "refgetAccession": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y",
            "type": "SequenceReference",
            "residueAlphabet": "aa",
            "moleculeType": "protein",
            # TODO: Currently FHIR doesn't support circular Sequence
            # "circular": False,
            "sequence": "V",  # A sequenceString that is a literal representation of the referenced sequence.
            "extensions": [
                {
                    "id": "sequence_reference.extension:1",
                    "name": "sequence_reference.extension.name",
                    "value": "sequence_reference.extension.value",
                    "description": "sequence_reference.extension.description",
                    "extensions": [
                        {
                            "id": "sequence_reference.sub_extension:1",
                            "name": "sequence_reference.sub_extension.name",
                            "value": "sequence_reference.sub_extension.value",
                            "description": "sequence_reference.sub_extension.description",
                        }
                    ],
                }
            ],
        },
        "aliases": ["Ensembl:ENSP00000288602.6"],
        "start": 599,
        "end": 600,
        "sequence": "V",  # The literal sequence encoded by the sequenceReference at these coordinates.
        "extensions": [
            {
                "id": "sequence_location.extension:1",
                "name": "sequence_location.name",
                "value": "sequence_location.value",
                "description": "sequence_location.description",
                "extensions": [
                    {
                        "id": "sequence_location.sub_extension:1",
                        "name": "sequence_location.sub_extension.name",
                        "value": "sequence_location.sub_extension.value",
                        "description": "sequence_location.sub_extension.description",
                    }
                ],
            }
        ],
    },
    "state": {
        "id": "state:1",
        "name": "state",
        "description": "My description for state",
        "sequence": "E",
        "type": "LiteralSequenceExpression",
        "extensions": [
            {
                "id": "state.extension:1",
                "name": "state.name",
                "value": "state.value",
                "description": "state.description",
                "extensions": [
                    {
                        "id": "state.sub_extension:1",
                        "name": "state.sub_extension.name",
                        "value": "state.sub_extension.value",
                        "description": "state.sub_extension.description",
                    }
                ],
            }
        ],
        "aliases": ["my_sequence"],
    },
}

# This output is generated by converting the original VRS value (input_vrs_data) into a FHIR allele profile.
fhir_synthetic_data = {
    "resourceType": "MolecularDefinition",
    "contained": [
        {
            "resourceType": "MolecularDefinition",
            "id": "vrs-location-sequence",
            "moleculeType": {
                "coding": [
                    {
                        "code": "amino acid",
                        "display": "amino acid Sequence",
                        "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/moleculeType",
                    }
                ]
            },
            "representation": [{"literal": {"value": "V"}}],
        },
        {
            "resourceType": "MolecularDefinition",
            "id": "vrs-location-sequenceReference",
            "extension": [
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/id",
                    "valueString": "sequence_reference.id",
                },
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/name",
                    "valueString": "sequence_reference.name",
                },
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/description",
                    "valueString": "sequence_reference.description",
                },
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/aliases",
                    "valueString": "sequence_reference.aliase",
                },
                {
                    "id": "sequence_reference.extension:1",
                    "extension": [
                        {
                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                            "valueString": "sequence_reference.extension.name",
                        },
                        {
                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                            "valueString": "sequence_reference.extension.value",
                        },
                        {
                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                            "valueString": "sequence_reference.extension.description",
                        },
                        {
                            "id": "sequence_reference.sub_extension:1",
                            "extension": [
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                                    "valueString": "sequence_reference.sub_extension.name",
                                },
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                                    "valueString": "sequence_reference.sub_extension.value",
                                },
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                                    "valueString": "sequence_reference.sub_extension.description",
                                },
                            ],
                        },
                    ],
                },
            ],
            "moleculeType": {
                "coding": [
                    {
                        "code": "amino acid",
                        "display": "amino acid Sequence",
                        "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/moleculeType",
                    }
                ]
            },
            "representation": [
                {
                    "code": [
                        {
                            "coding": [
                                {
                                    "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/refgetAccession",
                                    "code": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y",
                                }
                            ]
                        }
                    ],
                    "literal": {
                        "encoding": {
                            "coding": [
                                {
                                    "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/residueAlphabet",
                                    "code": "aa",
                                }
                            ]
                        },
                        "value": "V",
                    },
                }
            ],
        },
    ],
    "identifier": [
        {
            "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/id",
            "value": "ga4gh:VA.j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
        },
        {
            "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/name",
            "value": "V600E",
        },
        {
            "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/aliases",
            "value": "VAL600GLU",
        },
        {
            "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/aliases",
            "value": "V640E",
        },
        {
            "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/aliases",
            "value": "VAL640GLU",
        },
        {
            "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/Allele#properties/digest",
            "value": "j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
        },
    ],
    "description": "BRAF V600E variant",
    "moleculeType": {
        "coding": [
            {
                "code": "amino acid",
                "display": "amino acid Sequence",
                "system": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceReference#properties/moleculeType",
            }
        ]
    },
    "location": [
        {
            "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
            "extension": [
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/name",
                    "valueString": "NP_004324.2",
                },
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/description",
                    "valueString": "My location description",
                },
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/aliases",
                    "valueString": "Ensembl:ENSP00000288602.6",
                },
                {
                    "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/SequenceLocation#properties/digest",
                    "valueString": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
                },
                {
                    "id": "sequence_location.extension:1",
                    "extension": [
                        {
                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                            "valueString": "sequence_location.name",
                        },
                        {
                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                            "valueString": "sequence_location.value",
                        },
                        {
                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                            "valueString": "sequence_location.description",
                        },
                        {
                            "id": "sequence_location.sub_extension:1",
                            "extension": [
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                                    "valueString": "sequence_location.sub_extension.name",
                                },
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                                    "valueString": "sequence_location.sub_extension.value",
                                },
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                                    "valueString": "sequence_location.sub_extension.description",
                                },
                            ],
                        },
                    ],
                },
            ],
            "sequenceLocation": {
                "sequenceContext": {
                    "reference": "#vrs-location-sequence",
                    "type": "Sequence",
                    "display": "VRS location.sequence as contained FHIR Sequence.",
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
                    "startQuantity": {"value": 599.0},
                    "endQuantity": {"value": 600.0},
                },
            },
        }
    ],
    "representation": [
        {
            "focus": {
                "coding": [
                    {
                        # In the new Allele examples, the `system` field is set to the value shown below.
                        # However, the Allele profile (allele.py) does not currently enforce this 1:1 match.
                        # Need to confirm whether this is now the official system value before enabling the check:
                        # "http://hl7.org/fhir/uv/molecular-definition-data-types/CodeSystem/molecular-definition-focus"
                        "system": "http://hl7.org/fhir/moleculardefinition-focus",
                        "code": "allele-state",
                        "display": "Allele State",
                    }
                ]
            },
            "code": [
                {
                    "id": "expression:1",
                    "extension": [
                        {
                            "id": "sub-expression:1",
                            "extension": [
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                                    "valueString": "expression.name.1",
                                },
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                                    "valueString": "expression.value.1",
                                },
                                {
                                    "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                                    "valueString": "expression.description.1",
                                },
                                {
                                    "id": "sub-sub-expression:2",
                                    "extension": [
                                        {
                                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                                            "valueString": "expression.sub.name.2",
                                        },
                                        {
                                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                                            "valueString": "expression.sub.value,2",
                                        },
                                        {
                                            "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                                            "valueString": "expression.description.2",
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                    "coding": [
                        {
                            "version": "21.0",
                            "code": "NP_004324.2:p.Val600Glu",
                            "display": "hgvs.p",
                        }
                    ],
                }
            ],
            "literal": {
                "id": "state:1",
                "extension": [
                    {
                        "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/name",
                        "valueString": "state",
                    },
                    {
                        "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/description",
                        "valueString": "My description for state",
                    },
                    {
                        "url": "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/LiteralSequenceExpression#properties/aliases",
                        "valueString": "my_sequence",
                    },
                    {
                        "id": "state.extension:1",
                        "extension": [
                            {
                                "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                                "valueString": "state.name",
                            },
                            {
                                "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                                "valueString": "state.value",
                            },
                            {
                                "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                                "valueString": "state.description",
                            },
                            {
                                "id": "state.sub_extension:1",
                                "extension": [
                                    {
                                        "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/name",
                                        "valueString": "state.sub_extension.name",
                                    },
                                    {
                                        "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/value",
                                        "valueString": "state.sub_extension.value",
                                    },
                                    {
                                        "url": "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/Extension#properties/description",
                                        "valueString": "state.sub_extension.description",
                                    },
                                ],
                            },
                        ],
                    },
                ],
                "value": "E",
            },
        }
    ],
}
