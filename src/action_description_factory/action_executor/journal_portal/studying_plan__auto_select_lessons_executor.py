from enum import StrEnum
import logging

from playwright.sync_api import Page
from pydantic import BaseModel

from src.journal_portal.journal_portal_pages import main_page
from src.journal_portal.journal_portal_pages.studying_plan import studying_plan_page

logger = logging.getLogger(__name__)


class LinkAction(StrEnum):
    LINK = "link"
    UNLINK = "unlink"


class Args(BaseModel):
    action: LinkAction


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)


def execute(args: dict | None, page: Page) -> None:
    args_obj = parse_args(args)

    main_page.go_to_studying_plan_page(page)

    subject_combobox = studying_plan_page.get_switch_subject_combobox(page)
    class_combobox = studying_plan_page.get_switch_class_combobox(page)

    subject_combobox.click()
    subject_options = studying_plan_page.get_available_options_list(page)

    for subject_index, subject_opt in enumerate(subject_options):
        logger.info(f"Selecting subject {subject_opt.inner_text()}")
        subject_opt.click()

        class_combobox.click()
        class_options = studying_plan_page.get_available_options_list(page)

        for class_index, class_opt in enumerate(class_options):
            logger.info(f"Selecting class {class_opt.inner_text()}")
            class_opt.click()

            semester_radios = [studying_plan_page.get_semester_radio(i, page) for i in range(1, 3)]

            for semester_r in semester_radios:
                logger.info(f"Selecting semester {semester_r.inner_text()}")
                semester_r.click()

                if args_obj.action == LinkAction.LINK:
                    studying_plan_page.try_link_all_dates_to_lessons(page)

                if args_obj.action == LinkAction.UNLINK:
                    studying_plan_page.try_unlink_all_dates_to_lessons(page)

            if class_index < len(class_options) - 1:
                class_combobox.click()

        if subject_index < len(subject_options) - 1:
            subject_combobox.click()
