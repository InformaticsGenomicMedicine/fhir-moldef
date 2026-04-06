import re
from decimal import Decimal

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

from conventions.coordinate_systems import vrs_coordinate_interval
from conventions.refseq_identifiers import (
    detect_sequence_type,
    refseq_to_fhir_id,
    translate_sequence_id,
    validate_accession,
)
from translators.validations.allele import validate_allele_profile, validate_vrs_allele
from translators.validations.indexing import apply_indexing
from vrs_tools.normalizer import VariantNormalizer

class MinimalFhirAlleleToVrsAlleleTranslator:
    """Provide minimal translation from a FHIR Allele Profile to a VRS Allele object."""
    def __init__(self, dp=None, uri: str | None = None):
        self.dp = dp or create_dataproxy(uri=uri)
        self.service = VariantNormalizer(dp=self.dp)
        self.allele_denormalizer = VariantNormalizer(dp=self.dp)

    def _is_valid_sequence_location(self, locations):
        """Validates the `sequenceLocation` structure within the provided locations to ensure all necessary attributes are present for accurate translations.

        Args:
            locations (list): A list of location objects containing `sequenceLocation` attributes.

        Raises:
            ValueError: If 'sequenceLocation' is missing in any location.
            ValueError: If 'coordinateInterval' is missing in any sequence location.
            ValueError: If 'coordinateSystem.system.coding' is missing in any coordinate interval.
            ValueError: If 'coding.display' is missing in 'coordinateSystem.system.coding'.
            ValueError: If 'startQuantity.value' is missing in any coordinate interval.
            ValueError: If 'endQuantity.value' is missing in any coordinate interval.

        Returns:
            sequence_location: The validated sequence location object.

        """
        for loc in locations:
            # Access sequenceLocation first
            sequence_location = loc.sequenceLocation
            if not sequence_location:
                raise ValueError("Missing 'sequenceLocation' in location.")
            # Check coordinateInterval existence
            if not sequence_location.coordinateInterval:
                raise ValueError("Missing 'coordinateInterval' in sequence location.")

            coordinate_interval = sequence_location.coordinateInterval

            # Check coordinateSystem.system.coding
            if not coordinate_interval.coordinateSystem.system.coding:
                raise ValueError(
                    "Missing 'coordinateSystem.system.coding' in coordinate interval."
                )

            if not any(
                coding.display
                for coding in coordinate_interval.coordinateSystem.system.coding
            ):
                raise ValueError(
                    "Missing 'coding.display' in 'coordinateSystem.system.coding'."
                )

            # Check startQuantity and endQuantity
            if not getattr(coordinate_interval.startQuantity, "value", None):
                raise ValueError(
                    "Missing 'startQuantity.value' in coordinate interval."
                )
            if not getattr(coordinate_interval.endQuantity, "value", None):
                raise ValueError("Missing 'endQuantity.value' in coordinate interval.")

        return sequence_location

    def _convert_decimal_to_int(self, value):
        """Validate and convert a Decimal value to an integer if possible.

        Args:
            value (Decimal): The value to be validated and converted.

        Raises:
            TypeError: If the value is not a Decimal.
            ValueError: If the Decimal value cannot be converted to an integer.

        Returns:
            int: The validated and converted integer value.

        """
        if not isinstance(value, Decimal):
            raise TypeError("Value is not a valid Decimal value.")

        if value == value.to_integral_value():
            value = int(value)
        else:
            raise TypeError(
                "Decimal Value must be able to be converted into an Integer"
            )
        return value

    def _validate_sequence(self, sequence):
        """Validate the sequence to ensure it contains valid characters as per VRS rules.

        Args:
            sequence (str): The sequence to be validated.

        Raises:
            ValueError: If the sequence contains invalid characters.

        Returns:
            str: The validated sequence.

        """
        pattern = r"^[A-Z*\-]*$"
        if not re.match(pattern, sequence):
            raise ValueError("Invalid sequence value")
        return sequence

    def _get_literal_value_for_allele_state(self, representations):
        """Retrieves the literal value associated with an `allele-state` representation, if present, from the provided list of representations.

        Args:
            representations (list): A list of representation objects that may include `allele-state` details.

        Raises:
                ValueError: If the `allele-state` representation is present but lacks a `literal.value`.

        Returns:
            str: The value of the `literal` attribute for the `allele-state` representation.

        """
        for rep in representations:
            focus = getattr(rep, "focus", None)
            if focus and any(
                coding.code == "allele-state" for coding in getattr(focus, "coding", [])
            ):
                literal = getattr(rep, "literal", None)
                if literal:
                    return literal.value
                else:
                    raise ValueError(
                        "Missing `literal.value` for the `allele-state` representation."
                    )

    def _validate_and_extract_code(self, expression):
        if not expression.contained:
            raise ValueError("Missing 'contained' field.")

        contained_item = expression.contained[0]
        if not contained_item.representation or len(contained_item.representation) != 1:
            raise ValueError(
                "Contained 'representation' must contain exactly one item."
            )

        representation_item = contained_item.representation[0]
        if not representation_item.code:
            raise ValueError("Missing 'code' field in representation.")

        code_item = representation_item.code[0]
        if not code_item.coding or not code_item.coding[0].code:
            raise ValueError("Missing 'coding.code' value.")

        return validate_accession(code_item.coding[0].code)

    def translate(self, expression, normalize=True):
        """Converts an FHIR Allele Profile object into a GA4GH VRS Allele object.

        Args:
            expression (Allele): A FHIR-compliant Allele containing sequence location,
                representation, and other metadata required for conversion.
            normalize (bool, optional): If True, returns a normalized VRS Allele using the VRS normalizer.
                Defaults to True.

        Raises:
            ValueError: Raised if multiple codings are found in the coordinate system or if the
                coordinate system is unsupported.

        Returns:
            models.Allele: A GA4GH VRS Allele object.
        """
        validate_allele_profile(expression)

        location_data = self._is_valid_sequence_location(expression.location)

        values_needed = {
            "refseq": self._validate_and_extract_code(expression),
            "start": location_data.coordinateInterval.startQuantity.value,
            "end": location_data.coordinateInterval.endQuantity.value,
        }

        coding_list = location_data.coordinateInterval.coordinateSystem.system.coding
        if len(coding_list) != 1:
            raise ValueError("Only one coding supported in coordinateSystem.")

        values_needed["coordinate_system_display"] = coding_list[0].display

        seq = self._get_literal_value_for_allele_state(expression.representation)
        start = apply_indexing(
            values_needed["coordinate_system_display"], values_needed["start"]
        )
        start_pos = self._convert_decimal_to_int(start)
        end_pos = self._convert_decimal_to_int(values_needed["end"])
        alt_seq = self._validate_sequence(seq)

        refget_accession = self.dp.derive_refget_accession(
            f"refseq:{values_needed['refseq']}"
        )
        seq_ref = SequenceReference(
            refgetAccession=refget_accession.split("refget:")[-1]
        )

        seq_location = SequenceLocation(
            sequenceReference=seq_ref,
            start=start_pos,
            end=end_pos,
        )
        lit_seq_expr = LiteralSequenceExpression(sequence=sequenceString(alt_seq))
        allele = Allele(location=seq_location, state=lit_seq_expr)

        return self.service.normalize(allele) if normalize else allele


