from enum import Enum


class LogLocation(Enum):
    DB = 'DB'
    CONSOLE = 'CONSOLE'
    FILE = 'FILE'

    DB_CONSOLE = 'DB_CONSOLE'
    DB_FILE = 'DB_FILE'

    FILE_CONSOLE = 'FILE_CONSOLE'

    ALL = 'ALL'


class LogType(Enum):
    INFO = 'INFO'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    DEBUG = 'DEBUG'