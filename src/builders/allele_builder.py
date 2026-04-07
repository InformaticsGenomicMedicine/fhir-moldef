from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from ga4gh.vrs.dataproxy import create_dataproxy
from ga4gh.vrs.models import (
    Allele,
    LiteralSequenceExpression,
    SequenceLocation,
    SequenceReference,
    sequenceString,
)

from conventions.coordinate_systems import vrs_coordinate_interval
from conventions.refseq_identifiers import (
    detect_sequence_type,
    refseq_to_fhir_id,
    validate_accession,
)
from profiles.allele import Allele as FhirAllele
from profiles.sequence import Sequence as FhirSequence
from resources.moleculardefinition import (
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)
from vrs_tools.normalizer import VariantNormalizer


class AlleleBuilder:
    """The goal of this module is to simplify the creation of FHIR Allele, eliminating the need to build them step by step or through the unpackaging process.
    These FHIR Allele will come with pre-filled attributes, allowing you to input just five key attributes: id, startQuantity, endQuantity, reference sequence, and literal value.
    This function specifically creates an FHIR Allele for Literal Value representation.
    """

    def __init__(self, dp=None, uri: str | None = None):
        self.dp = dp or create_dataproxy(uri=uri)
        self.service = VariantNormalizer(dp=self.dp)

    def build_vrs_allele(
        self,
        context_sequence_id: str,
        start: int,
        end: int,
        allele_state: str,
        normalize: bool = True,
    ):
        """Creates a Variant Representation Specification (VRS) Allele object.This method simplifies the creation of a VRS Allele so users do not need to directly interact with the underlying Python implementation of vrs-python.

        Args:
            context_sequence_id (str): Accession number of the reference sequence. Supported prefixes include: ("NC_", "NG_", "NM_", "NR_", "NP_")
            start (int): The start position of the allele (0-based interbase).
            end (int):  The end position of the allele (0-based interbase).
            allele_state (str): Literal value of the allele sequence state (e.g., ACGT).
            normalize (bool, optional): Weather to normalize the vrs allele or not. Defaults to True.
            id_value (str, optional): The unique identifier for the FHIR Allele instance. Defaults to None, and should be provided explicitly if required.

        Returns:
            models.Allele: A VRS Allele object, either in normalized form or as originally constructed.

        """
        refget_accession = self.dp.derive_refget_accession(
            f"refseq:{context_sequence_id}"
        )
        seq_ref = SequenceReference(
            refgetAccession=refget_accession.split("refget:")[-1]
        )

        seq_location = SequenceLocation(
            sequenceReference=seq_ref,
            start=start,
            end=end,
        )
        lit_seq_expr = LiteralSequenceExpression(sequence=sequenceString(allele_state))
        allele = Allele(location=seq_location, state=lit_seq_expr)
        if normalize:
            return self.service.normalize(allele)
        else:
            return allele

    def build_fhir_allele(
        self,
        context_sequence_id: str,
        start: int,
        end: int,
        allele_state: str,
        id_value: str = None,
    ):
        """Creates a FHIR (Fast Healthcare Interoperability Resources) Allele instance. This method simplifies the creation of a FHIR Allele resource by abstracting the underlying FHIR structure and data mapping.

        Args:
            context_sequence_id (str): Accession number of the reference sequence. Supported prefixes include: ("NC_", "NG_", "NM_", "NR_", "NP_")
            start (int):  The start position of the allele (0-based interbase).
            end (int):  The end position of the allele (0-based interbase).
            allele_state (str): Literal value of the allele sequence state (e.g., ACGT).
            id_value (str, optional): The unique identifier for the FHIR Allele instance. If not provided, a default ID will be generated in the format 'ref-to-{context_sequence_id}'.

        Returns:
            Allele: A fully constructed FHIR Allele resource.

        """
        val_sequence_id = validate_accession(refseq_id=context_sequence_id)

        sequence_type = detect_sequence_type(val_sequence_id)

        mol_type = CodeableConcept(
            coding=[
                {
                    "system": "http://hl7.org/fhir/sequence-type",
                    "code": sequence_type.lower(),
                    "display": f"{sequence_type} Sequence",
                }
            ]
        )

        coding_ref = Coding(
            system="http://www.ncbi.nlm.nih.gov/refseq",
            code=val_sequence_id,
        )

        code_value = CodeableConcept(coding=[coding_ref])
        representation_sequence = MolecularDefinitionRepresentation(code=[code_value])

        if id_value is not None:
            fhir_id = id_value
        else:
            fhir_id = refseq_to_fhir_id(refseq_accession=val_sequence_id)

        sequence_profile = FhirSequence(
            id=f"ref-to-{fhir_id}",
            moleculeType=mol_type,
            representation=[representation_sequence],
        )

        system, origin, normalizationMethod = vrs_coordinate_interval()

        seq_context = Reference(
            reference=f"#{sequence_profile.id}", type="MolecularDefinition"
        )
        focus_value = CodeableConcept(
            coding=[
                Coding(
                    system="http://hl7.org/fhir/moleculardefinition-focus",
                    code="allele-state",
                    display="Allele State",
                )
            ]
        )

        moldef_literal = MolecularDefinitionRepresentationLiteral(
            value=str(allele_state)
        )
        moldef_repr = MolecularDefinitionRepresentation(
            focus=focus_value, literal=moldef_literal
        )

        coord_system_fhir = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
            system=system, origin=origin, normalizationMethod=normalizationMethod
        )
        coord_interval = MolecularDefinitionLocationSequenceLocationCoordinateInterval(
            coordinateSystem=coord_system_fhir,
            startQuantity=Quantity(value=start),
            endQuantity=Quantity(value=end),
        )

        seq_location = MolecularDefinitionLocationSequenceLocation(
            sequenceContext=seq_context, coordinateInterval=coord_interval
        )

        location = MolecularDefinitionLocation(sequenceLocation=seq_location)

        return FhirAllele(
            contained=[sequence_profile],
            moleculeType=mol_type,
            location=[location],
            representation=[moldef_repr],
        )
