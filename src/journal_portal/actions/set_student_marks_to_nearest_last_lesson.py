from playwright.sync_api import Locator, Page, expect
from pydantic import BaseModel
import datetime
import random

import logging

logger = logging.getLogger(__name__)

# List of marks that never should be changed automatically
PERSIST_MARKS_LIST = ["ПП", "Н"]


class StudentMark(BaseModel):
    student_surname: str
    marks: list[int]
    override: bool


def go_to_journal(page: Page):
    page.wait_for_load_state("networkidle")
    link = page.get_by_test_id("appshell-nav").get_by_role("link", name="Журнал оцінок")

    expect(link).to_be_visible(timeout=60_000)
    link.click()

    page.wait_for_load_state("networkidle")


def go_to_class(class_name: str, page: Page):
    page.get_by_role("combobox", name="Перемкнути клас").click()

    option = page.get_by_role("option", name=class_name)
    expect(option).to_be_visible(timeout=5_000)
    option.click()

    page.wait_for_load_state("networkidle")


def find_nearest_date_index(page: Page):
    date_spans = page.locator("table thead th span").filter(has_not_text="+").all()

    today = datetime.date.today()
    lesson_dates: list[datetime.date] = []

    for span in date_spans:
        date_str = span.inner_text()  # format is "dd/mm"
        date_parts = date_str.split("/")
        lesson_dates.append(datetime.date(today.year, int(date_parts[1]), int(date_parts[0])))

    for index, d in enumerate(lesson_dates):
        if d > today:
            return index - 1  # return previous nearest to today lesson date index

    return 0


def select_mark_from_modal(selected_mark: int, mark_setup_button: Locator, page: Page):
    mark_setup_button.click()

    page.wait_for_load_state("networkidle")

    mark_selection_modal = page.locator("header").filter(has_text="Оцінювання").locator("..")
    expect(mark_selection_modal).to_be_visible(timeout=60_000)

    select_mark_button = mark_selection_modal.get_by_role("button", name=str(selected_mark), exact=True)
    select_mark_button.click()

    expect(mark_selection_modal).to_be_hidden(timeout=60_000)
    page.wait_for_load_state("networkidle")


def set_marks_to_student(start_date_index: int, mark_selection: StudentMark, student_row: Locator, page: Page):
    # need to skip students that are on individual studying form
    individual_studying_label = student_row.get_by_label("Індивідуальна форма навчання")
    student_name_span = student_row.locator("td span").last

    student_name = student_name_span.inner_text()

    if individual_studying_label.count() > 0:
        logger.info(f"Skipping student {student_name} because he is on individual studying")
        return

    mark_setup_buttons = student_row.locator("td button:not([aria-label='Дані учня'])").all()

    next_mark_index = 0

    for mark_btn_i in range(start_date_index, -1, -1):
        mark_btn = mark_setup_buttons[mark_btn_i]
        existing_mark_value = mark_btn.inner_text().strip()

        if existing_mark_value in PERSIST_MARKS_LIST:
            logger.info(f"Skipping mark {existing_mark_value} because it is persistent mark")
            continue

        if existing_mark_value != "" and not mark_selection.override:
            logger.info(f"Skipping mark {existing_mark_value} because override is not permitted")
            continue

        select_mark_from_modal(mark_selection.marks[next_mark_index], mark_btn, page)
        next_mark_index += 1

        if next_mark_index > len(mark_selection.marks) - 1:
            break


def set_marks_to_nearest_lessons(student_marks: list[StudentMark], class_name: str, page: Page):
    go_to_journal(page)
    go_to_class(class_name, page)

    date_index = find_nearest_date_index(page)

    student_rows = page.locator("table tbody tr").all()

    for row in student_rows:
        student_name_span = row.locator("td span").last
        student_name = student_name_span.inner_text()

        mark_selection: StudentMark | None = None

        for s in student_marks:
            if s.student_surname in student_name:
                mark_selection = s
                break

        if mark_selection is None:
            logger.info(f"Mark selection was not found for student {student_name}")
            continue

        set_marks_to_student(date_index, mark_selection, row, page)


# Set random mark between [min, max] inclusive values to all students
def set_random_mark_to_nearest_lessons_to_all_students(mark_min: int, mark_max: int, class_name: str, page: Page):
    go_to_journal(page)
    go_to_class(class_name, page)

    date_index = find_nearest_date_index(page)

    student_rows = page.locator("table tbody tr").all()

    for row in student_rows:
        mark_selection: StudentMark = StudentMark(
            student_surname="", marks=[random.randint(mark_min, mark_max)], override=False
        )
        set_marks_to_student(date_index, mark_selection, row, page)
