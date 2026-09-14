import re

from playwright.sync_api import Page
from pydantic import BaseModel


from src.admin_portal.domain.individual_student_schedule import IndividualHomeBasedSubjectSchedule
from src.alarms_schedule import AlarmSchedule


class SubjectSetup(BaseModel):
    subject: str
    teacher_surname: str
    room: str
    hours_per_week: str
    start_date: str = "01.09.2026"


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
            hours_per_week=str(lesson_schedule.hours_per_week),
            start_date=lesson_schedule.start_date or "01.09.2026",
        )

    return list(res.values())


def go_to_individual_plan_page(student_name: str, admin_page: Page) -> None:
    admin_page.get_by_role("link", name="Алфавітна книга учнів").click()
    admin_page.get_by_role("link", name=student_name).first.click()
    admin_page.get_by_role("link", name=" Індивідуальне навчання").click()
    admin_page.get_by_role("link", name="Індивідуальний навчальний план").click()


def setup_subject_params(subject_setup: SubjectSetup, admin_page: Page) -> None:
    # Select subject
    admin_page.locator(".col-6").first.click()
    admin_page.locator("label").filter(has_text=re.compile(rf"^\s*{re.escape(subject_setup.subject)}\s*$")).click()

    # Setup horse per week
    admin_page.locator('input[name="hours_per_week"]').fill(subject_setup.hours_per_week)

    # Setup start date
    admin_page.get_by_role("textbox", name="дд.мм.рррр").fill(subject_setup.start_date)

    # Select teacher
    admin_page.locator(".col").click()
    admin_page.get_by_role("treeitem", name=subject_setup.teacher_surname, exact=False).click()

    # Submit form
    admin_page.get_by_role("button", name="Надіслати ").click()


def set_up_individual_plan_subjects(
    student_name: str, lesson_schedules: list[IndividualHomeBasedSubjectSchedule], admin_page: Page
):
    go_to_individual_plan_page(student_name, admin_page)
    admin_page.wait_for_load_state("networkidle")

    subject_setups = get_subject_setup(lesson_schedules)
    for subject_setup in subject_setups:

        subject_locator = admin_page.get_by_role("cell", name=subject_setup.subject, exact=True)

        if subject_locator.count() > 0:
            print(f"Subject {subject_setup.subject} already exists for {student_name}. Skipping.")
            continue

        admin_page.get_by_role("link", name=" Додати групу").first.click()
        admin_page.wait_for_load_state("networkidle")

        setup_subject_params(subject_setup, admin_page)
        admin_page.wait_for_load_state("networkidle")


# ---


def go_to_calendar_page(student_name: str, admin_page: Page) -> None:
    admin_page.get_by_role("link", name="Алфавітна книга учнів").click()
    admin_page.get_by_role("link", name=student_name).first.click()
    admin_page.get_by_role("link", name=" Індивідуальне навчання").click()
    admin_page.get_by_role("link", name=" Календар").click()
    admin_page.get_by_role("link", name=" Розклад").click()


def set_up_lessons_schedule(
    student_name: str,
    lesson_schedules: list[IndividualHomeBasedSubjectSchedule],
    alarm_schedule: list[AlarmSchedule],
    admin_page: Page,
):
    go_to_calendar_page(student_name, admin_page)
    admin_page.wait_for_load_state("networkidle")

    for lesson_schedule in lesson_schedules:
        week_a_locator = admin_page.get_by_role("link", name="А", exact=True)
        week_b_locator = admin_page.get_by_role("link", name="Б", exact=True)

        if lesson_schedule.week_number == 1 and week_a_locator.count() > 0:
            week_a_locator.click()
            admin_page.wait_for_load_state("networkidle")

        if lesson_schedule.week_number == 2 and week_b_locator.count() > 0:
            week_b_locator.click()
            admin_page.wait_for_load_state("networkidle")

        week_name_div = admin_page.locator("div").filter(has_text=lesson_schedule.day_of_week).nth(4).locator("..")
        subject_cell = week_name_div.get_by_role("cell", name=lesson_schedule.subject, exact=True)

        if subject_cell.count() > 0:
            print(
                f"Lesson for {lesson_schedule.subject} on {lesson_schedule.day_of_week} already exists for {student_name}. Skipping."
            )
            continue

        set_up_calendar_lesson(alarm_schedule, admin_page, lesson_schedule)


def set_up_calendar_lesson(alarm_schedule, admin_page, lesson_schedule):
    admin_page.get_by_role("link", name=" Додати урок").click()

    # Set day of week
    admin_page.locator(".col-md-4").first.click()
    admin_page.get_by_role("treeitem", name=lesson_schedule.day_of_week).click()

    # set lesson number
    lesson_alarm = next(
        (alarm for alarm in alarm_schedule if alarm.lesson_number == lesson_schedule.lesson_number),
        AlarmSchedule(lesson_number=lesson_schedule.lesson_number, time_from="08:30", time_to="09:15"),
    )
    admin_page.locator(".row > div:nth-child(2)").first.click()
    admin_page.get_by_role("treeitem", name=f"({lesson_alarm.time_from})").click()

    # Set room number
    admin_page.locator(".row > div:nth-child(3)").click()
    admin_page.get_by_role("treeitem", name=str(lesson_schedule.room)).click()

    # Set subject
    admin_page.locator(".col-md-6").first.click()
    admin_page.get_by_role("treeitem", name=re.compile(rf"^{re.escape(lesson_schedule.subject)}")).click()

    # Submit form
    admin_page.get_by_role("button", name="Надіслати ").click()
    admin_page.wait_for_load_state("networkidle")
