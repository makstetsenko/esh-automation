import datetime
import logging
import re

from playwright.sync_api import Locator, Page

from src import shared_actions
from src.constants import DateFormatDashes

logger = logging.getLogger(__name__)


def get_schedule_dates_on_page(page: Page) -> list[datetime.date]:
    grid = page.locator('div.grid[style*="grid-template-columns"]')
    children = grid.locator(":scope > div")

    date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")

    date_texts = children.locator("span").filter(has_text=date_pattern).all_inner_texts()

    return [datetime.datetime.strptime(value, DateFormatDashes.dd_mm_yyyy).date() for value in date_texts]


def get_lessons_links_for_date(
    date: datetime.date,
    page: Page,
) -> list[Locator]:

    grid = page.locator('div.grid[style*="grid-template-columns"]')

    children = grid.locator(":scope > div")

    date_text = date.strftime(DateFormatDashes.dd_mm_yyyy)
    date_header = children.filter(has=page.get_by_text(date_text, exact=True))

    if date_header.count() == 0:
        raise ValueError(f"Date {date_text} is not displayed in the schedule")

    # index among direct grid children
    header_index = date_header.evaluate("""
        el => Array.from(el.parentElement.children).indexOf(el)
        """)

    # Header layout:
    # 0 = empty/time gutter
    # 1 = Monday
    # 2 = Tuesday
    # ...
    day_column = header_index

    lessons: list[Locator] = []

    # First 7 elements are the header row.
    index = 7 + day_column

    while index < children.count():
        cell = children.nth(index)

        lesson_links = cell.locator('a[href^="/teacher/journal/rates"]')

        for i in range(lesson_links.count()):
            lessons.append(lesson_links.nth(i))

        index += 7

    return lessons


def go_to_previous_week(page: Page):
    logger.info("Go to the previous week")
    page.get_by_role("button", name="Попередній тиждень").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 1000)


def go_to_next_week(page: Page):
    logger.info("Go to the next week")
    page.get_by_role("button", name="Наступний тиждень").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 1000)
