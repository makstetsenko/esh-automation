import datetime
import logging

from playwright.sync_api import Page
from pydantic import BaseModel

from src import shared_actions
from src.constants import DateFormat
from src.journal_portal.journal_portal_pages import main_page
from src.journal_portal.journal_portal_pages.journal_marks import journal_marks_page, lesson_planning_modal

logger = logging.getLogger(__name__)


class Args(BaseModel):
    start_date: datetime.date
    class_names: list[str] | None = None


def parse_args(args: dict | None):
    if args is None:
        raise ValueError("args is required")

    return Args.model_validate(args)



def proceed_with_class(args: Args, page: Page):
    start_month = args.start_date.month
    today = datetime.date.today()

    for month in range(start_month, today.month + 1):
        try:
            journal_marks_page.select_month(month, page)
        except:
            continue

        date_btns = journal_marks_page.get_all_date_buttons(page)
        
        for date_btn in date_btns:
            date_btn.button.click()
            shared_actions.wait(page, 500)
            shared_actions.wait_network_idle(page)
            
            create_hw_btn = lesson_planning_modal.get_create_homework_button(page)
            if create_hw_btn.count() == 0:
                lesson_planning_modal.close_modal(page)
                continue
            
            create_hw_btn.click()
            shared_actions.wait(page, 500)
            shared_actions.wait_network_idle(page)
            
            select_next_lesson_combobox = lesson_planning_modal.get_next_lesson_for_homework_combobox(page)
            
            if select_next_lesson_combobox.count() == 0:
                lesson_planning_modal.close_modal(page)
                continue
            
            select_next_lesson_combobox.click()
            shared_actions.wait(page, 500)
            shared_actions.wait_network_idle(page)
            
            lesson_options = journal_marks_page.get_available_options_list(page)
            
            if len(lesson_options) == 0:
                lesson_planning_modal.close_modal(page)
                continue

            
            logger.info(f"Selecting homework for date {date_btn.journal_date.date.strftime(DateFormat.dd_mm_yyyy)}")

            lesson_options[0].click()
            shared_actions.wait(page, 500)
            shared_actions.wait_network_idle(page)
            
            lesson_planning_modal.click_on_save_homework_button(page)
            
            lesson_planning_modal.close_modal(page)
            
            

def execute(args: dict | None, page: Page) -> None:
    args_obj = parse_args(args)

    main_page.go_to_journal_marks(page)


    class_combobox = journal_marks_page.get_switch_class_combobox(page)
    
    class_combobox.click()
    shared_actions.wait(page, 500)
    shared_actions.wait_network_idle(page)
    
    if args_obj.class_names is None:
        class_options = journal_marks_page.get_available_options_list(page) 
    else:
        all_options = journal_marks_page.get_available_options_list(page)
        class_options = []
        for n in args_obj.class_names:
            for o in all_options:
                if n in o.inner_text():
                    class_options.append(o)
    
    for class_index, class_opt in enumerate(class_options):
        logger.info(f"Selecting class {class_opt.inner_text()}")
       
        class_opt.click()
        shared_actions.wait(page, 500)
        shared_actions.wait_network_idle(page)
        
        subject_combobox = journal_marks_page.get_switch_subject_combobox(page)
        if subject_combobox.is_visible():
            subject_combobox.click()
            shared_actions.wait(page, 500)
            shared_actions.wait_network_idle(page)
            
            subject_options = journal_marks_page.get_available_options_list(page)
            
            for subject_index, subject_opt in enumerate(subject_options):
                logger.info(f"Selecting subject {subject_opt.inner_text()}")
                subject_opt.click()
                shared_actions.wait(page, 500)
                shared_actions.wait_network_idle(page)
                
                proceed_with_class(args_obj, page)
                
                if subject_index < len(subject_options) - 1:
                    subject_combobox.click()
                    shared_actions.wait(page, 500)
                    shared_actions.wait_network_idle(page)
        else:
            proceed_with_class(args_obj, page)
                
        
        if class_index < len(class_options) - 1:
            class_combobox.click()
            shared_actions.wait(page, 500)
            shared_actions.wait_network_idle(page)
        