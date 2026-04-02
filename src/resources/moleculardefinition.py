from fhir.resources import backboneelement, domainresource, fhirtypes
from fhir_core.types import BooleanType, CodeType, IntegerType
from pydantic import Field

import resources.fhirtypesextra as fhirtypesextra


class MolecularDefinition(domainresource.DomainResource):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    Representation of a molecular definition.
    """

    __resource_type__ = "MolecularDefinition"

    identifier: list[fhirtypes.IdentifierType] | None = Field(  # type: ignore
        None,
        alias="identifier",
        title="Unique ID for this particular resource",
        description="A unique identifier for this particular resource instance.",
        # The json_schema_extra dictionary includes an element_property flag set to False,
        # # indicating that this field is likely not part of the core FHIR element's structure and exists more for additional metadata.
        json_schema_extra={
            "element_property": True,
        },
    )

    description: fhirtypes.MarkdownType | None = Field(  # type: ignore
        None,
        alias="description",
        title="Description of the Molecular Definition instance",
        description="A description of the molecular definition instance in a human friendly format.",
        json_schema_extra={
            "element_property": True,
        },
    )

    moleculeType: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="moleculeType",
        title="aa | dna | rna",
        description="The type of the genomic molecule (Amino Acid, DNA, RNA).",
        json_schema_extra={
            "element_property": True,
            # note: Enum values can be used in validation,
            # but use in your own responsibilities, read official FHIR documentation.
            "enum_values": ["aa", "dna", "rna"],
        },
    )

    type: list[CodeType] | None = Field(  # type: ignore
        None,
        alias="type",
        title="	Type of the Molecular Definition entity",
        description="Description of various types of the genomic molecule other this described by the moleculeType element above.",
        json_schema_extra={
            "element_property": True,
        },
    )
    type__ext: fhirtypes.FHIRPrimitiveExtensionType | None = Field(  # type: ignore
        None, alias="_type", title="Extension field for ``type``."
    )

    location: list[fhirtypesextra.MolecularDefinitionLocationType] | None = Field(  # type: ignore
        None,
        alias="location",
        title="Location of this molecule",
        description="The molecular location of this molecule.",
        json_schema_extra={
            "element_property": True,
        },
    )

    topology: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="topology",
        title="Topology of the genomic molecule",
        description="The topology of the genomic molecule, e.g., dendrimer, array, or polyhedron.",
        json_schema_extra={
            "element_property": True,
        },
    )

    memberState: list[fhirtypes.ReferenceType] | None = Field(  # type: ignore
        None,
        alias="memberState",
        title="Member",
        description="A member or part of this molecule.",
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    representation: (
        list[fhirtypesextra.MolecularDefinitionRepresentationType] | None
    ) = Field(  # type: ignore
        None,
        alias="representation",
        title="Representation",
        description="The representation of this molecular definition, e.g., as a literal or repeated elements.",
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinition`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "meta",
            "implicitRules",
            "language",
            "text",
            "contained",
            "extension",
            "modifierExtension",
            "identifier",
            "description",
            "moleculeType",
            "type",
            "location",
            "memberState",
            "representation",
        ]


class MolecularDefinitionLocation(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The molecular location of this molecule.
    """

    __resource_type__ = "MolecularDefinitionLocation"

    sequenceLocation: (
        fhirtypesextra.MolecularDefinitionLocationSequenceLocationType | None
    ) = Field(  # type: ignore
        None,
        alias="sequenceLocation",
        title="Location of this molecule in context of a sequence",
        description="The Location of this molecule in context of a sequence.",
        json_schema_extra={
            "element_property": True,
        },
    )

    featureLocation: (
        list[fhirtypesextra.MolecularDefinitionLocationFeatureLocationType] | None
    ) = Field(  # type: ignore
        None,
        alias="featureLocation",
        title="Location in context of a feature",
        description="The location of this molecule in context of a feature.",
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocation`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "sequenceLocation",
            "featureLocation",
        ]


class MolecularDefinitionLocationSequenceLocation(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The Location of this molecule in context of a sequence.
    """

    __resource_type__ = "MolecularDefinitionLocationSequenceLocation"

    sequenceContext: fhirtypes.ReferenceType = Field(  # type: ignore
        ...,
        alias="sequenceContext",
        title="Reference sequence",
        description="The reference Sequence that contains this location.",
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    coordinateInterval: (
        fhirtypesextra.MolecularDefinitionLocationSequenceLocationCoordinateIntervalType
        | None
    ) = Field(  # type: ignore
        None,
        alias="coordinateInterval",
        title="Coordinate Interval for this location",
        description="The coordinate interval for this location.",
        json_schema_extra={
            "element_property": True,
        },
    )

    strand: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="strand",
        title="Forward or Reverse",
        description="The identification of the strand direction, i.e, forward vs reverse strand.",
        json_schema_extra={
            "element_property": True,
            # note: Enum values can be used in validation,
            # but use in your own responsibilities, read official FHIR documentation.
            "enum_values": ["Forward", "Reverse"],
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationSequenceLocation`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "sequenceContext",
            "coordinateInterval",
            "strand",
        ]


