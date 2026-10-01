from enum import StrEnum

from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import remove_schedule_confirmation_popup, shared_actions


class WeekName(StrEnum):
    WEEK_A = "А"
    WEEK_B = "Б"


def try_select_week(week: WeekName, page: Page):
    week_link = page.get_by_role("link", name=week, exact=True)

    if not week_link.count() > 0:
        return

    week_link.click()
    shared_actions.wait_network_idle(page)


def is_lesson_exists(day_of_week: str, subject_name: str, page: Page):
    # Monday, Tuesday ...
    day_of_week_div = page.locator("div").filter(has_text=day_of_week).nth(4).locator("..")
    subject_cell = day_of_week_div.get_by_role("cell", name=subject_name, exact=True)
    return subject_cell.count() > 0


def go_to_add_lesson_page(page: Page):
    link = page.get_by_role("link", name="Додати урок")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)


def click_on_remove_schedule_link(page: Page):
    link = page.get_by_role("link", name="Видалити розклад")
    shared_actions.wait_for_visible(link)

    link.click()

    remove_schedule_confirmation_popup.confirm_week_remove(page)

    shared_actions.wait_network_idle(page)


def go_to_individual_plan_subjects_list_page(page: Page):
    link = page.get_by_role("link", name="Індивідуальний навчальний план")
    shared_actions.wait_for_visible(link)

    link.click()
    shared_actions.wait_network_idle(page)
