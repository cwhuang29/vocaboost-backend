from enum import Enum


class AuthHistoryType(int, Enum):
    SIGNEDIN = 0
    SIGNEDOUT = 1


class LoginMethodType(int, Enum):
    PASSWORD = 0
    GOOGLE = 1
    APPLE = 2
    TWITTER = 3


class ManageWordType(int, Enum):
    ADD = 0
    REMOVE = 1