class MolecularDefinitionLocationSequenceLocationCoordinateInterval(
    backboneelement.BackboneElement
):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The coordinate interval for this location.
    """

    __resource_type__ = "MolecularDefinitionLocationSequenceLocationCoordinateInterval"

    coordinateSystem: (
        fhirtypesextra.MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType
        | None
    ) = Field(  # type: ignore
        None,
        alias="coordinateSystem",
        title="Coordinate system for this location",
        description="The coordinate system for this location.",
        json_schema_extra={
            "element_property": True,
        },
    )

    startQuantity: fhirtypes.QuantityType | None = Field(  # type: ignore
        None,
        alias="startQuantity",
        title="Start",
        description="The start of this interval.",
        json_schema_extra={
            "element_property": True,
            # Choice of Data Types. i.e sequence[x]
            "one_of_many": "start",
            "one_of_many_required": False,
        },
    )

    startRange: fhirtypes.RangeType | None = Field(  # type: ignore
        None,
        alias="startRange",
        title="Start",
        description="The start of this interval.",
        json_schema_extra={
            "element_property": True,
            # Choice of Data Types. i.e sequence[x]
            "one_of_many": "start",
            "one_of_many_required": False,
        },
    )

    endQuantity: fhirtypes.QuantityType | None = Field(  # type: ignore
        None,
        alias="endQuantity",
        title="End",
        description="The end of this interval.",
        json_schema_extra={
            "element_property": True,
            # Choice of Data Types. i.e sequence[x]
            "one_of_many": "end",
            "one_of_many_required": False,
        },
    )

    endRange: fhirtypes.RangeType | None = Field(  # type: ignore
        None,
        alias="endRange",
        title="End",
        description="The end of this interval.",
        json_schema_extra={
            "element_property": True,
            # Choice of Data Types. i.e sequence[x]
            "one_of_many": "end",
            "one_of_many_required": False,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationSequenceLocationCoordinateInterval`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "coordinateSystem",
            "startQuantity",
            "startRange",
            "endQuantity",
            "endRange",
        ]

    def get_one_of_many_fields(self) -> dict[str, list[str]]:
        """https://www.hl7.org/fhir/formats.html#choice
        A few elements have a choice of more than one data type for their content.
        All such elements have a name that takes the form nnn[x].
        The "nnn" part of the name is constant, and the "[x]" is replaced with
        the title-cased name of the type that is actually used.
        The table view shows each of these names explicitly.

        Elements that have a choice of data type cannot repeat - they must have a
        maximum cardinality of 1. When constructing an instance of an element with a
        choice of types, the authoring system must create a single element with a
        data type chosen from among the list of permitted data types.
        """
        one_of_many_fields = {
            "start": [
                "startQuantity",
                "startRange",
            ],
            "end": ["endQuantity", "endRange"],
        }
        return one_of_many_fields


class MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
    backboneelement.BackboneElement
):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The location of this molecule in context of a feature.
    """

    __resource_type__ = (
        "MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem"
    )

    system: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="system",
        title="System",
        description=("The system of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    origin: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="origin",
        title="Origin",
        description=("The origin of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    normalizationMethod: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="normalizationMethod",
        title="Normalization Method",
        description=("The normalization method of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationFeatureLocation`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "system",
            "origin",
            "normalizationMethod",
        ]


class MolecularDefinitionLocationFeatureLocation(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The location of this molecule in context of a feature.
    """

    __resource_type__ = "MolecularDefinitionLocationFeatureLocation"

    geneId: list[fhirtypes.CodeableConceptType] | None = Field(  # type: ignore
        None,
        alias="geneId",
        title="Gene Id",
        description=("The gene Id where this molecule occurs."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationFeatureLocation`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "geneId",
        ]


class MolecularDefinitionRepresentation(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The representation of this molecular definition, e.g., as a literal or repeated elements.
    """

    __resource_type__ = "MolecularDefinitionRepresentation"

    focus: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="focus",
        title="The focus of the representation",
        description=("A representation focus, e.g., reference or alternative state."),
        json_schema_extra={
            "element_property": True,
        },
    )

    code: list[fhirtypes.CodeableConceptType] | None = Field(  # type: ignore
        None,
        alias="code",
        title="A code of the representation",
        description=("A representation code."),
        json_schema_extra={
            "element_property": True,
        },
    )

    literal: fhirtypesextra.MolecularDefinitionRepresentationLiteralType | None = Field(  # type: ignore
        None,
        alias="literal",
        title="A literal representation",
        description=("A literal representation."),
        json_schema_extra={
            "element_property": True,
        },
    )

    resolvable: fhirtypes.ReferenceType | None = Field(  # type: ignore
        None,
        alias="resolvable",
        title="A resolvable representation of a molecule that optionally contains formatting in addition to the specification of the primary sequence itself",
        description=(
            "A resolvable representation of a molecule that optionally contains formatting in addition to the specification of the primary sequence itself. The sequence may be provided inline as an attached document or through a resolvable URI."
        ),
        json_schema_extra={
            "element_property": True,
        },
    )

    extracted: fhirtypesextra.MolecularDefinitionRepresentationExtractedType | None = (
        Field(  # type: ignore
            None,
            alias="extracted",
            title="A Molecular Sequence that is represented as an extracted portion of a different Molecular Sequence",
            description=(
                "A Molecular Sequence that is represented as an extracted portion of a different Molecular Sequence."
            ),
            json_schema_extra={
                "element_property": True,
            },
        )
    )

    repeated: fhirtypesextra.MolecularDefinitionRepresentationRepeatedType | None = (
        Field(  # type: ignore
            None,
            alias="repeated",
            title="A Molecular Sequence that is represented as a repeated sequence motif",
            description=(
                "A Molecular Sequence that is represented as a repeated sequence motif."
            ),
            json_schema_extra={
                "element_property": True,
            },
        )
    )

    concatenated: (
        fhirtypesextra.MolecularDefinitionRepresentationConcatenatedType | None
    ) = Field(  # type: ignore
        None,
        alias="concatenated",
        title="A Molecular Sequence that is represented as an ordered concatenation of two or more Molecular Sequences",
        description=(
            "A Molecular Sequence that is represented as an ordered concatenation of two or more Molecular Sequences."
        ),
        json_schema_extra={
            "element_property": True,
        },
    )

    relative: fhirtypesextra.MolecularDefinitionRepresentationRelativeType | None = (
        Field(  # type: ignore
            None,
            alias="relative",
            title="A Molecular Definition that is represented as an ordered series of edits on a specified starting sequence",
            description=(
                "A Molecular Definition that is represented as an ordered series of edits on a specified starting sequence."
            ),
            json_schema_extra={
                "element_property": True,
            },
        )
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentation`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "focus",
            "code",
            "literal",
            "resolvable",
            "extracted",
            "repeated",
            "concatenated",
            "relative",
        ]


class MolecularDefinitionRepresentationLiteral(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    A literal representation.
    """

    __resource_type__ = "MolecularDefinitionRepresentationLiteral"

    encoding: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="encoding",
        title="The encoding used for the expression of the primary sequence",
        description=(
            "The encoding used for the expression of the primary sequence. This defines the characters that may be used in the primary sequence and it permits the explicit inclusion/exclusion of IUPAC ambiguity codes."
        ),
        json_schema_extra={
            "element_property": True,
        },
    )

    value: fhirtypesextra.EmptyStringType = Field(  # type: ignore
        ...,
        alias="value",
        title="The primary (linear) sequence, expressed as a literal string",
        description=("The primary (linear) sequence, expressed as a literal string."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentationLiteral`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "encoding",
            "value",
        ]


class MolecularDefinitionRepresentationExtracted(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    A Molecular Sequence that is represented as an extracted portion of a different Molecular Sequence.
    """

    __resource_type__ = "MolecularDefinitionRepresentationExtracted"

    startingMolecule: fhirtypes.ReferenceType = Field(  # type: ignore
        ...,
        alias="startingMolecule",
        title="The Molecular Sequence that serves as the parent sequence, from which the intended sequence will be extracted",
        description=(
            "The Molecular Sequence that serves as the parent sequence, from which the intended sequence will be extracted."
        ),
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    coordinateInterval: (
        fhirtypesextra.MolecularDefinitionRepresentationExtractedCoordinateIntervalType
        | None
    ) = Field(  # type: ignore
        None,
        alias="coordinateInterval",
        title="Coordinate Interval for this location",
        description="The coordinate interval for this location.",
        json_schema_extra={
            "element_property": True,
        },
    )

    reverseComplement: BooleanType | None = Field(  # type: ignore
        None,
        alias="reverseComplement",
        title="A flag that indicates whether the extracted sequence should be reverse complemented",
        description=(
            "A flag that indicates whether the extracted sequence should be reverse complemented."
        ),
        json_schema_extra={"element_property": True},
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentationExtracted`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "startingMolecule",
            "coordinateInterval",
            "reverseComplement",
        ]


class MolecularDefinitionRepresentationExtractedCoordinateInterval(
    backboneelement.BackboneElement
):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The coordinate interval for this location.
    """

    __resource_type__ = "MolecularDefinitionRepresentationExtractedCoordinateInterval"

    coordinateSystem: (
        fhirtypesextra.MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystemType
        | None
    ) = Field(  # type: ignore
        None,
        alias="coordinateSystem",
        title="The coordinate system used to define the interval that defines the subsequence to be extracted. Coordinate systems are usually 0- or 1-based",
        description=(
            "The coordinate system used to define the interval that defines the subsequence to be extracted. Coordinate systems are usually 0- or 1-based."
        ),
        json_schema_extra={"element_property": True},
    )

    start: IntegerType = Field(  # type: ignore
        ...,
        alias="start",
        title="The start coordinate (on the parent sequence) of the interval that defines the subsequence to be extracted",
        description=(
            "The start coordinate (on the parent sequence) of the interval that defines the subsequence to be extracted."
        ),
        json_schema_extra={"element_property": True},
    )

    end: IntegerType = Field(  # type: ignore
        ...,
        alias="end",
        title="The end coordinate (on the parent sequence) of the interval that defines the subsequence to be extracted",
        description=(
            "The end coordinate (on the parent sequence) of the interval that defines the subsequence to be extracted."
        ),
        json_schema_extra={"element_property": True},
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationSequenceLocationCoordinateInterval`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "coordinateSystem",
            "start",
            "end",
        ]


class MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystem(
    backboneelement.BackboneElement
):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The location of this molecule in context of a feature.
    """

    __resource_type__ = (
        "MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystem"
    )

    system: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="system",
        title="System",
        description=("The system of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    origin: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="origin",
        title="Origin",
        description=("The origin of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    normalizationMethod: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="normalizationMethod",
        title="Normalization Method",
        description=("The normalization method of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationFeatureLocation`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "system",
            "origin",
            "normalizationMethod",
        ]


class MolecularDefinitionRepresentationRepeated(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    A Molecular Sequence that is represented as a repeated sequence motif.
    """

    __resource_type__ = "MolecularDefinitionRepresentationRepeated"

    sequenceMotif: fhirtypes.ReferenceType = Field(  # type: ignore
        ...,
        alias="sequenceMotif",
        title="The sequence that defines the repeated motif",
        description=("The sequence that defines the repeated motif."),
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    copyCount: IntegerType = Field(  # type: ignore
        ...,
        alias="copyCount",
        title="The number of repeats (copies) of the sequence motif",
        description=("The number of repeats (copies) of the sequence motif."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentationRepeated`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "sequenceMotif",
            "copyCount",
        ]


class MolecularDefinitionRepresentationConcatenated(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    A Molecular Sequence that is represented as an ordered concatenation of two or more Molecular Sequences.
    """

    __resource_type__ = "MolecularDefinitionRepresentationConcatenated"

    sequenceElement: (
        list[
            fhirtypesextra.MolecularDefinitionRepresentationConcatenatedSequenceElementType
        ]
        | None
    ) = Field(  # type: ignore
        None,
        alias="sequenceElement",
        title="One element of a concatenated Molecular Sequence",
        description=("One element of a concatenated Molecular Sequence."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentationConcatenated`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "sequenceElement",
        ]


class MolecularDefinitionRepresentationConcatenatedSequenceElement(
    backboneelement.BackboneElement
):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    One element of a concatenated Molecular Sequence.
    """

    __resource_type__ = "MolecularDefinitionRepresentationConcatenatedSequenceElement"

    sequence: fhirtypes.ReferenceType = Field(  # type: ignore
        ...,
        alias="sequence",
        title="The Molecular Sequence corresponding to this element",
        description=("The Molecular Sequence corresponding to this element."),
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    ordinalIndex: IntegerType = Field(  # type: ignore
        ...,
        alias="ordinalIndex",
        title="The ordinal position of this sequence element within the concatenated Molecular Sequence",
        description=(
            "The ordinal position of this sequence element within the concatenated Molecular Sequence."
        ),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentationConcatenatedSequenceElement`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "sequence",
            "ordinalIndex",
        ]


class MolecularDefinitionRepresentationRelative(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    A Molecular Definition that is represented as an ordered series of edits on a specified starting sequence.
    """

    __resource_type__ = "MolecularDefinitionRepresentationRelative"

    startingMolecule: fhirtypes.ReferenceType = Field(  # type: ignore
        ...,
        alias="startingMolecule",
        title="The Molecular Sequence that serves as the starting sequence, on which edits will be applied",
        description=(
            "The Molecular Sequence that serves as the starting sequence, on which edits will be applied."
        ),
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    edit: (
        list[fhirtypesextra.MolecularDefinitionRepresentationRelativeEditType] | None
    ) = Field(  # type: ignore
        None,
        alias="edit",
        title="An edit (change) made to a sequence",
        description=("An edit (change) made to a sequence."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentationRelative`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "startingMolecule",
            "edit",
        ]


class MolecularDefinitionRepresentationRelativeEdit(backboneelement.BackboneElement):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    An edit (change) made to a sequence.
    """

    __resource_type__ = "MolecularDefinitionRepresentationRelativeEdit"

    editOrder: IntegerType | None = Field(  # type: ignore
        None,
        alias="editOrder",
        title="The order of this edit, relative to other edits on the starting sequence",
        description=(
            "The order of this edit, relative to other edits on the starting sequence."
        ),
        json_schema_extra={
            "element_property": True,
        },
    )

    coordinateInterval: (
        fhirtypesextra.MolecularDefinitionRepresentationRelativeEditCoordinateIntervalType
        | None
    ) = Field(  # type: ignore
        None,
        alias="coordinateInterval",
        title="Coordinate Interval for this location",
        description="The coordinate interval for this location.",
        json_schema_extra={
            "element_property": True,
        },
    )

    replacementMolecule: fhirtypes.ReferenceType = Field(  # type: ignore
        ...,
        alias="replacementMolecule",
        title="The sequence that defines the replacement sequence used in the edit operation",
        description=(
            "The sequence that defines the replacement sequence used in the edit operation."
        ),
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    replacedMolecule: fhirtypes.ReferenceType | None = Field(  # type: ignore
        None,
        alias="replacedMolecule",
        title="...",
        description=None,
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["MolecularDefinition"],
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionRepresentationRelativeEdit`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "editOrder",
            "coordinateInterval",
            "replacementMolecule",
            "replacedMolecule",
        ]


class MolecularDefinitionRepresentationRelativeEditCoordinateInterval(
    backboneelement.BackboneElement
):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The coordinate interval for this location.
    """

    __resource_type__ = (
        "MolecularDefinitionRepresentationRelativeEditCoordinateInterval"
    )

    coordinateSystem: (
        fhirtypesextra.MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystemType
        | None
    ) = Field(  # type: ignore
        None,
        alias="coordinateSystem",
        title="The coordinate system used to define the edited intervals on the starting sequence. Coordinate systems are usually 0- or 1-based",
        description=(
            "The coordinate system used to define the edited intervals on the starting sequence. Coordinate systems are usually 0- or 1-based."
        ),
        json_schema_extra={
            "element_property": True,
        },
    )

    start: IntegerType | None = Field(  # type: ignore
        None,
        alias="start",
        title="The start coordinate of the interval that will be edited",
        description=("The start coordinate of the interval that will be edited."),
        json_schema_extra={
            "element_property": True,
        },
    )

    end: IntegerType | None = Field(  # type: ignore
        None,
        alias="end",
        title="The end coordinate of the interval that will be edited",
        description=("The end coordinate of the interval that will be edited."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationSequenceLocationCoordinateInterval`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "coordinateSystem",
            "start",
            "end",
        ]


class MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystem(
    backboneelement.BackboneElement
):
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    The location of this molecule in context of a feature.
    """

    __resource_type__ = "MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystem"

    system: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="system",
        title="System",
        description=("The system of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    origin: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="origin",
        title="Origin",
        description=("The origin of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    normalizationMethod: fhirtypes.CodeableConceptType | None = Field(  # type: ignore
        None,
        alias="normalizationMethod",
        title="Normalization Method",
        description=("The normalization method of the specified coordinate."),
        json_schema_extra={
            "element_property": True,
        },
    )

    @classmethod
    def elements_sequence(cls):
        """Returning all elements names from
        ``MolecularDefinitionLocationFeatureLocation`` according specification,
        with preserving original sequence order.
        """
        return [
            "id",
            "extension",
            "modifierExtension",
            "system",
            "origin",
            "normalizationMethod",
        ]
