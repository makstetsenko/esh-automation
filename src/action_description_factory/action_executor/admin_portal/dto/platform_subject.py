import csv
import pathlib

from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, Field


class PlatformSubject(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    name: str = Field(serialization_alias="Name")
    class_year: int = Field(serialization_alias="Class year")


def write_to_csv(subjects: list[PlatformSubject], path: pathlib.Path) -> None:
    fieldnames = [field.serialization_alias or name for name, field in PlatformSubject.model_fields.items()]

    with open(path.as_posix(), "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerows(x.model_dump(by_alias=True) for x in subjects)
