import csv
import pathlib

from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, Field


class PlatformTeacher(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    first_name: str = Field(serialization_alias="First name")
    last_name: str = Field(serialization_alias="Last name")
    middle_name: str = Field(serialization_alias="Middle name")
    original_name_on_platform: str = Field(serialization_alias="Original full name on platform")


def write_to_csv(teachers: list[PlatformTeacher], path: pathlib.Path) -> None:
    fieldnames = [field.serialization_alias or name for name, field in PlatformTeacher.model_fields.items()]

    with open(path.as_posix(), "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerows(student.model_dump(by_alias=True) for student in teachers)
