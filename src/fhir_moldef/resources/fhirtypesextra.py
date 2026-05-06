from __future__ import annotations as _annotations

import dataclasses
from typing import Annotated

from fhir_core.types import String, create_fhir_type


@dataclasses.dataclass(frozen=True)
class StringAllowEmpty(String):
    """FHIR String type that allows empty strings (regex updated automatically)."""

    allow_empty_str = True


EmptyStringType = Annotated[str, StringAllowEmpty()]

MolecularDefinitionType = create_fhir_type(
    "MolecularDefinitionType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinition",
)

MolecularDefinitionLocationType = create_fhir_type(
    "MolecularDefinitionLocationType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionLocation",
)

MolecularDefinitionLocationSequenceLocationType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionLocationSequenceLocation",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateInterval",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem",
)

MolecularDefinitionLocationFeatureLocationType = create_fhir_type(
    "MolecularDefinitionLocationFeatureLocationType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionLocationFeatureLocation",
)

MolecularDefinitionRepresentationType = create_fhir_type(
    "MolecularDefinitionRepresentationType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentation",
)

MolecularDefinitionRepresentationLiteralType = create_fhir_type(
    "MolecularDefinitionRepresentationLiteralType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationLiteral",
)

MolecularDefinitionRepresentationExtractedType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationExtracted",
)

MolecularDefinitionRepresentationExtractedCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedCoordinateIntervalType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationExtractedCoordinateInterval",
)

MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystemType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystem",
)

MolecularDefinitionRepresentationRepeatedType = create_fhir_type(
    "MolecularDefinitionRepresentationRepeatedType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationRepeated",
)

MolecularDefinitionRepresentationConcatenatedType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationConcatenated",
)

MolecularDefinitionRepresentationConcatenatedSequenceElementType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedSequenceElementType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationConcatenatedSequenceElement",
)

MolecularDefinitionRepresentationRelativeType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationRelative",
)

MolecularDefinitionRepresentationRelativeEditType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationRelativeEdit",
)

MolecularDefinitionRepresentationRelativeEditCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditCoordinateIntervalType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationRelativeEditCoordinateInterval",
)

MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystemType",
    "fhir_moldef.resources.moleculardefinition.MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystem",
)

__all__ = [
    # New MolecularDefinition Values
    "EmptyStringType",
    "MolecularDefinitionType",
    "MolecularDefinitionLocationType",
    "MolecularDefinitionLocationSequenceLocationType",
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalType",
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType",
    "MolecularDefinitionLocationFeatureLocationType",
    "MolecularDefinitionRepresentationType",
    "MolecularDefinitionRepresentationLiteralType",
    "MolecularDefinitionRepresentationExtractedType",
    "MolecularDefinitionRepresentationExtractedCoordinateIntervalType",
    "MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystemType",
    "MolecularDefinitionRepresentationRepeatedType",
    "MolecularDefinitionRepresentationConcatenatedType",
    "MolecularDefinitionRepresentationConcatenatedSequenceElementType",
    "MolecularDefinitionRepresentationRelativeType",
    "MolecularDefinitionRepresentationRelativeEditType",
    "MolecularDefinitionRepresentationRelativeEditCoordinateIntervalType",
    "MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystemType",
]
