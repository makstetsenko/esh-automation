import datetime
import re
from typing import ClassVar

from playwright.sync_api import Locator, Page, expect
from pydantic import BaseModel, ConfigDict

from src.journal_portal.actions.journal_portal_pages import shared_actions
from src.constants import DateFormat, DateFormatSlashes


class JournalDate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    date: datetime.date
    index: int

    def key(self):
        return f"{self.date.strftime(DateFormatSlashes.dd_mm_yyyy)}_{self.index}"


class DateButton(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    button: Locator
    date: JournalDate


class LessonButtonInfo(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

    date: JournalDate
    lesson_button: Locator

    def get_mark_value(self):
        return self.lesson_button.inner_text().strip()

    def has_mark(self):
        return self.get_mark_value() != ""

    def has_absence_mark(self):
        return self.get_mark_value().lower() in ["пп", "н", "хв"]


class StudentInfo(BaseModel):
    name: str
    is_on_individual_studying_form: bool
    lessons: list[LessonButtonInfo]


def get_all_date_buttons(page: Page) -> list[DateButton]:
    btns = page.get_by_role("button", name=re.compile(r"^\d{2}\/\d{2}$")).all()
    current_year = datetime.date.today().year

    return [
        DateButton(
            button=b,
            date=JournalDate(
                date=datetime.datetime.strptime(
                    f"{b.inner_text().strip()}/{current_year}", DateFormatSlashes.dd_mm_yyyy
                ).date(),
                index=i,
            ),
        )
        for i, b in enumerate(btns)
    ]


def get_date_buttons(date: datetime.date, page: Page) -> list[DateButton]:
    btns = get_all_date_buttons(page)
    
    return [b for b in btns if b.date.date == date]


def select_class(class_name: str, page: Page):
    combobox = page.get_by_role("combobox", name="Перемкнути клас")
    combobox.click()

    option = page.get_by_role("option", name=class_name)
    option.hover()
    option.press("Enter")

    expect(combobox).to_contain_text(
        class_name,
        timeout=15_000,
    )

    page.wait_for_timeout(timeout=1000)
    page.wait_for_load_state("networkidle")


# dropdown to change month period on page
def select_month(month_number: int, page: Page):
    month_name_map = {
        1: "Січ",
        2: "Лют",
        3: "Бер",
        4: "Кві",
        5: "Тра",
        6: "Чер",
        7: "Лип",
        8: "Сер",
        9: "Вер",
        10: "Жов",
        11: "Лис",
        12: "Гру",
    }

    btn = page.get_by_role("button", name="Перемкнути період")
    btn.click()

    month_btn = page.get_by_role("button", name=month_name_map[month_number], exact=True)
    month_btn.click()

    page.wait_for_timeout(timeout=1000)
    page.wait_for_load_state("networkidle")


def get_students(page: Page) -> list[StudentInfo]:
    students: list[StudentInfo] = []

    student_rows = page.locator("table tbody tr").all()
    date_buttons = get_all_date_buttons(page)

    for row in student_rows:
        cells = row.get_by_role("cell").all()

        student_cell: Locator = cells[0]
        lessons_cells: list[Locator] = cells[1:] if len(cells) > 1 else []
        individual_studying_label = student_cell.get_by_label("Індивідуальна форма навчання")

        lessons: list[LessonButtonInfo] = []

        for index, date_button in enumerate(date_buttons):
            lesson_btn = lessons_cells[index].locator("button") if index < len(lessons_cells) else None

            if lesson_btn is not None:
                lessons.append(LessonButtonInfo(date=date_button.date, lesson_button=lesson_btn))

        students.append(
            StudentInfo(
                name=student_cell.locator("button").first.inner_text().strip(),
                is_on_individual_studying_form=individual_studying_label.count() > 0,
                lessons=lessons,
            )
        )

    return students
