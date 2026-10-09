from playwright.sync_api import Page

from src.admin_portal.admin_platform_pages import breadcrumbs


def execute(args: dict | None, page: Page) -> None:
    breadcrumbs.go_home_page(page)
