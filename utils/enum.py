from enum import Enum


class AuthHistoryType(int, Enum):
    SIGNEDIN = 0
    SIGNEDOUT = 1


class LoginMethodType(int, Enum):
    PASSWORD = 0
    GOOGLE = 1
    APPLE = 2
    TWITTER = 3
    AZURE = 4


class ManageWordType(int, Enum):
    ADD = 0
    REMOVE = 1


class ClientSourceType(int, Enum):
    MOBILE = 0
    EXTENSION = 1
    UNKNOWN = 2


class ClientSourceHeaderType(str, Enum):
    MOBILE = 'mobile'
    EXTENSION = 'extension'
    UNKNOWN = 'unknown'


class DevicePlatformType(str, Enum):
    IOS = 'ios'
    ANDROID = 'android'
    UNKNOWN = 'unknown'


class RouterGroupType(str, Enum):
    AUTH = 'auth'
    USER = 'users'
    WORD = 'words'


class FONT_SIZE(str, Enum):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'


class HIGHLIGHTER_BG_COLORS(str, Enum):
    PINK = 'PINK'
    ORANGE = 'ORANGE'
    YELLOW = 'YELLOW'
    GREEN = 'GREEN'
    BLUE = 'BLUE'
    PURPLE = 'PURPLE'


class LANGS(str, Enum):
    en = 'en'
    es = 'es'
    zh_TW = 'zh_TW'
    zh_CN = 'zh_CN'


class PARTS_OF_SPEECH_SHORTHAND(str, Enum):
    noun = '(n.)'
    verb = '(v.)'
    adverb = '(adv.)'
    adjective = '(adj.)'
    preposition = '(prep.)'
    conjunction = '(conj.)'


class ONLINE_DIC_URL(str, Enum):
    en = 'https://dictionary.cambridge.org/dictionary/english/'
    es = 'https://dictionary.cambridge.org/dictionary/english-spanish/'
    zh_TW = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/'
    zh_CN = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B0%A1%E9%AB%94/'
