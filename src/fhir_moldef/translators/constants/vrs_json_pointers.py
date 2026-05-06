# VRS JSON pointers preserve attribute semantics during VRS-to-FHIR translation
# by referencing original schema definitions. This ensures each attribute's meaning remains clear.

# Define core URLs for VRS and GKS schemas
VRS_CORE_URL = "https://w3id.org/ga4gh/schema/vrs/2.0.1/json/"
GKS_CORE_URL = "https://github.com/ga4gh/gks-core/blob/1.0/schema/gks-core/json/"


def build_identifier(url, entity, fields):
    """Build a dictionary of field identifiers for a given GA4GH schema entity.

    Args:
        url (str): Base URL of the schema.
        entity (str): The name of the entity (e.g., 'Allele', 'SequenceLocation').
        fields (list): List of field names for the entity.

    Returns:
        dict: A dictionary mapping field names to fully qualified schema URLs.
    """
    return {field: f"{url}{entity}#properties/{field}" for field in fields}


# === VRS Entities ===

allele_identifiers = build_identifier(
    url=VRS_CORE_URL,
    entity="Allele",
    fields=["id", "name", "aliases", "digest", "location", "state"],
)

literal_sequence_expression_identifiers = build_identifier(
    url=VRS_CORE_URL,
    entity="LiteralSequenceExpression",
    fields=["id", "name", "description", "aliases", "extensions", "sequence"],
)

expression_identifiers = build_identifier(
    url=VRS_CORE_URL,
    entity="Expression",
    fields=["id", "extensions", "syntax", "value", "syntax_version"],
)

sequence_location_identifiers = build_identifier(
    url=VRS_CORE_URL,
    entity="SequenceLocation",
    fields=[
        "id",
        "name",
        "description",
        "aliases",
        "extensions",
        "digest",
        "sequenceReference",
        "start",
        "end",
        "sequence",
    ],
)

sequence_reference_identifiers = build_identifier(
    url=VRS_CORE_URL,
    entity="SequenceReference",
    fields=[
        "id",
        "name",
        "description",
        "aliases",
        "extensions",
        "refgetAccession",
        "residueAlphabet",
        "sequence",
        "moleculeType",
        "circular",
    ],
)

# Standalone sequence string identifier (not tied to a specific entity)
sequence_string_identifier = {"id": f"{VRS_CORE_URL}sequenceString"}

# === GKS Entities ===

extension_identifiers = build_identifier(
    url=GKS_CORE_URL,
    entity="Extension",
    fields=["id", "extensions", "name", "aliases", "value", "description"],
)
