import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel


from src.admin_portal.admin_platform_pages import (
    home_page,
)
from src.admin_portal.admin_platform_pages.student import student_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar import calendar_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar.schedule import (
    schedule_page,
)
from src.admin_portal.admin_platform_pages.student.individual_studying_form import individual_studying_form_page
from src.admin_portal.admin_platform_pages.student_alphabetical_list import student_alphabetical_list_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.calendar.schedule import add_lesson_page
from src.admin_portal.domain.individual_student_schedule import (
    read_schedule_from_file,
)
from src.admin_portal.domain.alarms_schedule import AlarmSchedule
from src import shared_actions

logger = logging.getLogger(__name__)


# ---


def student_individual_plan_set_up_schedule(
    student_name: str,
    schedule_plan_path: pathlib.Path,
    alarm_schedule: list[AlarmSchedule],
    page: Page,
):

    home_page.go_to_students_list_page(page)
    student_alphabetical_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    individual_studying_form_page.go_to_calendar_page(page)
    calendar_page.go_to_schedule_page(page)

    lesson_schedules = read_schedule_from_file(schedule_plan_path)

    for lesson_schedule in lesson_schedules:
        if lesson_schedule.week_number == 1:
            schedule_page.try_select_week(schedule_page.WeekName.WEEK_A, page)

        if lesson_schedule.week_number == 2:
            schedule_page.try_select_week(schedule_page.WeekName.WEEK_B, page)

        if schedule_page.is_lesson_exists(lesson_schedule.day_of_week, lesson_schedule.subject, page) > 0:
            print(
                f"Lesson for {lesson_schedule.subject} on {lesson_schedule.day_of_week} already exists for {student_name}. Skipping."
            )
            continue

        lesson_alarm = next(
            (alarm for alarm in alarm_schedule if alarm.lesson_number == lesson_schedule.lesson_number),
            AlarmSchedule(lesson_number=lesson_schedule.lesson_number, time_from="08:30", time_to="09:15"),
        )

        schedule_page.go_to_add_lesson_page(page)

        shared_actions.wait(page, 500)

        add_lesson_page.select_day_of_week(lesson_schedule.day_of_week, page)
        add_lesson_page.select_start(lesson_alarm.time_from, page)
        add_lesson_page.select_room(str(lesson_schedule.room), page)

        add_lesson_page.select_subject(lesson_schedule.subject, page)
        shared_actions.wait(page, 500)

        add_lesson_page.submit(page)


####################################################################################


class Args(BaseModel):
    student_name: str
    schedule_plan_path: str
    alarm_schedule: list[AlarmSchedule]


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    student_individual_plan_set_up_schedule(
        argsObj.student_name, pathlib.Path(argsObj.schedule_plan_path), argsObj.alarm_schedule, page
    )
