from playwright.sync_api import Page

from src.admin_portal.actions.shared import shared_actions


def go_to_calendar_page(page: Page):
    link = page.get_by_role("link", name="Календар")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)

def go_to_individual_plan_subjects_list_page(page: Page):
    link = page.get_by_role("link", name="Індивідуальний навчальний план")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)