
from playwright.sync_api import Page

from src.admin_portal.actions.shared import shared_actions


def is_subject_exists(subject_name: str, page: Page):
    subject_cell = page.get_by_role("cell", name=subject_name, exact=True)
    return subject_cell.count() > 0


def go_to_add_new_subject_group(page: Page):
    link = page.get_by_role("link", name="Додати групу").first
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)