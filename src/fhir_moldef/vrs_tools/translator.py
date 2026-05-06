from ga4gh.vrs.extras.translator import AlleleTranslator


class VariantTranslator:
    """Translates external variant representations (SPDI, HGVS, Beacon) into VRS objects."""

    def __init__(self, dataproxy, default_assembly="GRCh38", identify=True):
        self.trl = AlleleTranslator(
            data_proxy=dataproxy,
            default_assembly_name=default_assembly,
            identify=identify,
        )
