from enum import Enum

from playwright.sync_api import Page

from src.admin_portal.actions.admin_platform_pages import home_page
from src.admin_portal.actions.admin_platform_pages.school_calendar import school_calendar_page
from src.admin_portal.domain.calendar_school_type import CalendarSchoolType


def generate_calendar_weeks_for_school_from_first_week_to_today(calendar_type: CalendarSchoolType, page: Page):
    if calendar_type == CalendarSchoolType.HIGH_SCHOOL:
        home_page.go_to_high_schedule_page(page)

    if calendar_type == CalendarSchoolType.JUNIOR:
        home_page.go_to_junior_schedule_page(page)

    if calendar_type == CalendarSchoolType.INDIVIDUAL:
        home_page.go_to_individual_schedule_page(page)

    current_week = school_calendar_page.get_current_week_sequence_number(page)

    while current_week > 0:
        school_calendar_page.click_on_generate_week(page)
        school_calendar_page.click_on_previous_week_link(page)

        current_week -= 1
