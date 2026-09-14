import csv

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


# Модель для пед патронаж розкладу для одного уроку
class IndividualHomeBasedSubjectSchedule(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    subject: str = Field(alias="Subject")
    teacher: str = Field(alias="Teacher")
    room: Optional[str] = Field(alias="Room")
    day_of_week: str = Field(alias="DayOfWeek")
    lesson_number: int = Field(alias="LessonNumber")
    week_number: int = Field(alias="WeekNumber")
    hours_per_week: float = Field(alias="HoursPerWeek")
    start_date: str = Field(alias="StartDate", default="01.09.2026")


def get_schedule(csv_path: str) -> list[IndividualHomeBasedSubjectSchedule]:
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        students = [IndividualHomeBasedSubjectSchedule.model_validate(row) for row in reader]

    return students
