import re

from playwright.sync_api import Locator, Page
from pydantic import BaseModel, ConfigDict


from src.journal_portal.actions.journal_portal_pages import shared_actions


class MarkButton(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    mark: int
    button: Locator


def close_modal(page: Page):
    for b in page.get_by_role("button", name="Закрити").all():
        if not b.is_visible():
            continue

        b.click()
        shared_actions.wait_network_idle(page)
        shared_actions.wait(page, 250)

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def open_lesson_grading_tab(page: Page):
    tab = page.get_by_role("tab", name="Оцінювання уроку")
    shared_actions.wait_for_visible(tab, 5_000)
    shared_actions.wait(page, 250)
    tab.click()
    shared_actions.wait(page, 250)
    shared_actions.wait_network_idle(page)


def open_notes_tab(page: Page):
    tab = page.get_by_role("tab", name="Примітка")
    shared_actions.wait_for_visible(tab, 5_000)
    shared_actions.wait(page, 250)
    tab.click()
    shared_actions.wait(page, 250)
    shared_actions.wait_network_idle(page)


def open_homework_tab(page: Page):
    tab = page.get_by_role("tab", name="Домашнє завдання")
    shared_actions.wait_for_visible(tab, 5_000)
    shared_actions.wait(page, 250)
    tab.click()
    shared_actions.wait(page, 250)
    shared_actions.wait_network_idle(page)


# Removing mark closes modal
def remove_mark_button(page: Page):
    btn = page.get_by_role("button", name="Видалити")
    shared_actions.wait_for_visible(btn, 5_000)
    btn.click()
    shared_actions.wait(page, 250)
    shared_actions.wait_network_idle(page)


# When mark is selected the modal is closing automatically
def get_mark_buttons(page: Page) -> list[MarkButton]:
    mark_buttons: list[MarkButton] = []

    for b in (
        page.get_by_role("tab", name="Оцінювання уроку")
        .locator("..")
        .locator("..")
        .get_by_role("button", name=re.compile(r"\d{1,2}"))
        .all()
    ):
        if not b.is_visible():
            continue

        mark = int(b.inner_text().strip())
        mark_buttons.append(MarkButton(mark=mark, button=b))

    return mark_buttons
