import re

from playwright.sync_api import Page

from src.alarms_schedule import LessonAlarmSchedule


def go_to_student_calendar_page(student_name: str, admin_page: Page) -> None:
    admin_page.get_by_role("link", name=" Алфавітна книга учнів").click()
    admin_page.get_by_role("link", name=student_name).first.click()
    admin_page.get_by_role("link", name=" Індивідуальне навчання").click()
    admin_page.get_by_role("link", name=" Календар").click()
    admin_page.get_by_role("link", name=" Розклад дзвінків").click()


def add_lesson_alarm_schedule(schedule: LessonAlarmSchedule, admin_page: Page) -> None:
    admin_page.get_by_role("link", name=" Додати урок").click()

    admin_page.get_by_role("spinbutton", name="номер уроку").click()
    admin_page.get_by_role("spinbutton", name="номер уроку").fill(str(schedule.lesson_number))

    admin_page.get_by_role("textbox", name="початок уроку").click()
    admin_page.get_by_role("textbox", name="початок уроку").fill(schedule.time_from)

    admin_page.get_by_role("textbox", name="кінець уроку").click()
    admin_page.get_by_role("textbox", name="кінець уроку").fill(schedule.time_to)

    admin_page.get_by_role("button", name="Надіслати ").click()


def is_alarm_exists(schedule: LessonAlarmSchedule, admin_page: Page) -> bool:
    lesson_number = str(schedule.lesson_number)

    lesson_cell = admin_page.locator("table tbody tr td:first-child").filter(
        has_text=re.compile(rf"^\s*{re.escape(lesson_number)}\s*$")
    )

    return lesson_cell.count() > 0


def set_alarm_schedule(student_name: str, alarm_schedule: list[LessonAlarmSchedule], admin_page: Page) -> None:
    """
    Set the alarm schedule for the specific student.
    """

    go_to_student_calendar_page(student_name, admin_page)

    admin_page.wait_for_load_state("networkidle")

    for schedule in alarm_schedule:
        if is_alarm_exists(schedule, admin_page):
            print(f"Alarm for {student_name} for lesson {schedule.lesson_number} already exists. Skipping.")
            continue

        add_lesson_alarm_schedule(schedule, admin_page)
