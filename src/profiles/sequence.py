from typing import ClassVar

from fhir.resources import fhirtypes
from pydantic import model_validator

import resources.fhirtypesextra as fhirtypesextra
from exceptions.fhir import ElementNotAllowedError, InvalidMoleculeTypeError
from resources.moleculardefinition import MolecularDefinition


class Sequence(MolecularDefinition):
    """FHIR Sequence Profile

    Args:
        MolecularDefinition (MolecularDefinition): The base class for molecular definitions.

    Raises:
        ValueError: If `memberState` or `location` is included in the profile.

    Returns:
        Sequence: An instance of the Sequence class.

    """

    memberState: ClassVar[fhirtypes.ReferenceType | None]  # type: ignore
    location: ClassVar[fhirtypesextra.MolecularDefinitionLocationType | None]  # type: ignore

    # Combined validator to exclude both `memberState` and `location` during validation
    @model_validator(mode="before")
    def validate_exclusions(cls, data):
        if isinstance(data, dict):
            for field in ["memberState", "location"]:
                if field in data:
                    raise ElementNotAllowedError(
                        f"`{field}` is not allowed in Sequence."
                    )
        return data

    @model_validator(mode="after")
    def validate_moleculeType(self):
        """Validates that the 'moleculeType' field is present and contains exactly one item.

        Args:
            values (BaseModel): The validated model instance.

        Raises:
            InvalidMoleculeTypeError: If 'moleculeType' is missing or empty.

        Returns:
            BaseModel: The validated model instance if the check passes.

        """
        mt = getattr(self, "moleculeType", None)

        if not mt:
            raise InvalidMoleculeTypeError(
                "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Allele."
            )
        if isinstance(mt, list):
            if len(mt) != 1:
                raise InvalidMoleculeTypeError(
                    "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Allele."
                )
        else:
            try:
                if not mt.model_dump(exclude_unset=True):
                    raise InvalidMoleculeTypeError(
                        "The `moleculeType` field must contain exactly one item. `moleculeType` has a 1..1 cardinality for Allele."
                    )
            except AttributeError:
                pass

        return self

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
            "moleculeType",
            "representation",
        ]
