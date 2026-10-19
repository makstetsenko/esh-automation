import csv
import pathlib

from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, Field


class StudentDistribution(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        validate_by_name=True
    )

    student_surname: str = Field(validation_alias="Student surname", serialization_alias="Student surname")
    group_name: str = Field(validation_alias="Group name", serialization_alias="Group name")


def read_students_from_csv(path: pathlib.Path) -> list[StudentDistribution]:
    with open(path.as_posix(), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        result = [StudentDistribution.model_validate(row) for row in reader]

    return result