class MinimalVrsAlleleToFhirAlleleTranslator:
    """Provide minimal translation from a FHIR Allele Profile to a VRS Allele object."""
    def __init__(self, dp=None, uri: str | None = None):
        self.dp = dp or create_dataproxy(uri=uri)
        self.service = VariantNormalizer(dp=self.dp)
        self.allele_denormalizer = VariantNormalizer(dp=self.dp)

    def _extract_vrs_values(self, expression, dp):
        """Extract GA4GH ID, RefSeq ID, start, end, and sequence from a VRS Allele.

        Args:
            expression: A VRS Allele object.
            dp: SeqRepo data proxy for ID translation.

        Returns:
            tuple: (refseq_id, start_pos, end_pos, alt_allele)
        """
        validate_vrs_allele(expression)

        refgetAccession = translate_sequence_id(dp, expression)
        start_pos = expression.location.start
        end_pos = expression.location.end
        alt_allele = expression.state.sequence.model_dump()

        return refgetAccession, start_pos, end_pos, alt_allele

    def translate(self, expression):
        """Converts an GA4GH VRS Allele object into FHIR Allele object.

        Args:
            expression (Allele): A VRS Allele object containing refgetAccession, start and end position, and alternative sequence.

        Raises:
            InvalidVRSAlleleError: Raised if the input is not a valid VRS Allele object.

        Returns:
            FhirAllele: The translated FHIR Allele Profile representation.
        """

        validate_vrs_allele(expression)

        if expression.state.type == "ReferenceLengthExpression":
            expression = self.allele_denormalizer.denormalize_reference_length(
                expression
            )

        refgetAccession, start_pos, end_pos, alt_allele = self._extract_vrs_values(
            expression, self.dp
        )

        sequence_type = detect_sequence_type(refgetAccession)

        mol_type = CodeableConcept(
            coding=[
                Coding(
                    system="http://hl7.org/fhir/sequence-type",
                    code=sequence_type.lower(),
                    display=f"{sequence_type} Sequence",
                )
            ]
        )

        coding_ref = Coding(
            system="http://www.ncbi.nlm.nih.gov/refseq",
            code=refgetAccession,
            # display="TBD-THIS IS A DEMO EXAMPLE"
        )

        code_value = CodeableConcept(coding=[coding_ref])
        representation_sequence = MolecularDefinitionRepresentation(code=[code_value])

        fhir_id = refseq_to_fhir_id(refseq_accession=refgetAccession)

        sequence_profile = FhirSequence(
            id=f"ref-to-{fhir_id}",
            moleculeType=mol_type,
            representation=[representation_sequence],
        )

        start_quant = Quantity(value=int(start_pos))
        end_quant = Quantity(value=int(end_pos))

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

        moldef_literal = MolecularDefinitionRepresentationLiteral(value=str(alt_allele))

        moldef_repr = MolecularDefinitionRepresentation(
            focus=focus_value, literal=moldef_literal
        )

        coord_system_fhir = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
            system=system, origin=origin, normalizationMethod=normalizationMethod
        )
        coord_interval = MolecularDefinitionLocationSequenceLocationCoordinateInterval(
            coordinateSystem=coord_system_fhir,
            startQuantity=start_quant,
            endQuantity=end_quant,
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


