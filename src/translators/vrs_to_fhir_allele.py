from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from ga4gh.vrs.dataproxy import create_dataproxy

from conventions.coordinate_systems import vrs_coordinate_interval
from conventions.refseq_identifiers import (
    detect_sequence_type,
    translate_sequence_id,
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
from translators.constants.vrs_json_pointers import allele_identifiers as ALLELE_PTRS
from translators.constants.vrs_json_pointers import extension_identifiers as EXT_PTRS
from translators.constants.vrs_json_pointers import (
    literal_sequence_expression_identifiers as LSE_PTRS,
)
from translators.constants.vrs_json_pointers import (
    sequence_location_identifiers as SEQ_LOC_PTRS,
)
from translators.constants.vrs_json_pointers import (
    sequence_reference_identifiers as SEQ_REF_PTRS,
)
from translators.validations.allele import (
    validate_vrs_allele,
)
from vrs_tools.normalizer import VariantNormalizer


class VrsToFhirAlleleTranslator:
    """Translate GA4GH VRS Allele objects into the FHIR Allele Profile,providing full translation."""
    def __init__(self, dp=None, uri: str | None = None):
        self.dp = dp or create_dataproxy(uri=uri)
        self.allele_denormalize = VariantNormalizer(dp=self.dp)

    def translate(self, vrs_allele):
        """Convert a GA4GH VRS Allele object into its corresponding FHIR Allele Profile representation, currently supporting only alleles with a state type of LiteralSequenceExpression or ReferenceLengthExpression."""
        validate_vrs_allele(vrs_allele)

        if vrs_allele.state.type == "ReferenceLengthExpression":
            vrs_allele = self.allele_denormalize.denormalize_reference_length(
                vrs_allele
            )

        return FhirAllele(
            identifier=self.map_identifiers(vrs_allele),
            contained=self.map_contained(vrs_allele),
            description=self.map_description(vrs_allele),
            # NOTE: The moleculeType is inferred based on if it is present in the allele or the refget accession.
            moleculeType=self.map_mol_type(vrs_allele),
            # NOTE: At this time we will not be supporting Exension.
            # extension = self.map_extensions(vrs_allele),
            location=[self.map_location(vrs_allele)],
            representation=[self.map_lit_to_rep_lit_expr(vrs_allele)],
        )

    # --------------------------------------------------------------------------------------------

    def _extract_str(self, val):
        """Extract a string value from the input, which may be a plain string or a Pydantic RootModel.

        Args:
            val (str,object): The input value. Expected to be either a string or an object with a 'root' attribute

        Raises:
            TypeError: If the input is neither a string nor a compatible RootModel-like object.

        Returns:
            str | None: The extracted string if valid, or None if the input is None.

        """
        if val is None:
            return None
        if hasattr(val, "root"):
            return val.root
        raise TypeError(f"Expected a string or RootModel[str], got {type(val)}")

    # ========== MolecularType Mapping ==========

    def map_mol_type(self, ao):
        """Maps the molecular type of a sequence to a FHIR CodeableConcept using its refget accession.

        Args:
            ao (object): A VRS Allele object referencing a Refget accession.

        Returns:
            CodeableConcept: A FHIR-compliant CodeableConcept indicating the sequence type (e.g., DNA, RNA, or AA) based on the detected molecular type.

        """
        mapped_mol_type = {
            "genomic": "dna",
            "RNA": "rna",
            "mRNA": "rna",
            "protein": "amino acid",
        }

        molecule_type = getattr(ao.location.sequenceReference, "moleculeType", None)

        if not molecule_type:
            refget_accession = translate_sequence_id(dp=self.dp, expression=ao)
            sequence_type = detect_sequence_type(refget_accession)
        else:
            sequence_type = molecule_type

        molecule_type = mapped_mol_type.get(sequence_type)

        return CodeableConcept(
            coding=[
                Coding(
                    system=SEQ_REF_PTRS["moleculeType"],
                    code=molecule_type.lower(),
                    display=f"{molecule_type} Sequence",
                )
            ]
        )

    # ========== Identifiers Mapping ==========

    def map_identifiers(self, ao):
        """Maps various identifier fields from the input object to a list of FHIR Identifier instances.

        Args:
            ao (object): A VRS Allele object that may include metadata such as id, name, aliases, and computed identifier.

        Returns:
            list[Identifier] | None: A list of FHIR Identifier objects, or None if no identifiers are present.

        """
        identifiers = []
        identifiers.extend(self._map_id(ao))
        identifiers.extend(self._map_name(ao))
        identifiers.extend(self._map_aliases(ao))
        identifiers.extend(self._map_digest(ao))
        return identifiers or None

    def _map_id(self, ao):
        """Maps a VRS id to a FHIR Identifier, setting the system to reflect its origin in the VRS specification."""
        value = getattr(ao, "id", None)
        if value:
            return [Identifier(value=value, system=ALLELE_PTRS["id"])]
        return []

    def _map_name(self, ao):
        """Maps a VRS name to a FHIR Identifier, setting the system to reflect its origin in the VRS specification."""
        value = getattr(ao, "name", None)
        if value:
            return [Identifier(value=value, system=ALLELE_PTRS["name"])]
        return []

    def _map_aliases(self, ao):
        """Maps a VRS aliases to a FHIR Identifier, setting the system to reflect its origin in the VRS specification."""
        value = getattr(ao, "aliases", None)
        if value:
            return [
                Identifier(value=alias, system=ALLELE_PTRS["aliases"])
                for alias in ao.aliases
            ]
        return []

    def _map_digest(self, ao):
        """Maps a VRS digest to a FHIR Identifier, setting the system to reflect its origin in the VRS specification."""
        value = getattr(ao, "digest", None)
        if value:
            return [Identifier(value=value, system=ALLELE_PTRS["digest"])]
        return []

    # ========== Description Mapping ==========

    def map_description(self, ao):
        """Maps the VRS description to FHIR's description.markdown."""
        return getattr(ao, "description", None)

    # ========== Extensions Mapping ==========

    def map_extensions(self, source):
        """Maps VRS extensions from the input object to a list of FHIR Extension instances.

        Args:
            source (object): The input object, expected to have an 'extensions' attribute.

        Returns:
            list | None: A list of FHIR Extension objects, or None if no extensions are present.

        """
        vrs_exts = getattr(source, "extensions", None)
        if not vrs_exts:
            return None
        return [self._map_ext(ext_obj) for ext_obj in vrs_exts]

    def _map_ext(self, ext_obj):
        """Maps a VRS Extension object to a FHIR Extension, including its sub-extensions.

        Args:
            ext_obj (object): A VRS Extension object containing fields such as id, name, value, description, and possibly nested extensions.

        Returns:
            Extension: A FHIR Extension object representing the input VRS extension and its nested structure.

        """
        extension = Extension(
            id=ext_obj.id,
        )

        sub_exts = []
        sub_exts.extend(self._map_name_subext(ext_obj))
        sub_exts.extend(self._map_value_subext(ext_obj))
        sub_exts.extend(self._map_description_subext(ext_obj))
        sub_exts.extend(self._map_nested_extensions(ext_obj))

        if sub_exts:
            extension.extension = sub_exts

        return extension

    def _map_name_subext(self, ext_obj):
        """Returns a FHIR Extension for the 'name' field, if present."""
        if getattr(ext_obj, "name", None):
            return [Extension(url=EXT_PTRS["name"], valueString=ext_obj.name)]

    def _map_value_subext(self, ext_obj):
        """Returns a FHIR Extension for the 'value' field, if present."""
        value = getattr(ext_obj, "value", None)
        if value is not None:
            extension = Extension(url=EXT_PTRS["value"])
            self._assign_extension_value(extension, value)
            return [extension]

    def _map_description_subext(self, ext_obj):
        """Returns a FHIR sub-extension for the 'description' field, if present."""
        if getattr(ext_obj, "description", None):
            return [
                Extension(url=EXT_PTRS["description"], valueString=ext_obj.description)
            ]
        return []

    def _map_nested_extensions(self, ext_obj):
        """Maps and returns nested extensions as FHIR sub-extensions, or an empty list if none are present."""
        if not getattr(ext_obj, "extensions", None):
            return []
        return [self._map_ext(nested) for nested in ext_obj.extensions]

    def _assign_extension_value(self, extension, value):
        """Assigns a value to the appropriate attribute of a FHIR extension based on the value's type (str, bool, or float).

        TODO: need to figure out how we are going to map dictionary, list and null values.
        """
        if value is None:
            return

        type_map = {
            str: "valueString",
            bool: "valueBoolean",
            float: "valueDecimal",
            int: "valueInteger",
        }

        for expected_type, attr_name in type_map.items():
            if isinstance(value, expected_type):
                setattr(extension, attr_name, value)
                return

        raise TypeError(
            "Unsupported extension value type. Must be str, bool, or float."
        )

    # ========== Sub-Extensions Mapping ==========

    def _map_location_extensions(self, source):
        """Generates a list of FHIR `Extension` instances based on attributes from a VRS.Location object (`name`, `description`, `aliases`, `digest`, `extensions`).

        Args:
            source (object):A VRS.Location object that may contain `name`, `description`, `aliases`, `digest`, and `extensions` attributes.

        Returns:
            List: A list of FHIR `Extension` objects created from the VRS.Location attributes.

        """
        exts = []
        exts.extend(self._map_name_sub(source, url_base=SEQ_LOC_PTRS["name"]))
        exts.extend(
            self._map_description_sub(source, url_base=SEQ_LOC_PTRS["description"])
        )
        exts.extend(self._map_aliases_sub(source, url_base=SEQ_LOC_PTRS["aliases"]))
        exts.extend(self._map_digest_sub(source, url_base=SEQ_LOC_PTRS["digest"]))
        exts.extend(self.map_extensions(source=source) or [])
        return exts or None

    def _map_lse_extensions(self, source):
        """Generates a list of FHIR `Extension` instances based on attributes from a VRS.State.LiteralSequenceExpression object (`name`, `description`, `aliases`, `extensions`).

        Args:
            source (object):A VRS.State.LiteralSequenceExpression object that may contain `name`, `description`, `aliases`, and `extensions` attributes.

        Returns:
            List: A list of FHIR `Extension` objects created from the VRS.State.LiteralSequenceExpression attributes.

        """
        exts = []
        exts.extend(self._map_name_sub(source, url_base=LSE_PTRS["name"]))
        exts.extend(self._map_description_sub(source, url_base=LSE_PTRS["description"]))
        exts.extend(self._map_aliases_sub(source, url_base=LSE_PTRS["aliases"]))
        exts.extend(self.map_extensions(source=source) or [])
        return exts or None

    def _map_seqref_extensions(self, source):
        """Generates a list of FHIR `Extension` instances based on attributes from a VRS.Location.sequenceReference object (`id`, `name`, `description`, `aliases`, `extensions`).

        Args:
            source (object):A VRS.Location.sequenceReference object that may contain `id`, `name`, `description`, `aliases`, `extensions` attributes.

        Returns:
            List: A list of FHIR `Extension` objects created from the VRS.Location.sequenceReference attributes.

        """
        exts = []
        exts.extend(self._map_id_sub(source, url_base=SEQ_REF_PTRS["id"]))
        exts.extend(self._map_name_sub(source, url_base=SEQ_REF_PTRS["name"]))
        exts.extend(
            self._map_description_sub(source, url_base=SEQ_REF_PTRS["description"])
        )
        exts.extend(self._map_aliases_sub(source, url_base=SEQ_REF_PTRS["aliases"]))
        exts.extend(self.map_extensions(source=source) or [])
        return exts or None

    def _map_id_sub(self, source, url_base):
        """Returns a FHIR `Extension` for the `id` attribute if present in the source object."""
        if getattr(source, "id", None):
            return [Extension(url=url_base, valueString=source.id)]
        return []

    def _map_name_sub(self, source, url_base):
        """Returns a FHIR `Extension` for the `name` attribute if present in the source object."""
        if getattr(source, "name", None):
            return [Extension(url=url_base, valueString=source.name)]
        return []

    def _map_description_sub(self, source, url_base):
        """Returns a FHIR `Extension` for the `description` attribute if present in the source object."""
        if getattr(source, "description", None):
            return [Extension(url=url_base, valueString=source.description)]
        return []

    def _map_aliases_sub(self, source, url_base):
        """Returns a FHIR `Extension` for the `aliases` attribute if present in the source object."""
        aliases = getattr(source, "aliases", []) or []
        return [Extension(url=url_base, valueString=alias) for alias in aliases]

    def _map_digest_sub(self, source, url_base):
        """Returns a FHIR `Extension` for the `digest` attribute if present in the source object."""
        if getattr(source, "digest", None):
            return [Extension(url=url_base, valueString=source.digest)]
        return []

    # ========== Representation Literal Mapping ==========

    def map_lit_to_rep_lit_expr(self, ao):
        """Maps a VRS Allele State to a FHIR MolecularDefinitionRepresentation with a literal sequence expression.

        Args:
            ao (Object): A VRS Allele object containing literal sequence expression.

        Returns:
            Object: A FHIR representation of the allele with focus, code, and literal fields populated.

        """
        # NOTE: this is hard coded because its required in the FHIR Allele Schema.
        focus_value = CodeableConcept(
            coding=[
                Coding(
                    system="http://hl7.org/fhir/moleculardefinition-focus",
                    code="allele-state",
                    display="Allele State",
                )
            ]
        )

        rep = MolecularDefinitionRepresentation(
            focus=focus_value,
            code=self._map_codeable_concept(ao),
            literal=self._map_literal_representation(ao),
        )
        return rep

    def _map_coding(self, exp):
        """Maps a VRS expression to a FHIR Coding object using its syntax, value, and syntax_version.

        Maps:
            - vrs.syntax         -> Coding.display
            - vrs.value          -> Coding.code
            - vrs.syntax_version -> Coding.version
        """
        return Coding(
            display=exp.syntax,
            code=exp.value,
            version=exp.syntax_version,
        )

    def _map_codeable_concept(self, ao):
        """Maps the `expressions` attribute of the input object to a list of FHIR CodeableConcept instances.

        Each expression is converted to a CodeableConcept using:
          - vrs.expressions.id -> CodeableConcept.id
          - map_extensions(exp) -> CodeableConcept.extension
          - _map_coding(exp) -> CodeableConcept.coding
        """
        expressions = getattr(ao, "expressions", None)
        if not expressions:
            return None

        cc_list = []
        for exp in expressions:
            cc = CodeableConcept(
                id=exp.id,
                extension=self.map_extensions(source=exp),
                coding=[self._map_coding(exp)],
            )
            cc_list.append(cc)

        return cc_list

    def _map_representation_extensions(self, ao):
        """Maps representation extensions from the vrs allele state using a custom extension method (_map_lse_extensions).
        """
        return self._map_lse_extensions(source=ao.state)

    def _map_literal_representation(self, ao):
        """Maps a VRS Allele object's literal sequence expression (LSE) to a FHIR MolecularDefinitionRepresentationLiteral.

        Maps:
            - vrs.state.id -> id,
            - vrs.state.sequence -> value
            -  Additional fields → extension (via custom extension mapping)
        """
        state = getattr(ao, "state", None)

        id_ = getattr(state, "id", None)
        value = self._extract_str(getattr(state, "sequence", ""))

        return MolecularDefinitionRepresentationLiteral(
            id=id_, extension=self._map_representation_extensions(ao), value=value
        )

    # ========== Location Mapping ==========

    def map_location(self, ao):
        """Maps a VRS location to a FHIR MolecularDefinitionLocation resource.

        Notes:
          - `location.id` → MolecularDefinitionLocation.id
          - `extension` is populated using a custom mapping of location extensions
          - `sequenceLocation` is mandatory and populated from `sequenceReference` or `sequence` in the location

        """
        return MolecularDefinitionLocation(
            id=ao.location.id,
            extension=self._map_location_extensions(source=ao.location),
            sequenceLocation=self._map_sequence_location(ao),
        )

    def _map_coordinate_interval(self, ao):
        """Maps a VRS allele's start and end coordinates to a FHIR CoordinateInterval using 0-based interbase indexing.
        """
        start, end = (
            Quantity(value=int(ao.location.start)),
            Quantity(value=int(ao.location.end)),
        )

        system, origin, norm_method = vrs_coordinate_interval()
        coord_system_fhir = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
            system=system, origin=origin, normalizationMethod=norm_method
        )

        return MolecularDefinitionLocationSequenceLocationCoordinateInterval(
            coordinateSystem=coord_system_fhir,
            startQuantity=start,
            endQuantity=end,
        )

    def _map_sequence_location(self, ao):
        """Maps a VRS Allele object's location to a FHIR MolecularDefinitionLocationSequenceLocation, using either `sequence` or `sequenceReference` to set the sequence context.

        Args:
            ao (object): A VRS Allele object containing a `location` with either `sequence` or `sequenceReference`.

        Raises:
            ValueError: If neither `sequence` nor `sequenceReference` is present in the location.

        Returns:
            MolecularDefinitionLocationSequenceLocation: A FHIR object containing sequence context and coordinate interval..

        """
        if getattr(ao.location, "sequence", None):
            sequence_context = self._reference_location_sequence()
        elif getattr(ao.location, "sequenceReference", None):
            sequence_context = self._reference_sequence_reference()
        else:
            raise ValueError(
                "Neither 'sequence' nor 'sequenceReference' is defined in ao.location, but one is required."
            )

        return MolecularDefinitionLocationSequenceLocation(
            sequenceContext=sequence_context,  # NOTE: This is a required field. So if sequence and sequenceReference isn't present we need to substitute it with something.
            coordinateInterval=self._map_coordinate_interval(ao),
        )

    # ========== Contained Mapping Using SequenceProfile ==========

    def map_contained(self, ao):
        """Constructs and returns a list of FHIR SequenceProfile resources to be embedded in the `contained` section of an AlleleProfile, based on the VRS Allele.locaiotion.seequence and Allele.location.sequenceReference.

        Args:
            ao (object): A VRS allele object expected to contain a `location` attribute with either a `sequence` (string) or a `sequenceReference`.

        Returns:
            list:  A list of FHIR SequenceProfile resources.

        """
        contained = []

        if getattr(ao.location, "sequence", None):
            seq = self.build_location_sequence(ao)
            if seq:
                contained.append(seq)

        if getattr(ao.location, "sequenceReference", None):
            ref_seq = self.build_location_reference_sequence(ao)
            if ref_seq:
                contained.append(ref_seq)

        return contained or None

    def build_location_sequence(self, ao):
        """Constructs a FHIR SequenceProfile resource when `location.sequence` is present on the allele object.

        Notes:
        - `moleculeType` is a required field and is derived from the Refget accession.
        - The `system` field in the coding block is currently hardcoded to the FHIR sequence-type URL.

        Args:
            ao (object): An vrs allele object containing a `location.sequence` attribute.

        Returns:
            FhirSequence: A FHIR SequenceProfile resource built from the sequence data.

        """
        sequence_id = "vrs-location-sequence"
        sequence_value = self._extract_str(getattr(ao.location, "sequence", None))

        rep_literal = MolecularDefinitionRepresentationLiteral(value=sequence_value)
        rep_sequence = MolecularDefinitionRepresentation(literal=rep_literal)
        molecule_type = self.map_mol_type(ao)

        return FhirSequence(
            id=sequence_id, moleculeType=molecule_type, representation=[rep_sequence]
        )

    def build_location_reference_sequence(self, ao):
        """Constructs a FHIR SequenceProfile resource when `location.sequenceReference` is present on the allele object.

        Args:
            ao (object): An allele object containing a `location.sequenceReference`.

        Returns:
            FhirSequence: A FHIR SequenceProfile resource built from the sequenceReference data.

        """
        source = ao.location.sequenceReference
        seqref_id = "vrs-location-sequenceReference"
        seqref_refget_accession = source.refgetAccession

        seqref_residue_alphabet = getattr(source, "residueAlphabet", None)
        seqref_sequence = self._extract_str(getattr(source, "sequence", None))
        molecule_type = self.map_mol_type(ao)
        # NOTE: Circular is currently not represented when we are going from vrs to FHIR.

        # NOTE: While only `refgetAccession` is required, if `sequence` is provided and we want to include `residueAlphabet`,
        # we must include both — since `residueAlphabet` is tied to the literal representation, which requires a sequence value.
        # If `residueAlphabet` is missing but `sequence` is present, we can infer it from `refgetAccession`.

        rep_sequence = None
        if seqref_sequence:
            if seqref_residue_alphabet is None:
                get_moltype = molecule_type.coding[0].code
                seqref_residue_alphabet = self._infer_residue_alphabet(get_moltype)
            if seqref_residue_alphabet:
                rep_sequence = MolecularDefinitionRepresentationLiteral(
                    value=seqref_sequence,
                    encoding=CodeableConcept(
                        coding=[
                            Coding(
                                system=SEQ_REF_PTRS["residueAlphabet"],
                                code=seqref_residue_alphabet,
                            )
                        ]
                    ),
                )

        representation_sequence = MolecularDefinitionRepresentation(
            code=[
                CodeableConcept(
                    coding=[
                        Coding(
                            system=SEQ_REF_PTRS["refgetAccession"],
                            code=seqref_refget_accession,
                        )
                    ]
                )
            ],
            literal=rep_sequence,
        )

        return FhirSequence(
            id=seqref_id,
            moleculeType=molecule_type,
            extension=self._map_seqref_extensions(source=source),
            representation=[representation_sequence],
        )

    def _infer_residue_alphabet(self, molecule_type):
        """Map the molecule type to the corresponding residue alphabet code ('na' or 'aa')."""
        residue_alphabet = {"dna": "na", "rna": "na", "amino acid": "aa"}
        return residue_alphabet.get(molecule_type)

    def _reference_location_sequence(self):
        """Create reference objects for location.sequence."""
        return Reference(
            type="Sequence",
            reference="#vrs-location-sequence",
            display="VRS location.sequence as contained FHIR Sequence.",
        )

    def _reference_sequence_reference(self):
        """Create reference objects for location.sequenceReference."""
        return Reference(
            type="Sequence",
            reference="#vrs-location-sequenceReference",
            display="VRS location.sequenceReference as contained FHIR Sequence",
        )
