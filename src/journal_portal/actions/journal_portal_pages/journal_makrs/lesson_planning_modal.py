from playwright.sync_api import Page

from src.journal_portal.actions.journal_portal_pages import shared_actions


def open_online_tab(page: Page):
    btn = page.get_by_role("tab", name="Онлайн урок")
    shared_actions.wait_for_visible(btn, 5_000)
    btn.click()
    shared_actions.wait(page, 250)


def has_google_meet_button(page: Page):
    btn = page.get_by_role("button", name="GOOGLE MEET").filter(visible=True)
    return btn.count() > 0


def click_on_google_meet_button(page: Page):
    page.get_by_role("button", name="GOOGLE MEET").click()
    success_label = page.get_by_text("Онлайн-урок заплановано.")
    shared_actions.wait_for_visible(success_label)
    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)


def close_modal(page: Page):
    for b in page.get_by_label("Закрити").all():
        if not b.is_visible():
            continue
        
        b.click()
        shared_actions.wait_network_idle(page)
        shared_actions.wait(page, 250)

    shared_actions.wait_network_idle(page)
    shared_actions.wait(page, 250)
