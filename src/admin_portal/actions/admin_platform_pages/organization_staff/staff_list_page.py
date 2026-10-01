from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import shared_actions


def go_to_staff_calendar_page(staff_name: str, page: Page):
    link = page.get_by_role("link", name=staff_name)
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
