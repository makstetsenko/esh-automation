from playwright.sync_api import Page

from src import shared_actions
from src.app_settings import get_app_settings


def confirm_week_remove(page: Page):
    popup = page.get_by_text("Видалити розклад?").locator("..").locator("..")
    shared_actions.wait_for_visible(popup, timeout=5000)

    pass_input = popup.locator("#masterKey").filter(visible=True)

    if pass_input.count() > 0:
        app_settings = get_app_settings()
        pass_input.fill(app_settings.director_password)

    yes_btn = popup.get_by_role("button", name="Так")
    yes_btn.click()

    shared_actions.wait_network_idle(page)
