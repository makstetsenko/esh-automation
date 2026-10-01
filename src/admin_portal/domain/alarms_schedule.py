from pydantic import BaseModel


class AlarmSchedule(BaseModel):
    lesson_number: int
    time_from: str
    time_to: str


high_school_alarms: list[AlarmSchedule] = [
    AlarmSchedule(lesson_number=1, time_from="08:30", time_to="09:15"),
    AlarmSchedule(lesson_number=2, time_from="09:25", time_to="10:10"),
    AlarmSchedule(lesson_number=3, time_from="10:20", time_to="11:05"),
    AlarmSchedule(lesson_number=4, time_from="11:25", time_to="12:10"),
    AlarmSchedule(lesson_number=5, time_from="12:30", time_to="13:15"),
    AlarmSchedule(lesson_number=6, time_from="13:25", time_to="14:10"),
    AlarmSchedule(lesson_number=7, time_from="14:20", time_to="15:05"),
    AlarmSchedule(lesson_number=8, time_from="15:15", time_to="16:00"),
    AlarmSchedule(lesson_number=9, time_from="16:10", time_to="16:55"),
]
