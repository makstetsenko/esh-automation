from src import action_description_factory
from src.action_description_factory.action_descriptor import TargetPlatform
from src.app_args import get_app_args
from src.app_logging import setup_logging

from src.browser import create_browser
from playwright.sync_api import Page, expect, sync_playwright, TimeoutError as PlaywrightTimeoutError


import logging

SCHOOL_PORTAL_URL = "https://eschool-ua.com/portal"

setup_logging()

logger = logging.getLogger(__name__)


def close_welcome_modal_if_appeared(page: Page):
    whats_new_modal = (
        page.get_by_role("heading", name="Вітаємо в оновленому E-журналі").locator("..").locator("..").locator("..")
    )

    try:
        # check here if page is visible
        expect(whats_new_modal).to_be_visible(timeout=1_000)
    except PlaywrightTimeoutError:
        # if exception -> not visible -> just continue external flow
        return

    # click on "Continue" -> close modal -> continue external flow
    whats_new_modal.get_by_role("button", name="Почати роботу").click()


def go_to_journal(page: Page):
    with page.expect_popup() as journal_page_info:
        page.get_by_role("link", name="Е-журнал Е-журнал").click()

    journal_page = journal_page_info.value
    journal_page.wait_for_load_state("networkidle")
    # close_welcome_modal_if_appeared(journal_page)
    return journal_page


def go_to_admin(page: Page):
    with page.expect_popup() as admin_page_info:
        page.get_by_role("link", name="Адміністрування Адміністрування").click()
    admin_page = admin_page_info.value
    admin_page.wait_for_load_state("networkidle")
    return admin_page


def main():

    app_args = get_app_args()

    action_descriptor = action_description_factory.action_descriptor.read_from_yaml_file(
        app_args.action_descriptor_path
    )

    with sync_playwright() as p:
        context = create_browser(p)
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(SCHOOL_PORTAL_URL)

        target_page = (
            go_to_admin(page) if action_descriptor.target_platform == TargetPlatform.ADMIN else go_to_journal(page)
        )

        while not action_descriptor is None:
            action_description_factory.execute(action_descriptor, target_page)
            action_descriptor = action_descriptor.next

        context.close()


if __name__ == "__main__":
    main()
