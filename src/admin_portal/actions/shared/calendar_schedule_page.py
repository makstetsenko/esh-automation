import re

from playwright.sync_api import Page

from src.admin_portal.actions.shared import remove_calendar_confirmation_popup, shared_actions


def click_on_generate_week(page: Page):
    link = page.get_by_role("link", name="Сформувати тиждень")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)


def get_current_week_sequence_number(page: Page) -> int:
    calendar_heading = page.get_by_role("heading", name=re.compile(r"Тиждень"))
    shared_actions.wait_for_visible(calendar_heading)

    calendar_heading_text = calendar_heading.inner_text().strip()

    return int(calendar_heading_text.split()[1])


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


def click_on_remove_week_link(page: Page):
    link = page.get_by_role("link", name="Видалити тиждень")
    shared_actions.wait_for_visible(link)

    link.click()

    remove_calendar_confirmation_popup.confirm_week_remove(page)

    shared_actions.wait_network_idle(page)
