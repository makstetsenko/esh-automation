from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import shared_actions


def go_to_student_page(student_name: str, page: Page):
    student_link = page.get_by_role("link", name=student_name).first
    shared_actions.wait_for_visible(student_link)

    student_link.click()
    shared_actions.wait_network_idle(page)
