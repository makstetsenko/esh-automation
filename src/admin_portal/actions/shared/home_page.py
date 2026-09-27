from playwright.sync_api import Page

from src.admin_portal.actions.shared import shared_actions


def go_to_staff_list_page(page: Page) -> None:
    link = page.get_by_role("link", name="Працівники")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
