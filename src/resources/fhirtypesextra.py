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
    "resources.moleculardefinition.MolecularDefinition",
)

MolecularDefinitionLocationType = create_fhir_type(
    "MolecularDefinitionLocationType",
    "resources.moleculardefinition.MolecularDefinitionLocation",
)

MolecularDefinitionLocationSequenceLocationType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationType",
    "resources.moleculardefinition.MolecularDefinitionLocationSequenceLocation",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalType",
    "resources.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateInterval",
)

MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystemType",
    "resources.moleculardefinition.MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem",
)

MolecularDefinitionLocationFeatureLocationType = create_fhir_type(
    "MolecularDefinitionLocationFeatureLocationType",
    "resources.moleculardefinition.MolecularDefinitionLocationFeatureLocation",
)

MolecularDefinitionRepresentationType = create_fhir_type(
    "MolecularDefinitionRepresentationType",
    "resources.moleculardefinition.MolecularDefinitionRepresentation",
)

MolecularDefinitionRepresentationLiteralType = create_fhir_type(
    "MolecularDefinitionRepresentationLiteralType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationLiteral",
)

MolecularDefinitionRepresentationExtractedType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationExtracted",
)

MolecularDefinitionRepresentationExtractedCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedCoordinateIntervalType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationExtractedCoordinateInterval",
)

MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystemType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationExtractedCoordinateIntervalCoordinateSystem",
)

MolecularDefinitionRepresentationRepeatedType = create_fhir_type(
    "MolecularDefinitionRepresentationRepeatedType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationRepeated",
)

MolecularDefinitionRepresentationConcatenatedType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationConcatenated",
)

MolecularDefinitionRepresentationConcatenatedSequenceElementType = create_fhir_type(
    "MolecularDefinitionRepresentationConcatenatedSequenceElementType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationConcatenatedSequenceElement",
)

MolecularDefinitionRepresentationRelativeType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationRelative",
)

MolecularDefinitionRepresentationRelativeEditType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationRelativeEdit",
)

MolecularDefinitionRepresentationRelativeEditCoordinateIntervalType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditCoordinateIntervalType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationRelativeEditCoordinateInterval",
)

MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystemType = create_fhir_type(
    "MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystemType",
    "resources.moleculardefinition.MolecularDefinitionRepresentationRelativeEditCoordinateIntervalCoordinateSystem",
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
