import datetime
from enum import Enum
import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel

from src.admin_portal.admin_platform_pages import (
    home_page,
)
from src.admin_portal.admin_platform_pages.school_class import class_page
from src.admin_portal.admin_platform_pages.school_calendar import school_calendar_page
from src.admin_portal.admin_platform_pages.school_class.calendar import class_calendar_page
from src.admin_portal.admin_platform_pages.student import student_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar import calendar_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form import individual_studying_form_page
from src.admin_portal.admin_platform_pages.student_alphabetical_list import student_alphabetical_list_page
from src.admin_portal.domain.calendar_school_type import CalendarSchoolType

logger = logging.getLogger(__name__)


def remove_calendar_weeks_for_individual_student_until_stop_date(
    student_name: str, stop_date: datetime.date, page: Page
):
    home_page.go_to_students_list_page(page)
    student_alphabetical_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    individual_studying_form_page.go_to_calendar_page(page)

    while True:
        if calendar_page.has_any_lessons_on_calendar_page(page):
            calendar_page.click_on_remove_week_link(page)

        if stop_date in calendar_page.get_dates_on_page(page):
            break

        calendar_page.click_on_previous_week_link(page)


####################################################################################


class Args(BaseModel):
    student_name: str
    stop_date: datetime.date


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    remove_calendar_weeks_for_individual_student_until_stop_date(argsObj.student_name, argsObj.stop_date, page)
