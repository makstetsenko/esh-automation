# Report that represents Teacher and his subjects and his classes


import csv
import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel, ConfigDict

from src.admin_portal.actions.shared import home_page
from src.admin_portal.actions.shared.organization_staff import staff_list_page

logger = logging.getLogger(__name__)


class SubjectInfo(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    name: str
    hours_per_week: float
    classes: list[str]


def write_to_csv(data: list[SubjectInfo], path: pathlib.Path) -> None:
    fieldnames = [field.serialization_alias or name for name, field in SubjectInfo.model_fields.items()]

    with open(path.as_posix(), "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerows(s.model_dump(by_alias=True) for s in data)


def get_teaching_report(staff_name: str, page: Page) -> list[SubjectInfo] | None:
    logger.info(f"Processing {staff_name}")

    home_page.go_to_staff_list_page(page)
    try:
        staff_list_page.go_to_staff_calendar_page(staff_name, page)
    except:
        logger.warning(f"Staff {staff_name} not found. skipping")
        return None

    subject_rows = page.locator("table tbody tr").all()

    subjects_result: dict[str, SubjectInfo] = {}

    for row in subject_rows:
        if not row.is_visible():
            continue

        class_name = row.locator("td:nth-child(4)").inner_text()

        subject_cell = row.locator("td:nth-child(5)")

        if not subject_cell.is_visible():
            continue

        subject_name_from_cell = subject_cell.locator("div:nth-child(1)").inner_text()

        subject_name = subject_name_from_cell.split("(")[0].strip()

        if subject_name not in subjects_result:
            subjects_result[subject_name] = SubjectInfo(name=subject_name, hours_per_week=0, classes=[])

        subjects_result[subject_name].hours_per_week += 1

        if class_name not in subjects_result[subject_name].classes:
            subjects_result[subject_name].classes.append(class_name)

    return list(subjects_result.values())
