import datetime
import pathlib

from app_logging import setup_logging
from src.admin_portal.actions import (
    admin_home,
    distribute_students_in_class,
    global_students_list,
    global_teachers_list,
    global_subjects_list,
)
from src.admin_portal.actions.individual_student_schedule_setup import lesson_schedule
from src.admin_portal.domain import platform_student, platform_teacher, platform_subject
from src.admin_portal.domain import student_distribution
from src.admin_portal.domain.individual_student_schedule import get_schedule
from src.admin_portal.domain.student_distribution import StudentDistribution
from src.browser import create_browser
from playwright.sync_api import Page, sync_playwright


from src.alarms_schedule import AlarmSchedule, high_school_alarms


import logging

SCHOOL_PORTAL_URL = "https://eschool-ua.com/portal"

setup_logging()

logger = logging.getLogger(__name__)


def setup_students_individual_schedule(admin_page: Page) -> None:
    students = [
        # (
        #     "Криловський Євген Євгенович",
        #     "./data/admin_portal/individual_student_schedule/krylovskyi.csv",
        # ),
        ("Білоус Тимур Вікторович", "./data/admin_portal/individual_student_schedule/bilous.csv"),
        # ("Кононенко Андрій Максимович", "./data/admin_portal/individual_student_schedule/kononenko.csv"),
        # ("Береговий Андрій Ярославович", "./data/admin_portal/individual_student_schedule/berehovyi.csv"),
    ]

    for student_name, schedule_file in students:
        # home.go_home_page(admin_page)
        # student_alarm_schedule.set_alarm_schedule(
        #     student_name=student_name,
        #     alarm_schedule=high_school_alarms,
        #     admin_page=admin_page,
        # )

        lesson_schedules = get_schedule(schedule_file)

        # home.go_home_page(admin_page)
        # lesson_schedule.set_up_individual_plan_subjects(
        #     student_name=student_name,
        #     lesson_schedules=lesson_schedules,
        #     admin_page=admin_page,
        # )

        admin_home.go_home_page(admin_page)
        lesson_schedule.set_up_lessons_schedule(
            student_name=student_name,
            lesson_schedules=lesson_schedules,
            alarm_schedule=high_school_alarms,
            admin_page=admin_page,
        )


def download_students_list(admin_page: Page) -> None:
    students = global_students_list.get_all_students(admin_page)

    save_path = pathlib.Path("./output/platform_students.csv").resolve()

    platform_student.write_to_csv(students, save_path)

    print(f"Saved students to {save_path.as_posix()}")


def download_teachers_list(admin_page: Page) -> None:
    teachers = global_teachers_list.get_all_teachers(admin_page)

    save_path = pathlib.Path("./output/platform_teachers.csv").resolve()

    platform_teacher.write_to_csv(teachers, save_path)

    print(f"Saved teachers to {save_path.as_posix()}")


def download_subjects_list(admin_page: Page) -> None:
    subjects = global_subjects_list.get_all_subjects(admin_page)

    save_path = pathlib.Path("./output/platform_subjects.csv").resolve()

    platform_subject.write_to_csv(subjects, save_path)

    print(f"Saved subjects to {save_path.as_posix()}")


def distribute_students_in_subjects_in_class(
    subjects: list[str],
    class_name: str,
    student_distribution_csv_path: pathlib.Path,
    page: Page,
    studying_start_date: datetime.date,
    remove_selection_if_distribution_missing: bool,
) -> None:
    distribution = student_distribution.read_students_from_csv(student_distribution_csv_path)
    distribute_students_in_class.distribute_students(
        class_name, subjects, distribution, page, studying_start_date, remove_selection_if_distribution_missing
    )


def main():
    with sync_playwright() as p:
        context = create_browser(p)

        page = context.pages[0] if context.pages else context.new_page()

        page.goto(SCHOOL_PORTAL_URL)

        with page.expect_popup() as admin_page_info:
            page.get_by_role("link", name="Адміністрування Адміністрування").click()
            admin_page = admin_page_info.value
            admin_page.wait_for_load_state("networkidle")

        # ---
        # Here uncomment required actions.
        # Later I will add actions setup and choosing from config or smth
        # ---

        # 1) setup individual schedule for students
        # setup_students_individual_schedule(admin_page)

        # 2) Download students list from admin
        # download_students_list(admin_page)

        # 3) Download teachers list from admin
        # download_teachers_list(admin_page)

        # 4) Download subjects list from admin
        # download_subjects_list(admin_page)

        # 5) distribute students between groups in selected subject and class
        distribute_students_in_subjects_in_class(
            subjects=["Українська мова"],
            class_name="5-А",
            student_distribution_csv_path=pathlib.Path(
                "data/admin_portal/students-distribution-in-class/5-А-students-distribution.csv"
            ),
            page=admin_page,
            studying_start_date=datetime.date(2026, 9, 1),
            remove_selection_if_distribution_missing=True,  # If False => basically do nothing if student was not specified in csv file. If True => group selection will be removed
        )

        context.close()


if __name__ == "__main__":
    main()
