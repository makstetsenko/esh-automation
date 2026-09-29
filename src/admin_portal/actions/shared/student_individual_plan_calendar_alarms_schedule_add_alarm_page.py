
from playwright.sync_api import Page

from src.admin_portal.actions.shared import shared_actions


def fill_lesson_number(lesson_number: int, page: Page):
    page.get_by_role("spinbutton", name="номер уроку").fill(str(lesson_number))


def fill_start_time(start_time: str, page: Page):
    page.get_by_role("textbox", name="початок уроку").fill(start_time)


def fill_end_time(end_time: str, page: Page):
    page.get_by_role("textbox", name="кінець уроку").fill(end_time)


def submit(page: Page):
    page.get_by_role("button", name="Надіслати").click()
    shared_actions.wait_network_idle(page)