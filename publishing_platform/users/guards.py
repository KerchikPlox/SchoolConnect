import uuid
from abc import ABC
from typing import Type, List, Optional

from fastapi import Depends, HTTPException, status


from publishing_platform.auth.service import get_current_user
from publishing_platform.users.dto import UserFAPI
from publishing_platform.users.enums import Roles

__all__ = [
    "RoleGuard",
    "RoleRanger",
    "RoleDenierSingle",
    "RoleApplierSingle",
    "RoleApplierMulti",
    "RoleDenierMulti",
]

roles_as_list = [Roles.student, Roles.teacher, Roles.admin]


access_denied_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access_denied - not enough right or your role not satisfied to some constraints",
    headers={"WWW-Authenticate": "Bearer"},
)

# -------------------- Охранные классы-зависимости, заточенные строго под свою роль/роли --------------------


class GuardInstance(ABC):
    user: Optional[UserFAPI] = None

    @staticmethod
    def __static_init__(self, user: UserFAPI = Depends(get_current_user)):
        ...


class RoleRanger:
    min_role: Roles

    @staticmethod
    def __static_init__(self, user: UserFAPI = Depends(get_current_user)):
        # берём диапазон начиная с минимально-возможной роли, включая указанную как минимальную
        allowed = roles_as_list[roles_as_list.index(self.min_role) :]

        # разрешаем если роль попадает в указанный диапазон
        if user.role not in allowed:
            raise access_denied_exception
        else:
            self.user = user


class RoleDenierSingle:
    deny_role: Roles

    @staticmethod
    def __static_init__(self, user: UserFAPI = Depends(get_current_user)):
        # запращаем если роль совпадает с запрещённой
        if user.role == self.deny_role:
            raise access_denied_exception
        else:
            self.user = user


class RoleApplierSingle:
    allow_role: Roles

    @staticmethod
    def __static_init__(self, user: UserFAPI = Depends(get_current_user)):
        # разрешаем если роль совпадает с разрешённой, иначе запрещаем
        if not (user.role == self.allow_role):
            raise access_denied_exception
        else:
            self.user = user


class RoleApplierMulti:
    allow_list: List[Roles]

    @staticmethod
    def __static_init__(self, user: UserFAPI = Depends(get_current_user)):
        # разрешаем если роль НЕ среди тех, что разрешены
        if user.role not in self.allow_list:
            raise access_denied_exception
        else:
            self.user = user


class RoleDenierMulti:
    deny_list: List[Roles]

    @staticmethod
    def __static_init__(self, user: UserFAPI = Depends(get_current_user)):
        # запрещаем если роль среди указанных к запрету
        if user.role in self.deny_list:
            raise access_denied_exception
        else:
            self.user = user


# -------------------- Класс высшего порядка, который раздаёт классы перечисленные выше --------------------


class RoleGuard:
    @classmethod
    def min_access_level(cls, min_role: Roles) -> Type[RoleRanger]:
        new_type = type(f"{RoleRanger.__name__}_{uuid.uuid4().hex}", (RoleRanger,), {})
        new_type.min_role = min_role
        new_type.__init__ = RoleRanger.__static_init__
        return new_type  # noqa / we are confident that type will be correct, because it have all needed attrs

    @classmethod
    def deny(cls, deny_role: Roles) -> Type[RoleDenierSingle]:
        new_type = type(f"{RoleDenierSingle.__name__}_{uuid.uuid4().hex}", (RoleDenierSingle,), {})
        new_type.deny_role = deny_role
        new_type.__init__ = RoleDenierSingle.__static_init__
        return new_type  # noqa / we are confident that type will be correct, because it have all needed attrs

    @classmethod
    def allow(cls, allow_role: Roles) -> Type[RoleApplierSingle]:
        new_type = type(f"{RoleApplierSingle.__name__}_{uuid.uuid4().hex}", (RoleApplierSingle,), {})
        new_type.allow_role = allow_role
        new_type.__init__ = RoleApplierSingle.__static_init__
        return new_type  # noqa / we are confident that type will be correct, because it have all needed attrs

    @classmethod
    def allow_list(cls, *allow_list: Roles) -> Type[RoleApplierMulti]:
        new_type = type(f"{RoleApplierMulti.__name__}_{uuid.uuid4().hex}", (RoleApplierMulti,), {})
        new_type.allow_list = allow_list
        new_type.__init__ = RoleApplierMulti.__static_init__
        return new_type  # noqa / we are confident that type will be correct, because it have all needed attrs

    @classmethod
    def deny_list(cls, *deny_list: Roles) -> Type[RoleDenierMulti]:
        new_type = type(f"{RoleDenierMulti.__name__}_{uuid.uuid4().hex}", (RoleDenierMulti,), {})
        new_type.deny_list = deny_list
        new_type.__init__ = RoleDenierMulti.__static_init__
        return new_type  # noqa / we are confident that type will be correct, because it have all needed attrs
