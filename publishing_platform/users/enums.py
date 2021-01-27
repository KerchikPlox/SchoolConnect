from enum import Enum


__all__ = [
    "Roles"
]


class Roles(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"
