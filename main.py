from src.browser import create_browser
from playwright.sync_api import sync_playwright
from src.actions.admin_portal.induvidual_schedule_setup import student_alarm_schedule, lesson_schedule
from src.actions.admin_portal import home
from src.models.individual_home_based_instruction import IndividualHomeBasedSubjectSchedule, get_schedule

from src.alarms_schedule import LessonAlarmSchedule, high_school_alarms

SCHOOL_PORTAL_URL = "https://eschool-ua.com/portal"


def main():
    with sync_playwright() as p:
        context = create_browser(p)

        page = context.pages[0] if context.pages else context.new_page()

        page.goto(SCHOOL_PORTAL_URL)

        with page.expect_popup() as admin_page_info:
            page.get_by_role("link", name="Адміністрування Адміністрування").click()
            admin_page = admin_page_info.value
            admin_page.wait_for_load_state("networkidle")

        students = [
            # (
            #     "Криловський Євген Євгенович",
            #     "./data/admin_portal/individual_plan_schedule/krylovskyi.csv",
            # ),
            ("Білоус Тимур Вікторович", "./data/admin_portal/individual_plan_schedule/bilous.csv"),
            ("Кононенко Андрій Максимович", "./data/admin_portal/individual_plan_schedule/kononenko.csv"),
            ("Береговий Андрій Ярославович", "./data/admin_portal/individual_plan_schedule/berehovyi.csv"),
        ]

        for student_name, schedule_file in students:
            home.go_home_page(admin_page)
            student_alarm_schedule.set_alarm_schedule(
                student_name=student_name,
                alarm_schedule=high_school_alarms,
                admin_page=admin_page,
            )

            lesson_schedules = get_schedule(schedule_file)

            home.go_home_page(admin_page)
            lesson_schedule.set_up_individual_plan_subjects(
                student_name=student_name,
                lesson_schedules=lesson_schedules,
                admin_page=admin_page,
            )

            home.go_home_page(admin_page)
            lesson_schedule.set_up_lessons_schedule(
                student_name=student_name,
                lesson_schedules=lesson_schedules,
                alarm_schedule=high_school_alarms,
                admin_page=admin_page,
            )

        context.close()


if __name__ == "__main__":
    main()
