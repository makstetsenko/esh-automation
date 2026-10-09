import logging

from playwright.sync_api import Page

from src.action_description_factory.action_executor import admin_portal, journal_portal

from src.action_description_factory.action_descriptor import ActionDescriptor
from src.action_description_factory.action_descriptor import ActionName

logger = logging.getLogger(__name__)

EXECUTION_MAP = {
    ActionName.ADMIN__BREADCRUMBS_NAVIGATE_HOME: admin_portal.breadcrumbs_navigate_home_executor.execute,
    ActionName.ADMIN__DISTRIBUTE_STUDENTS_IN_CLASS: admin_portal.distribute_students_in_class_executor.execute,
    ActionName.ADMIN__REPORTS__GET_ALL_STUDENTS: admin_portal.global_students_list_executor.execute,
    ActionName.ADMIN__REPORTS__GET_ALL_SUBJECTS: admin_portal.global_subjects_list_executor.execute,
    ActionName.ADMIN__REPORTS__GET_ALL_TEACHERS: admin_portal.global_teachers_list_executor.execute,
    ActionName.ADMIN__REPORTS__TEACHING_LOAD: admin_portal.teaching_load_report_executor.execute,
    ActionName.ADMIN__CALENDAR__GENERATE_CALENDAR_WEEKS_FOR_SCHOOL_FROM_FIRST_WEEK_TO_TODAY: admin_portal.generate_calendar_executor.execute,
    ActionName.ADMIN__CALENDAR__REMOVE_CALENDAR_WEEKS_FOR_CLASS_UNTIL_STOP_DATE: admin_portal.remove_calendar_weeks_for_class_until_stop_date_executor.execute,
    ActionName.ADMIN__CALENDAR__REMOVE_CALENDAR_WEEKS_FOR_INDIVIDUAL_STUDENT_UNTIL_STOP_DATE: admin_portal.remove_calendar_weeks_for_individual_student_until_stop_date_executor.execute,
    ActionName.ADMIN__CALENDAR__REMOVE_CALENDAR_WEEKS_FOR_SCHOOL_FROM_FIRST_WEEK_TO_TODAY: admin_portal.remove_calendar_weeks_for_school_from_first_week_to_today_executor.execute,
    ActionName.ADMIN__SCHEDULE__REMOVE_SCHEDULE_FOR_STUDENT: admin_portal.remove_schedule_for_student_executor.execute,
    ActionName.ADMIN__SCHEDULE__REMOVE_SCHEDULE_SUBJECTS_FOR_STUDENT: admin_portal.remove_schedule_subjects_for_student_executor.execute,
    ActionName.ADMIN__INDIVIDUAL_PLAN__SET_UP_ALARM_SCHEDULE: admin_portal.student_individual_plan_set_up_alarm_schedule_executor.execute,
    ActionName.ADMIN__INDIVIDUAL_PLAN__SET_UP_SUBJECTS: admin_portal.student_individual_plan_set_up_subjects_executor.execute,
    ActionName.ADMIN__INDIVIDUAL_PLAN__SET_UP_SCHEDULE: admin_portal.student_individual_plan_set_up_schedule_executor.execute,
    ActionName.JOURNAL__GRADING__GRADE_STUDENTS: journal_portal.grade_students.execute,
    ActionName.JOURNAL__GRADING__REMOVE_GRADES_FROM_STUDENTS: journal_portal.grades_removal.execute,
    ActionName.JOURNAL__SCHEDULE__MARK_LESSONS_AS_ONLINE: journal_portal.mark_lessons_as_online.execute,
}


def execute(descriptor: ActionDescriptor, page: Page):
    logger.info(f"Executing {descriptor.name.value}")
    action = EXECUTION_MAP[descriptor.name]
    action(descriptor.args, page)
