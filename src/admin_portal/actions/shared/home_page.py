from playwright.sync_api import Page

from src.admin_portal.actions.shared import shared_actions


def go_to_staff_list_page(page: Page) -> None:
    link = page.get_by_role("link", name="Працівники")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)


def go_to_students_list_page(page: Page) -> None:
    link = page.get_by_role("link", name="Алфавітна книга учнів")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)


def click_on_school_schedule_link(page: Page):
    schedule_option = page.get_by_role("link", name="Розклад школи")
    shared_actions.wait_for_visible(schedule_option)

    schedule_option.click()
    shared_actions.wait_network_idle(page)


def go_to_junior_schedule_page(page: Page):
    click_on_school_schedule_link(page)

    link = page.get_by_role("link", name="Молодша школа (1-4 класи)")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)


def go_to_high_schedule_page(page: Page):
    click_on_school_schedule_link(page)

    link = page.get_by_role("link", name="Старша школа (5-12 класи)")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)


def go_to_individual_schedule_page(page: Page):
    click_on_school_schedule_link(page)

    link = page.get_by_role("link", name="Індивідуальна форма")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)

def go_to_class_page(class_name: str, page: Page):
    link = page.get_by_role("link", name=class_name, exact=True)
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
