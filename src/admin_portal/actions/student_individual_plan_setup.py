import datetime
import pathlib
import re

from playwright.sync_api import Page
from pydantic import BaseModel


from src import alarms_schedule
from src.admin_portal.actions.shared import breadcrumbs, home_page, student_individual_plan_add_subject_page, student_individual_plan_calendar_alarms_schedule_add_alarm_page, student_individual_plan_calendar_alarms_schedule_page, student_individual_plan_calendar_page, student_individual_plan_calendar_schedule_add_lesson_page, student_individual_plan_calendar_schedule_page, student_individual_plan_page, student_individual_plan_subjects_list_page, student_page, students_list_page
from src.admin_portal.domain.individual_student_schedule import IndividualHomeBasedSubjectSchedule, read_schedule_from_file
from src.alarms_schedule import AlarmSchedule


class SubjectSetup(BaseModel):
    subject: str
    teacher_surname: str
    room: str
    hours_per_week: float



def get_subject_setup(lesson_schedules: list[IndividualHomeBasedSubjectSchedule]) -> list[SubjectSetup]:

    res = {}
    for lesson_schedule in lesson_schedules:
        key = lesson_schedule.subject

        if key in res:
            continue

        teacher_name_parts = lesson_schedule.teacher.split()
        if len(teacher_name_parts) <= 1:
            teacher_name_parts = lesson_schedule.teacher.split(".")


        res[key] = SubjectSetup(
            subject=lesson_schedule.subject,
            teacher_surname=([n for n in teacher_name_parts if len(n) > 2][0] if lesson_schedule.teacher else ""),
            room=lesson_schedule.room or "0",
            hours_per_week=lesson_schedule.hours_per_week,
        )

    return list(res.values())




def set_up_subjects(
    student_name: str, lesson_schedules: list[IndividualHomeBasedSubjectSchedule], individual_plan_start_date: datetime.date, page: Page
):
    home_page.go_to_students_list_page(page)
    students_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    student_individual_plan_page.go_to_individual_plan_subjects_list_page(page)

    subject_setups = get_subject_setup(lesson_schedules)
    
    for subject_setup in subject_setups:

        if student_individual_plan_subjects_list_page.is_subject_exists(subject_setup.subject, page):
            print(f"Subject {subject_setup.subject} already exists for {student_name}. Skipping.")
            continue

        student_individual_plan_subjects_list_page.go_to_add_new_subject_group(page)
        
        student_individual_plan_add_subject_page.select_subject(subject_setup.subject, page)
        student_individual_plan_add_subject_page.fill_hours_per_week(subject_setup.hours_per_week, page)
        student_individual_plan_add_subject_page.fill_start_date(individual_plan_start_date, page)
        student_individual_plan_add_subject_page.select_teacher(subject_setup.teacher_surname, page)
        student_individual_plan_add_subject_page.submit_form(page)
        

# ---


def set_up_schedule(
    student_name: str,
    lesson_schedules: list[IndividualHomeBasedSubjectSchedule],
    alarm_schedule: list[AlarmSchedule],
    page: Page,
):

    home_page.go_to_students_list_page(page)
    students_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    student_individual_plan_page.go_to_calendar_page(page)
    student_individual_plan_calendar_page.go_to_schedule_page(page)
    

    for lesson_schedule in lesson_schedules:
        if lesson_schedule.week_number == 1:
            student_individual_plan_calendar_schedule_page.try_select_week(student_individual_plan_calendar_schedule_page.WeekName.WEEK_A, page)
                        
        if lesson_schedule.week_number == 2:
            student_individual_plan_calendar_schedule_page.try_select_week(student_individual_plan_calendar_schedule_page.WeekName.WEEK_B, page)

        if student_individual_plan_calendar_schedule_page.is_lesson_exists(lesson_schedule.day_of_week, lesson_schedule.subject, page) > 0:
            print(
                f"Lesson for {lesson_schedule.subject} on {lesson_schedule.day_of_week} already exists for {student_name}. Skipping."
            )
            continue

        lesson_alarm = next(
            (alarm for alarm in alarm_schedule if alarm.lesson_number == lesson_schedule.lesson_number),
            AlarmSchedule(lesson_number=lesson_schedule.lesson_number, time_from="08:30", time_to="09:15"),
        )
        
        student_individual_plan_calendar_schedule_page.go_to_add_lesson_page(page)
        
        student_individual_plan_calendar_schedule_add_lesson_page.select_day_of_week(lesson_schedule.day_of_week, page)
        student_individual_plan_calendar_schedule_add_lesson_page.select_start(lesson_alarm.time_from, page)
        student_individual_plan_calendar_schedule_add_lesson_page.select_room(str(lesson_schedule.room), page)
        student_individual_plan_calendar_schedule_add_lesson_page.select_subject(lesson_schedule.subject, page)
        student_individual_plan_calendar_schedule_add_lesson_page.submit(page)


# ---



def set_up_alarm_schedule(student_name: str, alarm_schedule: list[AlarmSchedule], page: Page) -> None:
    """
    Set the alarm schedule for the specific student.
    """
    
    home_page.go_to_students_list_page(page)
    students_list_page.go_to_student_page(student_name, page)
    student_page.go_to_individual_plan_page(page)
    student_individual_plan_page.go_to_calendar_page(page)
    student_individual_plan_calendar_page.go_to_alarms_schedule_page(page)

    for schedule in alarm_schedule:
        if student_individual_plan_calendar_alarms_schedule_page.is_alarm_lesson_exists(schedule.lesson_number, page):
            print(f"Alarm for {student_name} for lesson {schedule.lesson_number} already exists. Skipping.")
            continue

        student_individual_plan_calendar_alarms_schedule_page.go_to_add_alarm_page(page)
        student_individual_plan_calendar_alarms_schedule_add_alarm_page.fill_lesson_number(schedule.lesson_number, page)
        student_individual_plan_calendar_alarms_schedule_add_alarm_page.fill_start_time(schedule.time_from, page)
        student_individual_plan_calendar_alarms_schedule_add_alarm_page.fill_end_time(schedule.time_to, page)
        student_individual_plan_calendar_alarms_schedule_add_alarm_page.submit(page)


# ---


def setup_complete_individual_plan(
    student_name: str,
    schedule_plan_path: pathlib.Path,
    individual_plan_start_date: datetime.date,
    page: Page):
    
    set_up_alarm_schedule(
        student_name=student_name,
        alarm_schedule=alarms_schedule.high_school_alarms,
        page=page,
    )
    breadcrumbs.go_home_page(page)

    lesson_schedules = read_schedule_from_file(schedule_plan_path)

    set_up_subjects(
        student_name=student_name,
        lesson_schedules=lesson_schedules,
        individual_plan_start_date=individual_plan_start_date,
        page=page,
    )
    breadcrumbs.go_home_page(page)
    
    set_up_schedule(
        student_name=student_name,
        lesson_schedules=lesson_schedules,
        alarm_schedule=alarms_schedule.high_school_alarms,
        page=page,
    )