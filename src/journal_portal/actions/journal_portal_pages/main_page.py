from playwright.sync_api import expect
from playwright.sync_api import Page

from src.journal_portal.actions.journal_portal_pages import shared_actions


def go_to_schedule_page(page: Page):
    page.get_by_test_id("appshell-nav").get_by_role("link", name="Розклад").click()
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 500)


def go_to_journal(page: Page):
    page.wait_for_load_state("networkidle")
    link = page.get_by_test_id("appshell-nav").get_by_role("link", name="Журнал оцінок")

    expect(link).to_be_visible(timeout=60_000)
    link.click()

    page.wait_for_load_state("networkidle")
