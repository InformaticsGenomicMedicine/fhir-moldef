import hgvs.parser
from ga4gh.vrs.utils.hgvs_tools import HgvsTools


# NOTE: Consider removing this module now that we can use Podman and have access to the UTA database.
# NOTE: Evaluate using hgvstools as a replacement for this module.
class HgvsToolsLite(HgvsTools):
    """
    A lightweight subclass of HgvsTools that does not connect to the UTA database.
    Provides parsing and syntax validation only.
    """

    def __init__(self, data_proxy=None):
        self.data_proxy = data_proxy
        self.parser = hgvs.parser.Parser()

        # make UTA-related attrs exist but disabled
        # Need to write a Query to see if i get a connection form UTA
        self.uta_conn = None
        self.normalizer = None
        self.variant_mapper = None
