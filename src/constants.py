from enum import StrEnum


class DateFormat(StrEnum):
    dd_mm_yyyy = "%d.%m.%Y"
    dd_mm_yy = "%d.%m.%y"


class DateFormatDashes(StrEnum):
    dd_mm_yyyy = "%d-%m-%Y"


class DateFormatSlashes(StrEnum):
    dd_mm = "%d/%m"
