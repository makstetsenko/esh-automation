from playwright.sync_api import Page

from src.admin_portal.actions.shared import shared_actions


def go_to_calendar_page(page: Page):
    link = page.get_by_role("link", name="Зміни до розкладу")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
