import datetime
import re

from playwright.sync_api import Page

from src.admin_portal.actions.shared import remove_calendar_confirmation_popup, shared_actions


def has_any_lessons_on_calendar_page(page: Page):
    lessons_rows = page.locator("table tbody tr").filter(visible=True)
    shared_actions.wait_network_idle(page)

    return lessons_rows.count() > 0


def click_on_next_week_link(page: Page):
    calendar_heading = page.get_by_role("heading", name=re.compile(r"Тиждень"))
    shared_actions.wait_for_visible(calendar_heading)

    next_week_link = calendar_heading.get_by_role("link").nth(1)
    next_week_link.click()
    shared_actions.wait_network_idle(page)


def click_on_previous_week_link(page: Page):
    calendar_heading = page.get_by_role("heading", name=re.compile(r"Тиждень"))
    shared_actions.wait_for_visible(calendar_heading)

    next_week_link = calendar_heading.get_by_role("link").nth(0)
    next_week_link.click()
    shared_actions.wait_network_idle(page)


def get_dates_on_page(page: Page) -> list[datetime.date]:
    dates_spans = page.locator("div.card-header h6 span").all()

    dates: list[datetime.date] = []

    for span in dates_spans:
        date_text = span.inner_text()
        dates.append(datetime.date.fromisoformat(date_text))

    return dates


def click_on_remove_week_link(page: Page):
    link = page.get_by_role("link", name="Видалити тиждень")
    shared_actions.wait_for_visible(link)

    link.click()

    remove_calendar_confirmation_popup.confirm_week_remove(page)

    shared_actions.wait_network_idle(page)


def go_to_schedule_page(page: Page):
    link = page.get_by_role("link", name=re.compile(r"Розклад$"))
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)


def go_to_alarms_schedule_page(page: Page):
    link = page.get_by_role("link", name="Розклад дзвінків")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
