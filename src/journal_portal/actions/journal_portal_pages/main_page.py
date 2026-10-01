from playwright.sync_api import Page

from src.journal_portal.actions.journal_portal_pages import shared_actions


def go_to_schedule_page(page: Page):
    page.get_by_test_id("appshell-nav").get_by_role("link", name="Розклад").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 500)
