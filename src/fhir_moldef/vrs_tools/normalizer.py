from ga4gh.core import ga4gh_identify
from ga4gh.vrs.dataproxy import create_dataproxy
from ga4gh.vrs.models import LiteralSequenceExpression
from ga4gh.vrs.normalize import (
    denormalize_reference_length_expression,
)
from ga4gh.vrs.normalize import (
    normalize as vrs_normalize,
)


class VariantNormalizer:
    """Handles variant normalization using GA4GH VRS."""

    def __init__(self, dp=None, uri: str | None = None):
        self.dp = dp or create_dataproxy(uri=uri)

    def normalize(self, allele):
        """Normalize an allele and assign GA4GH digest-based identifiers."""
        # Using the ga4gh normalize function to normalize the allele. (Coming form biocommons.normalize())
        allele = vrs_normalize(allele, self.dp)
        # Setting the allele id to a GA4GH digest-based id for the object, as a CURIE
        allele.id = ga4gh_identify(allele)
        # Setting the location id to a GA4GH digest-based id for the object, as a CURIE
        allele.location.id = ga4gh_identify(allele.location)

        return allele

    def denormalize_reference_length(self, ao):
        """Denormalize a ReferenceLengthExpression allele expression into a literal sequence."""
        sequence = f"ga4gh:{ao.location.get_refget_accession()}"

        aliases = self.dp.translate_sequence_identifier(sequence, "refseq")
        refseq_id = aliases[0].split(":")[1]

        ref_seq = self.dp.get_sequence(
            identifier=refseq_id, start=ao.location.start, end=ao.location.end
        )

        if ao.state.type == "ReferenceLengthExpression":
            alt_seq = denormalize_reference_length_expression(
                ref_seq=ref_seq,
                repeat_subunit_length=ao.state.repeatSubunitLength,
                alt_length=ao.state.length,
            )
            ao.state = LiteralSequenceExpression(sequence=alt_seq)

        return ao
