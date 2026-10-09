import datetime
import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel

from src import shared_actions
from src.constants import DateFormat
from src.journal_portal.journal_portal_pages.journal_marks import journal_marks_page
from src.journal_portal.journal_portal_pages.journal_marks.journal_marks_page import JournalDate
from src.journal_portal.journal_portal_pages.journal_marks import grading_modal

logger = logging.getLogger(__name__)


def remove_grade_from_student(class_name: str, student_name: str, date: JournalDate, page: Page):
    """
    Remove grade from a student for a specific lesson date.
    """

    journal_marks_page.select_class(class_name, page)
    journal_marks_page.select_month(date.date.month, page)

    students = journal_marks_page.get_students(page)

    student = next((s for s in students if student_name.lower() in s.name.lower()), None)
    if not student:
        logger.warning(f"Student {student_name} not found in class {class_name}. Skipping grade removal.")
        return False

    lesson_btns = [l for l in student.lessons if l.date.key() == date.key() and not l.has_absence_mark()]

    if len(lesson_btns) == 0:
        logger.warning(
            f"No lessons found for student {student_name} on {date.date.strftime(DateFormat.dd_mm_yyyy)}. Skipping grade removal."
        )
        return False

    for lesson_btn in lesson_btns:
        if not lesson_btn.has_mark():
            logger.warning(
                f"Student {student_name} does not have a mark for {date.date.strftime(DateFormat.dd_mm_yyyy)}. Skipping grade removal."
            )
            continue

        lesson_btn.lesson_button.click()

        shared_actions.wait_network_idle(page)
        shared_actions.wait(page, 1000)

        grading_modal.remove_mark_button(page)

        shared_actions.wait_network_idle(page)
        shared_actions.wait(page, 1000)

        logger.info(f"Removed grade for student {student_name} on {date.date.strftime(DateFormat.dd_mm_yyyy)}.")


def remove_grade_from_student_batch(
    class_name: str, student_name: str, date_from: datetime.date, date_to: datetime.date, page: Page
):

    available_dates = []

    min_date = date_from if date_from < date_to else date_to
    max_date = date_to if date_from < date_to else date_from

    reference_date = max_date

    while True:
        journal_marks_page.select_class(class_name, page)
        journal_marks_page.select_month(reference_date.month, page)

        all_dates = journal_marks_page.get_all_date_buttons(page)
        available_dates += [d.date for d in all_dates if d.date.date <= max_date and d.date.date >= min_date]

        if min_date.month == all_dates[0].date.date.month:
            break

        # Finish on September or January because these months are start of academic term
        if reference_date.month in [
            1,
            9,
        ]:
            break

        reference_date = reference_date - datetime.timedelta(
            days=reference_date.day
        )  # Go to the last day of the previous month

    while len(available_dates) > 0:
        date = available_dates.pop()
        remove_grade_from_student(class_name, student_name, date, page)


####################################################################################


class Args(BaseModel):
    class_name: str
    student_name: str
    date_from: datetime.date
    date_to: datetime.date


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    remove_grade_from_student_batch(
        class_name=argsObj.class_name,
        student_name=argsObj.student_name,
        date_from=argsObj.date_from,
        date_to=argsObj.date_to,
        page=page,
    )
