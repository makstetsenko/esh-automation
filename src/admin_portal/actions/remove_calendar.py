import datetime
from enum import Enum

from playwright.sync_api import Page

from src.admin_portal.actions.shared import (
    home_page,
)
from src.admin_portal.actions.shared.school_class import class_page
from src.admin_portal.actions.shared.school_calendar import school_calendar_page
from src.admin_portal.actions.shared.school_class.calendar import class_calendar_page
from src.admin_portal.actions.shared.student import student_page
from src.admin_portal.actions.shared.student.individual_studying_form.calendar import calendar_page
from src.admin_portal.actions.shared.student.individual_studying_form import individual_studying_form_page
from src.admin_portal.actions.shared.student_alphabetical_list import student_alphabetical_list_page
from src.admin_portal.domain.calendar_school_type import CalendarSchoolType


def remove_calendar_weeks_for_school_from_first_week_to_today(calendar_type: CalendarSchoolType, page: Page):
    if calendar_type == CalendarSchoolType.HIGH_SCHOOL:
        home_page.go_to_high_schedule_page(page)

    if calendar_type == CalendarSchoolType.JUNIOR:
        home_page.go_to_junior_schedule_page(page)

    if calendar_type == CalendarSchoolType.INDIVIDUAL:
        home_page.go_to_individual_schedule_page(page)

    current_week = school_calendar_page.get_current_week_sequence_number(page)

    while current_week > 0:
        school_calendar_page.click_on_remove_week_link(page)
        school_calendar_page.click_on_previous_week_link(page)

        current_week -= 1


def remove_calendar_weeks_for_individual_student_until_no_lessons_on_page(student_name: str, page: Page):
    home_page.go_to_students_list_page(page)
    student_alphabetical_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    individual_studying_form_page.go_to_calendar_page(page)

    while True:
        calendar_page.click_on_remove_week_link(page)
        calendar_page.click_on_previous_week_link(page)

        if not calendar_page.has_any_lessons_on_calendar_page(page):
            break


def remove_calendar_weeks_for_individual_student_until_stop_date(
    student_name: str, stop_date: datetime.date, page: Page
):
    home_page.go_to_students_list_page(page)
    student_alphabetical_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    individual_studying_form_page.go_to_calendar_page(page)

    while True:
        if calendar_page.has_any_lessons_on_calendar_page(page):
            calendar_page.click_on_remove_week_link(page)

        if stop_date in calendar_page.get_dates_on_page(page):
            break

        calendar_page.click_on_previous_week_link(page)


def remove_calendar_weeks_for_class_until_stop_date(class_name: str, stop_date: datetime.date, page: Page):
    home_page.go_to_class_page(class_name, page)
    class_page.go_to_calendar_page(page)

    while True:
        if class_calendar_page.has_any_lessons_on_calendar_page(page):
            class_calendar_page.click_on_remove_week_link(page)

        if stop_date in class_calendar_page.get_dates_on_page(page):
            break

        class_calendar_page.click_on_previous_week_link(page)
