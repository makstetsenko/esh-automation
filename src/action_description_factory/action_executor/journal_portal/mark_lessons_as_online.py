import datetime
import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel

from src import shared_actions
from src.constants import DateFormat
from src.journal_portal.journal_portal_pages.journal_marks import lesson_planning_modal
from src.journal_portal.journal_portal_pages.schedule import schedule_page
from src.journal_portal.journal_portal_pages.journal_marks import journal_marks_page
from src.journal_portal.journal_portal_pages import main_page
from src.journal_portal.journal_portal_pages.schedule import lesson_link

logger = logging.getLogger(__name__)


def setup_online_for_date(date: datetime.date, page: Page):
    logger.info(f"Processing date {date.strftime(DateFormat.dd_mm_yyyy)}")

    processed_lessons: set[str] = set()

    while True:
        main_page.go_to_schedule_page(page)

        while True:
            schedule_dates = schedule_page.get_schedule_dates_on_page(page)
            if all([d > date for d in schedule_dates]):
                schedule_page.go_to_previous_week(page)
                continue

            if all([d < date for d in schedule_dates]):
                schedule_page.go_to_next_week(page)
                continue

            break

        lesson_links = [
            l
            for l in schedule_page.get_lessons_links_for_date(date, page)
            if not lesson_link.is_lesson_online(l)
            and not lesson_link.is_lesson_planned_for_online(l)
            and not lesson_link.get_lesson_details(l).key() in processed_lessons
        ]

        if len(lesson_links) == 0:
            return

        for link in lesson_links:
            lesson_details = lesson_link.get_lesson_details(link)

            logger.info(f"Configuring lesson {lesson_details.key()} for date {date.strftime(DateFormat.dd_mm_yyyy)}")

            link.click()  # navigates to journal page

            shared_actions.wait_network_idle(page)
            shared_actions.wait(page, 1000)

            date_header_btns = journal_marks_page.get_date_buttons(date, page)

            for date_btn in date_header_btns:
                date_btn.button.click()
                shared_actions.wait_network_idle(page)
                shared_actions.wait(page, 500)

                try:
                    lesson_planning_modal.open_online_tab(page)
                except Exception as e:
                    logger.error(f"Cannot setup online for lesson {lesson_details.key()} because o error {e}")
                    break

                if not lesson_planning_modal.has_google_meet_button(page):
                    lesson_planning_modal.close_modal(page)
                    continue

                lesson_planning_modal.click_on_google_meet_button(page)
                lesson_planning_modal.close_modal(page)

            processed_lessons.add(lesson_details.key())
            break


####################################################################################


class Args(BaseModel):
    dates: list[datetime.date]


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    for d in argsObj.dates:
        setup_online_for_date(d, page)
