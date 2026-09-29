from playwright.sync_api import Locator, Page, expect


def wait_network_idle(page: Page):
    page.wait_for_load_state("networkidle")


def wait_for_visible_and_stable(locator: Locator):
    locator.wait_for(state="visible")
    element = locator.element_handle()
    if element:
        element.wait_for_element_state("stable")


def wait_for_visible(locator: Locator, timeout=30_000):
    locator.wait_for(state="visible", timeout=timeout)


def wait_for_element_attached(locator: Locator):
    expect(locator).to_be_attached()
