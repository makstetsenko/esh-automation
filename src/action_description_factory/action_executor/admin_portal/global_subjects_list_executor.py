import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel

from src.action_description_factory.action_executor.admin_portal import dto
from src.action_description_factory.action_executor.admin_portal.dto.platform_subject import PlatformSubject

CLASS_YEARS = range(1, 12)
logger = logging.getLogger(__name__)


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


####################################################################################
class Args(BaseModel):
    output_file_path: str


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    argsObj = parse_args(args)
    output_file_path: pathlib.Path = pathlib.Path(argsObj.output_file_path)

    data = get_all_subjects(page)

    dto.platform_subject.write_to_csv(data, output_file_path)
    logger.info(f"Saved report at path {output_file_path.resolve().absolute().as_posix()}")
