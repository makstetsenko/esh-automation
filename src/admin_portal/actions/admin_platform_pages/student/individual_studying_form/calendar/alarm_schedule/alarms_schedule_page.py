import re

from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import shared_actions


def is_alarm_lesson_exists(lesson_number: int, page: Page):
    lesson_cell = page.locator("table tbody tr td:first-child").filter(
        has_text=re.compile(rf"^\s*{re.escape(str(lesson_number))}\s*$")
    )

    return lesson_cell.count() > 0


def go_to_add_alarm_page(page: Page):
    link = page.get_by_role("link", name="Додати урок")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
