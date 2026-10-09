import datetime
import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel


from src.admin_portal.admin_platform_pages import (
    home_page,
)
from src.admin_portal.admin_platform_pages.student import student_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.individual_studying_plan import (
    add_subject_page,
)
from src.admin_portal.admin_platform_pages.student.individual_studying_form import individual_studying_form_page
from src.admin_portal.admin_platform_pages.student.individual_studying_form.individual_studying_plan import (
    subjects_list_page,
)
from src.admin_portal.admin_platform_pages.student_alphabetical_list import student_alphabetical_list_page
from src.admin_portal.domain.individual_student_schedule import (
    IndividualHomeBasedSubjectSchedule,
    read_schedule_from_file,
)

logger = logging.getLogger(__name__)


class SubjectSetup(BaseModel):
    subject: str
    teacher_surname: str
    room: str
    hours_per_week: float


def get_subject_setup(lesson_schedules: list[IndividualHomeBasedSubjectSchedule]) -> list[SubjectSetup]:

    res = {}
    for lesson_schedule in lesson_schedules:
        key = lesson_schedule.subject

        if key in res:
            continue

        teacher_name_parts = lesson_schedule.teacher.split()
        if len(teacher_name_parts) <= 1:
            teacher_name_parts = lesson_schedule.teacher.split(".")

        res[key] = SubjectSetup(
            subject=lesson_schedule.subject,
            teacher_surname=([n for n in teacher_name_parts if len(n) > 2][0] if lesson_schedule.teacher else ""),
            room=lesson_schedule.room or "0",
            hours_per_week=lesson_schedule.hours_per_week,
        )

    return list(res.values())


# ---


def student_individual_plan_set_up_subjects(
    student_name: str,
    schedule_plan_path: pathlib.Path,
    individual_plan_start_date: datetime.date,
    page: Page,
):
    home_page.go_to_students_list_page(page)
    student_alphabetical_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    individual_studying_form_page.go_to_individual_plan_subjects_list_page(page)

    lesson_schedules = read_schedule_from_file(schedule_plan_path)

    subject_setups = get_subject_setup(lesson_schedules)

    for subject_setup in subject_setups:

        if subjects_list_page.is_subject_exists(subject_setup.subject, page):
            print(f"Subject {subject_setup.subject} already exists for {student_name}. Skipping.")
            continue

        subjects_list_page.go_to_add_new_subject_group(page)

        add_subject_page.select_subject(subject_setup.subject, page)
        add_subject_page.fill_hours_per_week(subject_setup.hours_per_week, page)
        add_subject_page.fill_start_date(individual_plan_start_date, page)
        add_subject_page.select_teacher(subject_setup.teacher_surname, page)
        add_subject_page.submit_form(page)


####################################################################################


class Args(BaseModel):
    student_name: str
    schedule_plan_path: str
    individual_plan_start_date: datetime.date


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    student_individual_plan_set_up_subjects(
        argsObj.student_name, pathlib.Path(argsObj.schedule_plan_path), argsObj.individual_plan_start_date, page
    )
