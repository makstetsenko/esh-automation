import logging

from playwright.sync_api import Locator, Page

from src import shared_actions

logger = logging.getLogger(__name__)


def get_semester_radio(semester_number: int, page: Page) -> Locator:
    return page.get_by_role("radio", name=f"{semester_number} семестр")


def get_plan_table(page: Page) -> Locator:
    return page.get_by_role("table", name="Журнал тем")


def get_link_all_dates_button(page: Page) -> Locator:
    return page.get_by_role("button", name="Прив'язати всі дати до тем")


def get_unlink_all_dates_buttons(page: Page) -> list[Locator]:
    return page.get_by_label("Відв'язати всі дати теми").all()


def get_switch_class_combobox(page: Page) -> Locator:
    return page.get_by_role("combobox", name="Перемкнути клас")


def get_switch_subject_combobox(page: Page) -> Locator:
    return page.get_by_role("combobox", name="Перемкнути предмет і навчальну групу")


def get_available_options_list(page: Page) -> list[Locator]:
    return page.get_by_role("option").all()


def try_link_all_dates_to_lessons(page: Page):
    logger.info("Try link all dates to lessons")
    btn = get_link_all_dates_button(page)

    if btn.count() == 0:
        logger.warning("Cant link all dates because related button was not found")
        return

    btn.click()
    shared_actions.wait(page, 500)

    submit_btn = page.get_by_role("button", name="Прив'язати", exact=True)
    submit_btn.click()
    shared_actions.wait(page, 500)
    shared_actions.wait_network_idle(page)


def try_unlink_all_dates_to_lessons(page: Page):
    logger.info("Try unlink all dates to lessons")
    btns = get_unlink_all_dates_buttons(page)

    if len(btns) == 0:
        logger.warning("Cant unlink all dates because related button was not found")
        return

    for btn in btns:
        btn.click()
        shared_actions.wait(page, 500)

        submit_btn = page.get_by_role("button", name="Відв'язати", exact=True)
        submit_btn.click()
        shared_actions.wait(page, 500)
        shared_actions.wait_network_idle(page)
