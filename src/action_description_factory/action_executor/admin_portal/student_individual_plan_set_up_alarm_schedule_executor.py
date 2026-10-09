import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel


from src.admin_portal.admin_platform_pages import (
    home_page,
)
from src.admin_portal.admin_platform_pages.student import student_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar import calendar_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar.alarm_schedule import (
    alarms_schedule_page,
)
from src.admin_portal.admin_platform_pages.student.individual_studying_form import individual_studying_form_page
from src.admin_portal.admin_platform_pages.student_alphabetical_list import student_alphabetical_list_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar.alarm_schedule import add_alarm_page
from src.admin_portal.domain.alarms_schedule import AlarmSchedule

logger = logging.getLogger(__name__)


# ---


def student_individual_plan_set_up_alarm_schedule(
    student_name: str, alarm_schedule: list[AlarmSchedule], page: Page
) -> None:
    """
    Set the alarm schedule for the specific student.
    """

    home_page.go_to_students_list_page(page)
    student_alphabetical_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    individual_studying_form_page.go_to_calendar_page(page)
    calendar_page.go_to_alarms_schedule_page(page)

    for schedule in alarm_schedule:
        if alarms_schedule_page.is_alarm_lesson_exists(schedule.lesson_number, page):
            print(f"Alarm for {student_name} for lesson {schedule.lesson_number} already exists. Skipping.")
            continue

        alarms_schedule_page.go_to_add_alarm_page(page)
        add_alarm_page.fill_lesson_number(schedule.lesson_number, page)
        add_alarm_page.fill_start_time(schedule.time_from, page)
        add_alarm_page.fill_end_time(schedule.time_to, page)
        add_alarm_page.submit(page)


####################################################################################


class Args(BaseModel):
    student_name: str
    alarm_schedule: list[AlarmSchedule]


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    student_individual_plan_set_up_alarm_schedule(argsObj.student_name, argsObj.alarm_schedule, page)


# ---
