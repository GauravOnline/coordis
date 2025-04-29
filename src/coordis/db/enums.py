from enum import StrEnum


class EventType(StrEnum):
    HOMEWORK = ("Homework",)
    ASSIGNMENT = ("Assignment",)
    QUIZ = ("Quiz",)
    PRESENTATION = ("Presentation",)
    MEETING = ("Meeting",)
    MIDTERM = ("Mid-Term",)
    FINAL = ("Final",)


__all__ = ["EventType"]
