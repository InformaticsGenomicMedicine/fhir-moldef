from ga4gh.core.models import Extension
from ga4gh.vrs.models import (
    Allele,
    Expression,
    LiteralSequenceExpression,
    SequenceLocation,
    SequenceReference,
    sequenceString,
)

from translators.constants.vrs_json_pointers import allele_identifiers as ALLELE_PTRS
from translators.constants.vrs_json_pointers import extension_identifiers as EXT_PTRS
from translators.constants.vrs_json_pointers import (
    literal_sequence_expression_identifiers as LSE,
)
from translators.constants.vrs_json_pointers import (
    sequence_location_identifiers as SEQ_LOC,
)
from translators.constants.vrs_json_pointers import (
    sequence_reference_identifiers as SEQ_REF,
)


class FhirToVrsAlleleTranslator:
    """Translate a FHIR Allele Profile into a GA4GH VRS Allele, providing full translation."""
    def translate(self, ao):
        """Converts a FHIR Allele Profile object into a fully populated VRS 2.0 Allele object.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object to be translated into a VRS 2.0 Allele.

        Returns:
            Allele: A fully populated VRS 2.0 Allele object.
        """
        meta = self._extract_allele_metadata(ao)
        return Allele(
            id=meta["id"],
            name=meta["name"],
            type="Allele",
            aliases=meta["aliases"],
            digest=meta["digest"],
            description=ao.description,
            expressions=self._map_expressions(ao),
            location=self._map_sequence_location(ao),
            state=self._map_literal_sequence_expression(ao),
        )

    # ========== Meta Data Mapping ==========

    def _extract_allele_metadata(self, ao):
        """Parses the `identifier` fields of a FHIR Allele Profile to extract metadata.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object to be translated into a VRS 2.0 Allele.

        Returns:
            dict: A dictionary with extracted metadata keys:
            - 'id' (str): A unique identifier for the allele.
            - 'name' (str): A human-readable label for the allele.
            - 'digest' (str): A computed digest or hash of the allele.
            - 'aliases' (list of str): A list of alternate identifiers for the allele.
        """
        values = {"aliases": []}

        for identifier in ao.identifier:
            for key, system_uri in ALLELE_PTRS.items():
                if system_uri in identifier.system:
                    if key == "aliases":
                        values.setdefault("aliases", []).append(identifier.value)
                    else:
                        values[key] = identifier.value or None

        for key in ["id", "name", "digest"]:
            values.setdefault(key, None)

        if not values["aliases"]:
            values["aliases"] = None

        return values

    # ========== Expressions Mapping ==========

    def _map_expressions(self, ao):
        """Maps the expression information from a FHIR Allele Profile to a VRS Expression.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object to be translated into a VRS 2.0 Allele.

        Returns:
            list[Expression]: A list containing a single VRS `Expression` object with
            extracted syntax, value, version, and optional extensions.
        """

        if not ao.representation[0].code:
            return None

        expression_list = []
        for code in ao.representation[0].code:
            extensions = (
                self._extract_nested_extensions(code.extension)
                if code.extension
                else None
            )
            for coding in code.coding:
                exp = Expression(
                    id=code.id,
                    syntax=coding.display,
                    value=coding.code,
                    syntax_version=coding.version,
                    extensions=extensions,
                )
                expression_list.append(exp)

        return expression_list

    # ========== Sequence Location Mapping ==========

    def _map_sequence_location(self, ao):
        """Maps sequence location data from a FHIR Allele Profile to a VRS SequenceLocation object.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object to be translated into a VRS 2.0 Allele.

        Returns:
            SequenceLocation: A VRS 2.0 `SequenceLocation` object with sequence reference, coordinates,
        literal sequence, and mapped extensions.
        """
        start, end = self._get_coordinates(ao)
        location_data = self._extract_location_fields(ao.location)
        sequence, _ = self._extract_contained_sequences(ao)
        literal_sequence = self._extract_contained_sequence_value(sequence)
        mapped_extensions = self._map_extension(location_data["extensions"])

        return SequenceLocation(
            id=location_data["id"],
            name=location_data["name"],
            description=location_data["description"],
            extensions=mapped_extensions,
            digest=location_data["digest"],
            aliases=location_data["aliases"],
            type="SequenceLocation",
            sequenceReference=self._map_sequence_reference(ao),
            start=start,
            end=end,
            sequence=literal_sequence,  # coming from contained value
        )

    def _get_coordinates(self, ao):
        """Extracts start and end coordinate values from a FHIR Allele Profile.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object to be translated into a VRS 2.0 Allele.

        Returns:
            tuple[int, int]: A tuple containing the start and end coordinates as integers.
        """
        interval = ao.location[0].sequenceLocation.coordinateInterval
        return interval.startQuantity.value, interval.endQuantity.value

    def _map_sequence_reference(self, ao):
        """Maps sequence reference data from a FHIR Allele Profile to a VRS SequenceReference object.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object to be translated into a VRS 2.0 Allele.

        Returns:
            SequenceReference: A fully populated VRS 2.0 `SequenceReference` object including identifiers, sequence string, and relevant extensions.
        """
        _, sequence_reference = self._extract_contained_sequences(ao)
        ref_seq_data = self._extract_reference_sequence_fields(sequence_reference)

        mapped_extensions = self._map_extension(ref_seq_data["extensions"])

        refget_accession, molecule_type, residue_alphabet, literal_sequence = (
            self._extract_contained_sequence_reference_details(sequence_reference)
        )

        return SequenceReference(
            id=ref_seq_data["id"],
            name=ref_seq_data["name"],
            description=ref_seq_data["description"],
            aliases=ref_seq_data["aliases"],
            extensions=mapped_extensions,
            refgetAccession=refget_accession,
            residueAlphabet=residue_alphabet,
            moleculeType=self._validate_molecule_type(molecule_type),
            # TODO/NOTE: No place to put this in the fhir schema/ so we can just hard code it.
            # circular=False,
            sequence=literal_sequence,
        )

    # ========== Contained Resource Parsing ==========
    def _extract_contained_sequences(self, ao):
        """Extracts sequence and sequenceReference resources from a FHIR Allele Profile's contained list.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object that includes `contained` resources.

        Raises:
            ValueError: If either required contained resource is missing.

        Returns:
            tuple: A tuple `(seq, seq_ref)` where:
            - seq: The contained sequence object (e.g., for use in SequenceLocation).
            - seq_ref: The contained sequenceReference object (e.g., for use in SequenceReference).
        """
        seq = None
        seq_ref = None

        for resource in ao.contained:
            if resource.id == "vrs-location-sequence":
                seq = resource
            elif resource.id == "vrs-location-sequenceReference":
                seq_ref = resource

        if seq is None and seq_ref is None:
            raise ValueError(
                "Both 'vrs-location-sequence' and 'vrs-location-sequenceReference' are missing."
            )

        return seq, seq_ref

    def _extract_contained_sequence_value(self, sequence):
        """Extracts the literal sequence string from a contained FHIR sequence resource.

        Args:
            sequence (object): A FHIR `contained` sequence resource with a
            `representation.literal.value` field.

        Returns:
            str: The literal sequence string (e.g., nucleotide bases or amino acid residues).
        """
        if sequence is None:
            return None
        return sequenceString(sequence.representation[0].literal.value)

    def _extract_contained_sequence_reference_details(self, seq_ref):
        """Extracts sequence reference metadata from a contained sequenceReference resource.

        Args:
            seq_ref (object): A FHIR `contained` resource representing a sequenceReference.

        Returns:
        tuple[str, str, str, str]: A tuple containing:
            - refgetAccession (str): A RefGet digest identifier for the sequence.
            - moleculeType (str): The type of molecule ("genomic", "RNA", "mRNA", or "protein").
            - residueAlphabet (str): The encoding alphabet for the sequence ("na" or "aa").
            - sequence (str): A literal representation of the sequence.
        """
        # These are always present
        representation = seq_ref.representation[0]
        refget_accession = representation.code[0].coding[0].code
        molecule_type = seq_ref.moleculeType.coding[0].code

        residue_alphabet = None
        sequence = None

        if hasattr(representation, "literal") and hasattr(
            representation.literal, "encoding"
        ):
            residue_alphabet = representation.literal.encoding.coding[0].code
            sequence = sequenceString(representation.literal.value)

        if residue_alphabet is None:
            residue_alphabet = self._infer_residue_alphabet(molecule_type)

        return refget_accession, molecule_type, residue_alphabet, sequence

    def _infer_residue_alphabet(self, molecule_type):
        """Infers the residue alphabet category based on the moleculeType attribute.

        Args:
            molecule_type (str): The type of molecule (e.g., 'DNA', 'RNA', or 'protein').

        Returns:
            str or None: Returns 'na' for nucleic acids (DNA or RNA), 'aa' for proteins,
        or None if the molecule type is unrecognized.
        """
        residue_alphabet = {"dna": "na", "rna": "na", "amino acid": "aa"}
        return residue_alphabet.get(molecule_type)

    def _validate_molecule_type(self, molecule_type):
        """Validates and converts a FHIR molecule type to its VRS-compliant equivalent.

        Args:
            molecule_type (str): A molecule type from a FHIR resource. Expected values are 'dna', 'rna', or 'protein'
              (case-insensitive).

        Raises:
            ValueError: If the input molecule type is not one of the expected FHIR types.

        Returns:
            str: A molecule type string compatible with VRS. One of 'genomic', 'RNA', or 'protein'.
        """
        mapped_mol_type = {"dna": "genomic", "rna": "RNA", "amino acid": "protein"}

        molecule_type = molecule_type.lower()

        if molecule_type in mapped_mol_type:
            return mapped_mol_type[molecule_type]

        raise ValueError(
            f"Unsupported moleculeType: '{molecule_type}'. Expected one of: dna, rna, amino acid."
        )

    # ========== Literal Sequence Expression Mapping ==========

    def _map_literal_sequence_expression(self, ao):
        """Maps a FHIR literal sequence expression to a VRS LiteralSequenceExpression object.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object that includes one or more
            literal sequence representations.

        Returns:
            LiteralSequenceExpression: A VRS-compliant object that encapsulates a literal
        sequence and its associated metadata and extensions.
        """
        lse_data = self._extract_literal_fields(ao.representation)
        mapped_extensions = self._map_extension(lse_data["extensions"])

        return LiteralSequenceExpression(
            id=lse_data["id"],
            name=lse_data["name"],
            description=lse_data["description"],
            aliases=lse_data["aliases"],
            extensions=mapped_extensions,
            sequence=sequenceString(self._get_literal_sequence_value(ao)),
        )

    def _get_literal_sequence_value(self, ao):
        """Retrieves the literal sequence string from a FHIR Allele Profile.

        Args:
            ao (AlleleObject): A FHIR Allele Profile object with at least one literal representation.

        Returns:
            str: The literal sequence string (e.g., a DNA, RNA, or protein sequence).
        """
        return ao.representation[0].literal.value

    # ========== Extension Mapping ==========
    def _map_extension(self, ext_list):
        """Recursively maps a list of extension dictionaries into Extension objects.

        Args:
            ext_list (list[dict]): A list of extension dictionaries, each with keys such as
            'id', 'name', 'value', 'description', and optionally 'extensions' (for nesting).

        Returns:
            list[Extension] | None: A list of `Extension` objects representing the structured extensions, or `None` if the input list is empty or None.
        """
        extension_objects = []
        for ext in ext_list:
            exts = ext.get("extensions")
            sub_extensions = self._map_extension(exts) if exts else None
            extension_objects.append(
                Extension(
                    id=ext.get("id"),
                    name=ext.get("name"),
                    value=ext.get("value"),
                    description=ext.get("description"),
                    extensions=sub_extensions,
                )
            )
        return extension_objects or None

    def _extract_location_fields(self, location_obj):
        """Extracts structured metadata from a list of FHIR location objects.

        Args:
            llocation_obj (list): A list of FHIR location objects, each potentially
            containing extensions that define metadata fields.

        Returns:
            list[dict]: A list of dictionaries, one per location object, each containing: id,name, description, digest, aliases ,extensions
        """

        for loc in location_obj:
            result = {
                "id": getattr(loc, "id", None),
                "name": None,
                "description": None,
                "digest": None,
                "aliases": [],
                "extensions": [],
            }

            for ext in getattr(loc, "extension", None) or []:
                url = getattr(ext, "url", "") or ""
                val = self._get_extension_value(ext)

                if SEQ_LOC["name"] in url:
                    result["name"] = val
                elif SEQ_LOC["description"] in url:
                    result["description"] = val
                elif SEQ_LOC["digest"] in url:
                    result["digest"] = val
                elif SEQ_LOC["aliases"] in url:
                    result["aliases"].append(val)
                elif ext.extension:
                    nested = self._extract_nested_extensions([ext])
                    if nested:
                        result["extensions"].extend(nested)

            if not result["aliases"]:
                result["aliases"] = None

        return result

    def _extract_literal_fields(self, representation_obj):
        """Extracts metadata fields from FHIR literal sequence representations.

        Args:
            representation_obj (list): A list of FHIR representation objects, each
            potentially containing a `literal` element with structured metadata
            in extensions.

        Returns:
           dict: A dictionary representing the last literal sequence expression found.
        Includes the fields: id, name, description, aliases, and extensions.
        """

        for rep in representation_obj:
            literal = getattr(rep, "literal", None)
            if literal is None:
                continue

            result = {
                "id": getattr(rep.literal, "id", None),
                "name": None,
                "description": None,
                "aliases": [],
                "extensions": [],
            }

            for ext in getattr(literal, "extension", None) or []:
                url = getattr(ext, "url", "") or ""
                val = self._get_extension_value(ext)

                if LSE["name"] in url:
                    result["name"] = val
                elif LSE["description"] in url:
                    result["description"] = val
                elif LSE["aliases"] in url:
                    result["aliases"].append(val)
                elif ext.extension:
                    nested = self._extract_nested_extensions([ext])
                    if nested:
                        result["extensions"].extend(nested)

        if not result["aliases"]:
            result["aliases"] = None

        return result

    def _extract_reference_sequence_fields(self, ref_seq):
        """Extract metadata fields from a FHIR `sequenceReference` resource.

        Args:
            ref_seq (object): A FHIR resource object representing a contained `sequenceReference`.

        Returns:
           dict: A dictionary containing the extracted fields: id, name, description,
            digest, aliases, and extensions.
        """
        result = {
            "id": None,
            "name": None,
            "description": None,
            "digest": None,
            "aliases": [],
            "extensions": [],
        }

        for ext in getattr(ref_seq, "extension", None) or []:
            url = getattr(ext, "url", "") or ""
            val = self._get_extension_value(ext)

            if SEQ_REF["id"] in url:
                result["id"] = val
            if SEQ_REF["name"] in url:
                result["name"] = val
            elif SEQ_REF["description"] in url:
                result["description"] = val
            elif SEQ_REF["aliases"] in url:
                result["aliases"].append(val)
            elif hasattr(ext, "extension"):
                nested = self._extract_nested_extensions([ext])
                if nested:
                    result["extensions"].extend(nested)

        if not result["aliases"]:
            result["aliases"] = None

        return result

    def _extract_nested_extensions(self, extension_list):
        """Recursively extracts structured metadata from nested FHIR extensions.

        Args:
            extension_list (list): A list of FHIR extension objects.

        Returns:
            list[dict]: A list of dictionaries, each representing a parsed extension with: id, name, value description, extensions
        """
        results = []

        for ext in extension_list:
            ext_id = getattr(ext, "id", None)
            result = {"id": ext_id}
            inner_extensions = getattr(ext, "extension", [])

            if (
                inner_extensions is None
            ):  # to avoid extensions that are none. Prefer to find a better solution.
                continue

            nested_ext = []

            for inner_ext in inner_extensions:
                inner_url = getattr(inner_ext, "url", "") or ""
                inner_val = self._get_extension_value(inner_ext)

                if EXT_PTRS["name"] in inner_url:
                    result["name"] = inner_val
                elif EXT_PTRS["value"] in inner_url:
                    result["value"] = inner_val
                elif EXT_PTRS["description"] in inner_url:
                    result["description"] = inner_val
                elif hasattr(inner_ext, "extension"):
                    nested_ext.extend(self._extract_nested_extensions([inner_ext]))

            if nested_ext:
                result["extensions"] = nested_ext

            results.append(result)

        return results

    def _get_extension_value(self, ext):
        """Extracts a supported value from a FHIR Extension.

        Checks for the following extension value types, in order:
        - valueString (string)
        - valueBoolean (boolean)
        - valueDecimal (decimal)
        - valueInteger (integer)

        Args:
            ext (obj): A FHIR Extension object potentially containing one of the supported value fields.

        Returns:
            Union[str, bool, float, None]: The first available value found, or None if none are set.
        """
        for attr in ["valueString", "valueBoolean", "valueDecimal", "valueInteger"]:
            val = getattr(ext, attr, None)
            if val is not None:
                return val
        return None
