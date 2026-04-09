import pytest
from ga4gh.vrs.models import Allele as VrsAllele

from profiles.allele import Allele as FhirAllele
from tests.translations.examples.allele_test_data import fhir_synthetic_data, vrs_synthetic_data
from translators.fhir_to_vrs_allele import FhirToVrsAlleleTranslator

@pytest.fixture
def fhir_to():
    return FhirToVrsAlleleTranslator()


@pytest.fixture
def fhir_allele_instance():
    return FhirAllele(**fhir_synthetic_data)


@pytest.fixture
def vrs_allele_instance():
    return VrsAllele(**vrs_synthetic_data)


def test_full_allele_translator_returns_expected(
    fhir_allele_instance, fhir_to, vrs_allele_instance
):
    vrs_obj = fhir_to.translate(fhir_allele_instance)
    assert isinstance(vrs_obj, VrsAllele)
    assert vrs_obj.model_dump(exclude_none=True) == vrs_allele_instance.model_dump(
        exclude_none=True
    )


def test_missing_contained_sequences_raises(fhir_to, fhir_allele_instance):
    fhir_allele_instance.contained = []

    with pytest.raises(
        ValueError,
        match="Both 'vrs-location-sequence' and 'vrs-location-sequenceReference' are missing.",
    ):
        fhir_to.translate(fhir_allele_instance)


def test_unsupported_molecule_type_raises(fhir_to, fhir_allele_instance):
    fhir_allele_instance.contained[1].moleculeType.coding[0].code = "carbohydrate"

    with pytest.raises(ValueError, match="Unsupported moleculeType: 'carbohydrate'"):
        fhir_to.translate(fhir_allele_instance)


def test_translate_allele_with_missing_optional_fields(fhir_to, fhir_allele_instance):
    fhir_allele_instance.identifier = []
    fhir_allele_instance.representation[0].code[0].coding[0].version = None
    fhir_allele_instance.representation[0].literal.extension = []

    vrs_obj = fhir_to.translate(fhir_allele_instance)
    assert vrs_obj.aliases is None
    assert vrs_obj.name is None
    assert vrs_obj.expressions[0].syntax_version is None
    assert vrs_obj.state.extensions is None


def test_optional_code_field(fhir_to, fhir_allele_instance):
    fhir_allele_instance.representation[0].code = []

    vrs_obj = fhir_to.translate(fhir_allele_instance)
    assert vrs_obj.expressions is None
