# Genomic example
# NC_000007.13:g.140453136A>T
{
    "id": "ga4gh:VA.nmp-bzYpO00NYIqr3CaVF0ZH2ZpSj1ly",
    "type": "Allele",
    "name": "V600E",
    "description": "BRAF V600E variant",
    "aliases": ["RS113488022", "VAL600GLU", "V640E", "VAL640GLU"],
    "digest": "nmp-bzYpO00NYIqr3CaVF0ZH2ZpSj1ly",
    "expressions": [
        {
            "id": "expression:1",
            "syntax": "hgvs.g",
            "value": "NC_000007.13:g.140453136A>T",
            "syntax_version": "21.0",
        }
    ],
    "location": {
        "id": "ga4gh:SL.hVna-JOV5bBTGdXexL--IQm135MG3bGT",
        "type": "SequenceLocation",
        "name": "NC_000007.13",
        "description": "NC_000007.13 location description",
        "aliases": ["Ensembl:ENSP00000288602.6"],
        "digest": "hVna-JOV5bBTGdXexL--IQm135MG3bGT",
        "sequenceReference": {
            "id": "sequence_reference.id",
            "type": "SequenceReference",
            "name": "sequence_reference.name",
            "description": "sequence_reference.description",
            "aliases": ["sequence_reference.alias"],
            "refgetAccession": "SQ.IW78mgV5Cqf6M24hy52hPjyyo5tCCd86",
            "residueAlphabet": "na",
            "circular": False,
            "sequence": "A",
            "moleculeType": "genomic",
        },
        "start": 140453135,
        "end": 140453136,
        "sequence": "A",
    },
    "state": {
        "id": "state.id",
        "type": "LiteralSequenceExpression",
        "name": "state.name",
        "description": "My description for state",
        "aliases": ["my_sequence"],
        "sequence": "T",
    },
}


# Transcript example
# NM_004333.4:c.1799T>A
{
    "id": "ga4gh:VA.aWCHp3b-SdVM5GsaWVL8ZwhYUkMFXpC4",
    "type": "Allele",
    "name": "V600E",
    "description": "BRAF V600E variant",
    "aliases": ["RS113488022", "VAL600GLU", "V640E", "VAL640GLU"],
    "digest": "aWCHp3b-SdVM5GsaWVL8ZwhYUkMFXpC4",
    "expressions": [
        {
            "id": "expression:1",
            "syntax": "hgvs.c",
            "value": "NM_004333.4:c.1799T>A",
            "syntax_version": "21.0",
        }
    ],
    "location": {
        "id": "ga4gh:SL.IseAEMqzS3_flHuwYrh7o5P6cA7fE-Z5",
        "type": "SequenceLocation",
        "name": "NM_004333.4",
        "description": "NM_004333.4 location description",
        "aliases": ["Ensembl:ENSP00000288602.6"],
        "digest": "IseAEMqzS3_flHuwYrh7o5P6cA7fE-Z5",
        "sequenceReference": {
            "id": "sequence_reference.id",
            "type": "SequenceReference",
            "name": "sequence_reference.name",
            "description": "sequence_reference.description",
            "aliases": ["sequence_reference.alias"],
            "refgetAccession": "SQ.jkiXxxRjK7uTMiW2KQFjpgvF3VQi-HhX",
            "residueAlphabet": "na",
            "circular": False,
            "sequence": "T",
            "moleculeType": "mRNA",
        },
        "start": 1859,
        "end": 1860,
        "sequence": "T",
    },
    "state": {
        "id": "state.id",
        "type": "LiteralSequenceExpression",
        "name": "state.name",
        "description": "My description for state",
        "aliases": ["my_sequence"],
        "sequence": "A",
    },
}


# Protein example
# NP_004324.2:p.Val600Glu
{
    "id": "ga4gh:VA.j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
    "type": "Allele",
    "name": "V600E",
    "description": "BRAF V600E variant",
    "aliases": ["VAL600GLU", "V640E", "VAL640GLU"],
    "digest": "j4XnsLZcdzDIYa5pvvXM7t1wn9OITr0L",
    "expressions": [
        {
            "id": "expression:1",
            "syntax": "hgvs.p",
            "value": "NP_004324.2:p.Val600Glu",
            "syntax_version": "21.0",
        }
    ],
    "location": {
        "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "name": "NP_004324.2",
        "description": "My location description",
        "digest": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "type": "SequenceLocation",
        "sequenceReference": {
            "id": "sequence_reference.id",
            "name": "sequence_reference.name",
            "aliases": ["sequence_reference.alias"],
            "description": "sequence_reference.description",
            "refgetAccession": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y",
            "type": "SequenceReference",
            "residueAlphabet": "aa",
            "moleculeType": "protein",
            "circular": False,
            "sequence": "V",
        },
        "aliases": ["Ensembl:ENSP00000288602.6"],
        "start": 599,
        "end": 600,
        "sequence": "V",
    },
    "state": {
        "id": "state:1",
        "name": "state",
        "description": "My description for state",
        "sequence": "E",
        "type": "LiteralSequenceExpression",
        "aliases": ["my_sequence"],
    },
}


# DONT MODIFY BELOW
{
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
                    "value": False,  # This should be represented as a valueBoolean
                    "description": "expression.description.1",
                }
            ],
        },
        {"syntax": "hgvs.c", "value": "NM_004333.4:c.1799T>A"},
        {"syntax": "hgvs.g", "value": "NC_000007.13:g.140453136A>T"},
    ],
    "aliases": ["VAL600GLU", "V640E", "VAL640GLU"],
    "extensions": None,  # NOTE: A translation was not created for this yet
    "location": {
        "id": "ga4gh:SL.t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "name": "NP_004324.2",
        "description": "My location description",
        "digest": "t-3DrWALhgLdXHsupI-e-M00aL3HgK3y",
        "type": "SequenceLocation",
        "sequenceReference": {
            "id": "sequence_reference.id",
            "name": "sequence_reference.name",
            "aliases": ["sequence_reference.alias"],
            "description": "sequence_reference.description",
            "refgetAccession": "SQ.cQvw4UsHHRRlogxbWCB8W-mKD4AraM9y",
            "type": "SequenceReference",
            "residueAlphabet": "aa",
            "moleculeType": "protein",
            "circular": False,
            "sequence": "V",
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
        "sequence": "V",
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
