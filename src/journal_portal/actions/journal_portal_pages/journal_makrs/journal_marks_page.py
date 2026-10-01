import datetime

from playwright.sync_api import Page

from src.journal_portal.actions.journal_portal_pages import shared_actions
from src.constants import DateFormat, DateFormatSlashes


def get_date_header_buttons(date: datetime.date, page: Page):
    return page.get_by_role("button", name=date.strftime(DateFormatSlashes.dd_mm)).all()
