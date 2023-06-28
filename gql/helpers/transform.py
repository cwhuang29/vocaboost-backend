import ast
from typing import Type, TypeVar

from structs.graphql.setting import SettingOut
from structs.graphql.user import UserOut
from structs.models.setting import SettingORM
from structs.models.user import UserORM
from utils.bean_utils import getProperties
from utils.enum import LoginMethodType
from utils.type import DetailedUserORMType


T = TypeVar('T')
S = TypeVar('S')

excludeFields = {'metadata', 'registry'}


def transformToGraphqlSchema(*, source: T, targetClass: Type[S]) -> S:
    target = targetClass(**getProperties(source, forbidden=excludeFields))
    return target


def transformUserOut(dbUser: UserORM, dbDetailedUser: DetailedUserORMType) -> UserOut:
    return UserOut(
        uuid=dbUser.uuid,
        loginMethod=LoginMethodType(dbUser.method),
        firstName=dbUser.firstName,
        lastName=dbUser.lastName,
        createdAt=dbUser.createdAt,
        email=dbDetailedUser.email,
        avatar=dbDetailedUser.avatar,
    )


def transformSettingOut(dbSetting: SettingORM) -> SettingOut:
    return SettingOut(
        highlightColor=dbSetting.highlightColor,
        language=dbSetting.language,
        fontSize=dbSetting.fontSize,
        showDetail=True if dbSetting.showDetail == 1 else False,
        collectedWords=ast.literal_eval(dbSetting.collectedWords),
        suspendedPages=ast.literal_eval(dbSetting.suspendedPages),
        updatedAt=dbSetting.updatedAt,
    )
