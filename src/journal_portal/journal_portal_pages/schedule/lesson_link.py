from playwright.sync_api import Locator
from pydantic import BaseModel


class LessonLinkDetails(BaseModel):
    name: str
    class_name: str
    group_name: str
    lesson_number: str

    def key(self):
        return f"{self.lesson_number} {self.name} {self.class_name} {self.group_name}"


def is_lesson_planned_for_online(btn: Locator):
    return btn.locator("span", has_text="Заплановано").count() > 0


def is_lesson_online(btn: Locator):
    return btn.locator("span", has_text="Онлайн").count() > 0


def get_lesson_details(lesson_link: Locator):
    return LessonLinkDetails(
        name=lesson_link.locator("span").nth(1).inner_text(),
        class_name=lesson_link.locator("span").nth(2).inner_text(),
        group_name=lesson_link.locator("span").nth(3).inner_text(),
        lesson_number=lesson_link.locator("span").nth(0).inner_text(),
    )
