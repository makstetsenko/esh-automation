import datetime
from enum import Enum

from playwright.sync_api import Page

from src.admin_portal.actions.shared import (
    calendar_schedule_page,
    class_calendar_page,
    class_page,
    home_page,
    student_individual_plan_calendar_page,
    student_individual_plan_page,
    student_page,
    students_list_page,
)
from src.admin_portal.domain.calendar_school_type import CalendarSchoolType


def remove_calendar_weeks_for_school_from_first_week_to_today(calendar_type: CalendarSchoolType, page: Page):
    if calendar_type == CalendarSchoolType.HIGH:
        home_page.go_to_high_schedule_page(page)

    if calendar_type == CalendarSchoolType.JUNIOR:
        home_page.go_to_junior_schedule_page(page)

    if calendar_type == CalendarSchoolType.INDIVIDUAL:
        home_page.go_to_individual_schedule_page(page)

    current_week = calendar_schedule_page.get_current_week_sequence_number(page)

    while current_week > 0:
        calendar_schedule_page.click_on_remove_week_link(page)
        calendar_schedule_page.click_on_previous_week_link(page)

        current_week -= 1


def remove_calendar_weeks_for_individual_student_until_no_lessons_on_page(student_name: str, page: Page):
    home_page.go_to_students_list_page(page)
    students_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    student_individual_plan_page.go_to_calendar_page(page)

    while True:
        student_individual_plan_calendar_page.click_on_remove_week_link(page)
        student_individual_plan_calendar_page.click_on_previous_week_link(page)

        if not student_individual_plan_calendar_page.has_any_lessons_on_calendar_page(page):
            break


def remove_calendar_weeks_for_individual_student_until_stop_date(student_name: str, stop_date: datetime.date, page: Page):
    home_page.go_to_students_list_page(page)
    students_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    student_individual_plan_page.go_to_calendar_page(page)

    while True:
        if student_individual_plan_calendar_page.has_any_lessons_on_calendar_page(page):
            student_individual_plan_calendar_page.click_on_remove_week_link(page)
        
        if stop_date in student_individual_plan_calendar_page.get_dates_on_page(page):
            break

        student_individual_plan_calendar_page.click_on_previous_week_link(page)
        



def remove_calendar_weeks_for_class_until_stop_date(class_name: str, stop_date: datetime.date, page: Page):
    home_page.go_to_class_page(class_name, page)
    class_page.go_to_calendar_page(page)

    while True:
        if class_calendar_page.has_any_lessons_on_calendar_page(page):
            class_calendar_page.click_on_remove_week_link(page)
        
        if stop_date in class_calendar_page.get_dates_on_page(page):
            break

        class_calendar_page.click_on_previous_week_link(page)
        