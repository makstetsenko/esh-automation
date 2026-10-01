import datetime
import re

from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import shared_actions
from src.constants import DateFormat


def select_subject(subject_name: str, page: Page):
    page.locator(".col-6").first.click()

    option = page.locator("label").filter(has_text=re.compile(rf"^\s*{re.escape(subject_name)}\s*$"))
    shared_actions.wait_for_visible(option)

    option.click()


def fill_hours_per_week(hours_per_week: float, page: Page):
    input = page.locator('input[name="hours_per_week"]')
    input.fill(f"{hours_per_week:g}")


def fill_start_date(start_date: datetime.date, page: Page):
    input = page.get_by_role("textbox", name="дд.мм.рррр")
    input.fill(start_date.strftime(DateFormat.dd_mm_yyyy))


def select_teacher(teacher_name: str, page: Page):
    page.locator(".col").first.click()

    option = page.get_by_role("treeitem", name=teacher_name, exact=False)
    shared_actions.wait_for_visible(option)

    option.click()


def submit_form(page: Page):
    btn = page.get_by_role("button", name="Надіслати")
    shared_actions.wait_for_visible(btn)

    btn.click()
    shared_actions.wait_network_idle(page)
