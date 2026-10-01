import datetime

from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import shared_actions
from src.constants import DateFormat


def set_date(date: datetime.date, page: Page):
    textbox = page.get_by_role("textbox", name="дд.мм.рррр")
    textbox.fill(date.strftime(DateFormat.dd_mm_yyyy))


def set_default_date(page: Page):
    default_date = datetime.date(datetime.date.today().year, 9, 1)
    set_date(default_date, page)


def submit(page: Page):
    page.get_by_role("button", name="Надіслати").click()
    shared_actions.wait_network_idle(page)
