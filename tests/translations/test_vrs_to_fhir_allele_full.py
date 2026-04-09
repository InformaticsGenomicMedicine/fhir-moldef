import pytest
from ga4gh.vrs.models import Allele as VrsAllele

from profiles.allele import Allele as FhirAllele
from tests.translations.examples.allele_test_data import fhir_synthetic_data, vrs_synthetic_data
from translators.vrs_to_fhir_allele import VrsToFhirAlleleTranslator


@pytest.fixture
def vrs_to():
    return VrsToFhirAlleleTranslator()


@pytest.fixture
def vrs_allele_instance():
    return VrsAllele(**vrs_synthetic_data)


@pytest.fixture
def fhir_allele_instance():
    return FhirAllele(**fhir_synthetic_data)


def test_full_allele_translator_returns_expected(
    vrs_allele_instance, vrs_to, fhir_allele_instance
):
    fhir_obj = vrs_to.translate(vrs_allele_instance)
    assert isinstance(fhir_obj, FhirAllele)
    assert fhir_obj.model_dump(exclude_none=True) == fhir_allele_instance.model_dump(
        exclude_none=True
    )


def test_optional_expressions_field(vrs_to, vrs_allele_instance):
    vrs_allele_instance.expressions = []

    fhir_obj = vrs_to.translate(vrs_allele_instance)
    assert fhir_obj.representation[0].code is None


def test_translate_allele_with_missing_optional_fields(vrs_to, vrs_allele_instance):
    vrs_allele_instance.id = None
    vrs_allele_instance.name = None
    vrs_allele_instance.digest = None
    vrs_allele_instance.aliases = []

    fhir_obj = vrs_to.translate(vrs_allele_instance)
    assert fhir_obj.identifier is None


def test_sequence_reference_missing_optional_fields(vrs_to, vrs_allele_instance):
    vrs_allele_instance.location.sequenceReference.id = None
    vrs_allele_instance.location.sequenceReference.name = None
    vrs_allele_instance.location.sequenceReference.aliases = None
    vrs_allele_instance.location.sequenceReference.description = None
    vrs_allele_instance.location.sequenceReference.extensions = None

    fhir_obj = vrs_to.translate(vrs_allele_instance)
    assert fhir_obj.contained[1].extension is None


def test_location_missing_optional_fields(vrs_to, vrs_allele_instance):
    vrs_allele_instance.location.id = None
    vrs_allele_instance.location.name = None
    vrs_allele_instance.location.description = None
    vrs_allele_instance.location.digest = None
    vrs_allele_instance.location.aliases = None
    vrs_allele_instance.location.extensions = None

    fhir_obj = vrs_to.translate(vrs_allele_instance)
    assert fhir_obj.location[0].extension is None


def test_state_missing_optional_fields(vrs_to, vrs_allele_instance):
    vrs_allele_instance.state.id = None
    vrs_allele_instance.state.name = None
    vrs_allele_instance.state.description = None
    vrs_allele_instance.state.aliases = None
    vrs_allele_instance.state.extensions = None

    fhir_obj = vrs_to.translate(vrs_allele_instance)
    assert fhir_obj.representation[0].literal.extension is None


def test_seqref_sequence_optional_field(vrs_to, vrs_allele_instance):
    # Note, in order to have literal we must have sequence in sequenceReference
    vrs_allele_instance.location.sequenceReference.sequence = None

    fhir_obj = vrs_to.translate(vrs_allele_instance)
    assert fhir_obj.contained[1].representation[0].literal is None
