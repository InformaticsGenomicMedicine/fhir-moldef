# NOTE: This Profile is a work in progress. Profile should not be used. 
from typing import ClassVar

from fhir.resources import fhirtypes
from pydantic import Field, model_validator

import resources.fhirtypesextra as fhirtypesextra
from exceptions.fhir import ElementNotAllowedError, InvalidTypeError
from resources.moleculardefinition import MolecularDefinition


class Genotype(MolecularDefinition):
    location: ClassVar[fhirtypesextra.MolecularDefinitionLocationType | None]  # type: ignore
    representation: ClassVar[
        fhirtypesextra.MolecularDefinitionRepresentationType | None
    ]  # type: ignore

    memberState: list[fhirtypes.ReferenceType] | None = Field(  # type: ignore
        None,
        alias="memberState",
        title="Member",
        description="A member or part of this molecule.",
        json_schema_extra={
            "element_property": True,
            # note: Listed Resource Type(s) should be allowed as Reference.
            "enum_reference_types": ["Allele", "Haplotype"],
        },
    )

    @model_validator(mode="before")
    def validate_exclusions(cls, data):
        for field in ["location", "representation"]:
            if field in data and data[field] is not None:
                raise ElementNotAllowedError(f"`{field}` is not allowed in Genotype.")
        return data

    @model_validator(mode="after")
    def validate_type(self):
        if not self.type or not self.type.model_dump(exclude_unset=True):
            raise InvalidTypeError(
                "The `type` field must contain exactly one item. `type` has a 1..1 cardinality for Genotype."
            )
        return self
