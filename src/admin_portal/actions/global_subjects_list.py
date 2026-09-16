from playwright.sync_api import Page

from src.admin_portal.domain.platform_subject import PlatformSubject

CLASS_YEARS = range(1, 12)


def go_to_subjects_list_page(admin_page: Page) -> None:
    admin_page.get_by_role("link", name="Налаштування школи ").click()
    admin_page.get_by_role("link", name="Предмети").click()

    admin_page.wait_for_load_state("networkidle")


def go_to_class_year_subjects(admin_page, year):
    admin_page.get_by_role("link", name="Паралель").click()
    admin_page.get_by_role("link", name=f"Паралель {year}", exact=True).click()
    admin_page.wait_for_load_state("networkidle")


def get_all_subjects(admin_page: Page) -> list[PlatformSubject]:
    go_to_subjects_list_page(admin_page)

    subjects: dict[tuple[int, str], PlatformSubject] = {}

    for year in CLASS_YEARS:
        go_to_class_year_subjects(admin_page, year)

        subjects_columns = admin_page.locator(".table tbody td:nth-child(3)")

        for s in subjects_columns.all():
            subject_name = s.inner_text()

            if subject_name.strip() == "":
                continue

            key = (year, subject_name)

            if key in subjects:
                continue

            subjects[key] = PlatformSubject(name=subject_name, class_year=year)

    return list(subjects.values())
