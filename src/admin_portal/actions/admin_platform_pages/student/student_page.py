from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import shared_actions


def go_to_individual_plan_page(page: Page):
    link = page.get_by_role("link", name="Індивідуальне навчання")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
