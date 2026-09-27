from playwright.sync_api import Page


def go_home_page(page: Page) -> None:
    """
    Navigate to the home page of the admin portal.
    """
    home_link = page.get_by_role("link", name="Ліцей")
    if home_link.is_visible():
        home_link.click()
