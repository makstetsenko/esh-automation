import datetime
import logging

from playwright.sync_api import Page
from pydantic import BaseModel

from src import shared_actions
from src.constants import DateFormat

from src.journal_portal.journal_portal_pages.journal_marks import journal_marks_page
from src.journal_portal.journal_portal_pages.journal_marks import grading_modal

logger = logging.getLogger(__name__)


def try_grade_student(
    class_name: str, student_name: str, date: journal_marks_page.JournalDate, mark: int, override: bool, page: Page
) -> bool:
    """
    Grade a student for a specific date.
    """

    logger.info(
        f"Grading student {student_name} in class {class_name} for date {date.date.strftime(DateFormat.dd_mm_yyyy)} with mark {mark}."
    )

    journal_marks_page.select_class(class_name, page)
    journal_marks_page.select_month(date.date.month, page)

    students = journal_marks_page.get_students(page)

    student = next((s for s in students if student_name.lower() in s.name.lower()), None)
    if not student:
        logger.warning(f"Student {student_name} not found in class {class_name}. Skipping grading.")
        return False

    lesson_btns = [l for l in student.lessons if l.date.key() == date.key() and not l.has_absence_mark()]

    if len(lesson_btns) == 0:
        logger.warning(
            f"No lessons found for student {student_name} on {date.date.strftime(DateFormat.dd_mm_yyyy)}. Skipping grading."
        )
        return False

    for lesson_btn in lesson_btns:
        if lesson_btn.has_mark() and not override:
            logger.warning(
                f"Student {student_name} already has a mark for {date.date.strftime(DateFormat.dd_mm_yyyy)}. Skipping grading."
            )
            continue

        lesson_btn.lesson_button.click()
        shared_actions.wait_network_idle(page)
        shared_actions.wait(page, 1000)

        grading_modal.open_lesson_grading_tab(page)
        mark_buttons = grading_modal.get_mark_buttons(page)

        mark_button = next((b for b in mark_buttons if b.mark == mark), None)

        if not mark_button:
            logger.warning(f"Mark {mark} not found on grading modal. Skipping grading.")
            grading_modal.close_modal(page)
            continue

        mark_button.button.click()
        shared_actions.wait_network_idle(page)
        shared_actions.wait(page, 1000)

        logger.info(
            f"Graded student {student_name} with mark {mark} for date {date.date.strftime(DateFormat.dd_mm_yyyy)}."
        )
        return True  # We only want to grade the first applicable lesson for the date

    return False


def grade_student_batch(
    class_name: str,
    student_name: str,
    date_from: datetime.date,
    date_to: datetime.date,
    marks: list[int | None],
    override: bool,
    page: Page,
) -> None:
    available_dates: list[journal_marks_page.JournalDate] = []

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

        if reference_date.month in [
            1,
            9,
        ]:  # Finish on September or January because these months are start of academic term
            break

        reference_date = reference_date - datetime.timedelta(
            days=reference_date.day
        )  # Go to the last day of the previous month

    for mark in marks:
        if len(available_dates) == 0:
            logger.warning(f"No more available dates to grade student {student_name}. Stopping batch grading.")
            break

        while len(available_dates) > 0:
            date_to_grade = available_dates.pop()

            if mark is None:
                logger.info(
                    f"Skipping grading for student {student_name} on {date_to_grade.date.strftime(DateFormat.dd_mm_yyyy)} as mark is None."
                )
                break  # Move to the next mark

            if try_grade_student(class_name, student_name, date_to_grade, mark, override, page):
                break  # Move to the next mark after successfully grading


class StudentGradeInfo(BaseModel):
    student_name: str
    marks: list[int | None]
    override: bool


def grade_list_of_students(
    class_name: str,
    students: list[StudentGradeInfo],
    date_from: datetime.date,
    date_to: datetime.date,
    page: Page,
) -> None:
    for s in students:
        grade_student_batch(class_name, s.student_name, date_from, date_to, s.marks, s.override, page)


####################################################################################


class Args(BaseModel):
    class_name: str
    students: dict[str, list[int | None]]
    date_from: datetime.date
    date_to: datetime.date


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    grade_list_of_students(
        class_name=argsObj.class_name,
        students=[
            StudentGradeInfo(student_name=student_name, marks=marks, override=False)
            for student_name, marks in argsObj.students.items()
        ],
        date_from=argsObj.date_from,
        date_to=argsObj.date_to,
        page=page,
    )
