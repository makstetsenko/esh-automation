from enum import StrEnum
import pathlib

from pydantic import BaseModel

from src.action_description_factory.action_descriptor_validator import raise_error_if_invalid_args


class ActionName(StrEnum):

    ### ADMIN ACTIONS ###
    ADMIN__BREADCRUMBS_NAVIGATE_HOME = "admin__breadcrumbs_navigate_home"
    ADMIN__DISTRIBUTE_STUDENTS_IN_CLASS = "admin__distribute_students_in_class"

    ADMIN__REPORTS__GET_ALL_STUDENTS = "admin__reports__get_all_students"
    ADMIN__REPORTS__GET_ALL_SUBJECTS = "admin__reports__get_all_subjects"
    ADMIN__REPORTS__GET_ALL_TEACHERS = "admin__reports__get_all_teachers"
    ADMIN__REPORTS__TEACHING_LOAD = "admin__reports__teaching_load"

    ADMIN__CALENDAR__GENERATE_CALENDAR_WEEKS_FOR_SCHOOL_FROM_FIRST_WEEK_TO_TODAY = (
        "admin__calendar__generate_calendar_weeks_for_school_from_first_week_to_today"
    )
    ADMIN__CALENDAR__REMOVE_CALENDAR_WEEKS_FOR_CLASS_UNTIL_STOP_DATE = (
        "admin__calendar__remove_calendar_weeks_for_class_until_stop_date"
    )
    ADMIN__CALENDAR__REMOVE_CALENDAR_WEEKS_FOR_INDIVIDUAL_STUDENT_UNTIL_STOP_DATE = (
        "admin__calendar__remove_calendar_weeks_for_individual_student_until_stop_date"
    )
    ADMIN__CALENDAR__REMOVE_CALENDAR_WEEKS_FOR_SCHOOL_FROM_FIRST_WEEK_TO_TODAY = (
        "admin__calendar__remove_calendar_weeks_for_school_from_first_week_to_today"
    )

    ADMIN__SCHEDULE__REMOVE_SCHEDULE_FOR_STUDENT = "admin__schedule__remove_schedule_for_student"
    ADMIN__SCHEDULE__REMOVE_SCHEDULE_SUBJECTS_FOR_STUDENT = "admin__schedule__remove_schedule_subjects_for_student"

    # these 3 actions are required if we need to setup completely new schedule for student on individual studying plan
    ADMIN__INDIVIDUAL_PLAN__SET_UP_ALARM_SCHEDULE = "admin__individual_plan__set_up_alarm_schedule"
    ADMIN__INDIVIDUAL_PLAN__SET_UP_SUBJECTS = "admin__individual_plan__set_up_subjects"
    ADMIN__INDIVIDUAL_PLAN__SET_UP_SCHEDULE = "admin__individual_plan__set_up_schedule"
    ###
    ### END OF ADMIN ACTIONS

    ### JOURNAL ACTIONS ###
    JOURNAL__GRADING__GRADE_STUDENTS = "journal__grading__grade_students"
    JOURNAL__GRADING__REMOVE_GRADES_FROM_STUDENTS = "journal__grading__remove_grades_from_students"
    JOURNAL__SCHEDULE__MARK_LESSONS_AS_ONLINE = "journal__schedule__mark_lessons_as_online"
    ### END OF JOURNAL ACTIONS ###


class TargetPlatform(StrEnum):
    ADMIN = "admin"
    JOURNAL = "journal"


class ActionDescriptor(BaseModel):
    name: ActionName
    args: dict | None = None
    next: ActionDescriptor | None = None
    target_platform: TargetPlatform


def read_from_yaml_file(file_path: pathlib.Path) -> ActionDescriptor:
    import yaml

    with open(file_path.as_posix(), "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    descriptor = ActionDescriptor.model_validate(data)

    raise_error_if_invalid_args(descriptor.name, descriptor.args)

    return descriptor
