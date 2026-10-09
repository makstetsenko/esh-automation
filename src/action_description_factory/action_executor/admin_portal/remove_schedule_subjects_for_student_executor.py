import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel

from src.admin_portal.admin_platform_pages import (
    home_page,
)
from src.admin_portal.admin_platform_pages.student import student_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.individual_studying_plan import (
    remove_subject_page,
)
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar import calendar_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar.schedule import (
    schedule_page,
)
from src.admin_portal.admin_platform_pages.student.individual_studying_form import individual_studying_form_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.individual_studying_plan import (
    subjects_list_page,
)
from src.admin_portal.admin_platform_pages.student_alphabetical_list import student_alphabetical_list_page

logger = logging.getLogger(__name__)


def remove_schedule_subjects_for_student(student_name: str, page: Page):
    home_page.go_to_students_list_page(page)
    student_alphabetical_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)

    individual_studying_form_page.go_to_calendar_page(page)
    calendar_page.go_to_schedule_page(page)

    schedule_page.go_to_individual_plan_subjects_list_page(page)

    while True:
        subject_rows = subjects_list_page.get_subject_rows(page)

        if len(subject_rows) == 0:
            break

        remove_btn = subjects_list_page.get_remove_subject_button(subject_rows[0])
        remove_btn.click()

        remove_subject_page.set_default_date(page)
        remove_subject_page.submit(page)


####################################################################################


class Args(BaseModel):
    student_name: str


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    remove_schedule_subjects_for_student(argsObj.student_name, page)
