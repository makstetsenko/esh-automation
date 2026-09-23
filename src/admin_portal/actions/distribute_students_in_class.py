import datetime
import logging

from playwright.sync_api import Locator, Page

from src.admin_portal.domain.student_distribution import StudentDistribution

logger = logging.getLogger(__name__)

class RemoveStudentMovementException(Exception):
    pass


def go_to_class_page(class_name: str, page: Page) -> None:
    page.get_by_role("link", name=class_name).click()
    page.wait_for_load_state("networkidle")


def go_to_class_subject_groups_page(page: Page) -> None:
    subject_groups_link = page.get_by_role("link", name="Навчальні групи")
    subject_groups_link.wait_for(state="visible", timeout=60_000)
    subject_groups_link.click()

    page.wait_for_load_state("networkidle")


def go_to_subject_group_students_distribution_page(subject_name: str, page: Page) -> None:
    page.get_by_role("link", name=subject_name).click()
    page.wait_for_load_state("networkidle")


def try_remove_previous_movements_info(student_row: Locator, page: Page) -> None:
    edit_movements_button = student_row.locator(".edit-movements")
    edit_movements_button.click()
    page.wait_for_load_state("networkidle")

    modal_with_movements = page.locator("#edit-movements-body")
    modal_with_movements.wait_for(state="visible")
    element = modal_with_movements.element_handle()
    if element:
        element.wait_for_element_state("stable")

    close_movements_modal_button = modal_with_movements.locator("..").get_by_role("button", name="Close")

    no_movements_text = modal_with_movements.get_by_text("Переводи не знайденi")

    if no_movements_text.count() > 0:
        close_movements_modal_button.click()
        return

    remove_movement_buttons = modal_with_movements.get_by_title("Видалити")

    for b in remove_movement_buttons.all():
        with page.expect_event("dialog") as dialog_info:
            b.click()

        dialog = dialog_info.value
        
        if "Учень має виставлені:" in dialog.message:
            dialog.accept()
            page.wait_for_load_state("networkidle")
            close_movements_modal_button.click()
            raise RemoveStudentMovementException(dialog.message)
        
        dialog.accept()

    save_movement_changes_button = modal_with_movements.locator("..").get_by_role("button", name="Зберегти змiни")

    if save_movement_changes_button.count() > 0:
        save_movement_changes_button.click()

    close_movements_modal_button.click()
    page.wait_for_load_state("networkidle")

    return


def process_student_row(
    student_row: Locator,
    students_distribution: list[StudentDistribution],
    group_names: list[str],
    page: Page,
    remove_selection_if_distribution_missing: bool,
):

    student_name_cell = student_row.get_by_role("cell").first
    student_name = student_name_cell.inner_text()

    logger.info(f"Processing student {student_name}")

    selected_distribution: StudentDistribution | None = None
    for distribution in students_distribution:
        if distribution.student_surname not in student_name:
            continue

        if distribution.group_name not in group_names:
            continue

        selected_distribution = distribution
        break

    remove_selection_button = student_row.locator(".remove-part")

    if selected_distribution == None:
        logger.warning(f"Distribution for student {student_name} was not found.")

    if selected_distribution is not None or remove_selection_if_distribution_missing:
        try:
            try_remove_previous_movements_info(student_row, page)
        except RemoveStudentMovementException as ex:
            logger.error(f"Error during removing student movement: {ex}")
            logger.error(f"Skipping group assignment for student {student_name}")
            return
    
    if selected_distribution is not None:
        logger.info(f"Assigning student {student_name} to  group {selected_distribution.group_name}")

        remove_selection_button.click()

        group_index = group_names.index(selected_distribution.group_name)

        checkbox_cells = student_row.get_by_role("cell", name="", exact=True)
        checkbox_cells.nth(group_index).click()
        return

    if remove_selection_if_distribution_missing:
        logger.info(f"Clearing group selection for student {student_name}")
        remove_selection_button.click()
        return


def submit(start_date: datetime.date, page: Page) -> None:
    page.get_by_role("button", name="Надіслати").click()
    page.wait_for_load_state("networkidle")

    submit_modal = page.locator(".modal-content").filter(
        has_text="Встановити дату зарахування учня до навчальної групи"
    )

    submit_modal.wait_for(state="visible")
    element = submit_modal.element_handle()
    if element:
        element.wait_for_element_state("stable")

    start_studying_date_input = submit_modal.get_by_role("textbox", name="ДД.ММ.РР")
    start_studying_date_input.fill(start_date.strftime("%d.%m.%y"))

    # click on modal header to close date selector
    submit_modal.get_by_role("heading").click()

    submit_button = submit_modal.get_by_role("button", name="Надіслати")
    submit_button.wait_for(state="visible")
    submit_button.click()

    page.wait_for_load_state("networkidle")


def distribute_students(
    class_name: str,
    subjects: list[str],
    students_distribution: list[StudentDistribution],
    page: Page,
    studying_start_date: datetime.date,
    remove_selection_if_distribution_missing: bool,
) -> None:
    go_to_class_page(class_name, page)
    go_to_class_subject_groups_page(page)

    for subject in subjects:
        logger.info(f"Processing class {class_name} and subject {subject}")

        go_to_subject_group_students_distribution_page(subject, page)

        select_all_students_buttons = page.locator(".table").get_by_role("button", name="Обрати всіх")
        group_names = [b.locator("..").locator("div").first.inner_text() for b in select_all_students_buttons.all()]

        all_students_rows = page.locator(".table tbody tr")
        for student_row in all_students_rows.all():
            process_student_row(
                student_row, students_distribution, group_names, page, remove_selection_if_distribution_missing
            )

        submit(studying_start_date, page)
        logger.info(f"Done class {class_name} and subject {subject}")

        go_to_class_subject_groups_page(page)
