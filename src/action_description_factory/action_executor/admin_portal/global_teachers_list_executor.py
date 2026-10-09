import logging
import pathlib

from playwright.sync_api import Page
from pydantic import BaseModel

from src.action_description_factory.action_executor.admin_portal import dto
from src.action_description_factory.action_executor.admin_portal.dto.platform_teacher import PlatformTeacher

logger = logging.getLogger(__name__)


def go_to_teachers_list_page(admin_page: Page) -> None:
    admin_page.get_by_role("link", name="Працівники").click()
    admin_page.wait_for_load_state("networkidle")


def get_all_teachers(admin_page: Page) -> list[PlatformTeacher]:
    go_to_teachers_list_page(admin_page)

    links = admin_page.locator(".table.table-bordered tbody").locator("tr td:nth-child(2) a")

    teachers: dict[str, PlatformTeacher] = {}

    for link in links.all():
        original_student_full_name = link.inner_text()

        if original_student_full_name in teachers:
            continue

        if original_student_full_name.strip() == "":
            continue

        if len(original_student_full_name.split()) < 2:
            continue

        # Adding name as it is on platform.
        # We should use original naming even if there are extra spacing and etc

        full_name_parts = original_student_full_name.strip().split()
        has_middle_name = len(full_name_parts) == 3

        teachers[original_student_full_name] = PlatformTeacher(
            first_name=full_name_parts[1],
            last_name=full_name_parts[0],
            middle_name=full_name_parts[2] if has_middle_name else "",
            original_name_on_platform=original_student_full_name,
        )

    return list(teachers.values())


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

    data = get_all_teachers(page)

    dto.platform_teacher.write_to_csv(data, output_file_path)
    logger.info(f"Saved report at path {output_file_path.resolve().absolute().as_posix()}")
