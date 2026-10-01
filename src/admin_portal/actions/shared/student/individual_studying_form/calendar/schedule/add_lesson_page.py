import re

from playwright.sync_api import Page

from src.admin_portal.actions.shared import shared_actions


def select_day_of_week(day_of_week: str, page: Page):
    page.locator(".col-md-4").first.click()
    option = page.get_by_role("treeitem", name=day_of_week)

    shared_actions.wait_for_visible(option)

    option.click()


def select_start(start_time: str, page: Page):
    page.locator(".row > div:nth-child(2)").first.click()
    page.get_by_role("treeitem", name=f"({start_time})").click()


def select_room(room_number: str, page: Page):
    page.locator(".row > div:nth-child(3)").click()
    page.get_by_role("treeitem", name=room_number).click()


def select_subject(subject_name: str, page: Page):
    page.locator(".col-md-6").first.click()
    shared_actions.wait(page, 250)
    page.get_by_role("treeitem").nth(
        2
    ).click()  # just click on random subject to load proper related teacher when correct subject is selected
    shared_actions.wait(page, 250)

    page.locator(".col-md-6").first.click()
    shared_actions.wait(page, 250)
    page.get_by_role("treeitem", name=re.compile(rf"^{re.escape(subject_name)}")).click()
    shared_actions.wait(page, 250)


def submit(page: Page):
    page.get_by_role("button", name="Надіслати").click()
    shared_actions.wait_network_idle(page)
