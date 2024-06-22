import sys

from abc import ABC, abstractmethod
from colorama import Fore, init
from threading import Thread
from datetime import datetime, timedelta
from psycopg2 import sql
from config.log_configuration import LogType
from logging.handlers import TimedRotatingFileHandler
import schedule
import logging
import os
import glob

init()


# database logging operation
# console logging operation
# file logging operation

class DbHandler(logging.Handler):
    def __init__(self, connection, cursor, table_name='logs'):
        super().__init__()
        self.__connection = connection
        self.__cursor = cursor
        self.__table_name = table_name

    def emit(self, record):
        query = sql.SQL(
            'INSERT INTO {} (level, message, created_at) VALUES (%s, %s, %s).format(sql.Identifier(self.__table_name)')
        with self.__connection, self.__cursor as cursor:
            cursor.execute(query, (record.levelname, record.msg, datetime.utcnow()))
            cursor.commit()


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA
    }

    def format(self, record):
        log_level = record.levelname
        color = self.COLORS.get(log_level, Fore.RESET)
        timestamp = self.formatTime(record, self.datefmt)
        log_message = '[{}{}] - [{}] - [{}]{}'.format(color, timestamp, log_level, record.getMessage(), Fore.RESET,
                                                      Fore.RESET)

        return log_message


class LoggerHelper(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def log(self, logType: LogType, msg):
        pass

    @abstractmethod
    def _log_info(self, message):
        pass

    @abstractmethod
    def _log_warning(self, message):
        pass

    @abstractmethod
    def _log_error(self, message):
        pass

    @abstractmethod
    def _log_debug(self, message):
        pass


class ConsoleLogger(LoggerHelper):

    def __init__(self):
        self.__setup_logger()
        super().__init__()

    def __setup_logger(self):
        self.__logger = logging.getLogger('console_logger')
        self.__logger.setLevel(logging.DEBUG)
        self.__formatter = ColoredFormatter('{asctime} - {levelname} - {message}', style='{',
                                            datefmt='%Y-%m-%d %H:%M:%S')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(console_handler)

    def log(self, logType: LogType, msg):
        match logType:
            case LogType.INFO:
                self._log_info(msg)
            case LogType.DEBUG:
                self._log_debug(msg)
            case LogType.WARNING:
                self._log_warning(msg)
            case LogType.ERROR:
                self._log_error(msg)

    def _log_info(self, message):
        self.__logger.setLevel(logging.INFO)
        self.__logger.info(message)

    def _log_warning(self, message):
        self.__logger.setLevel(logging.WARNING)
        self.__logger.warning(message)

    def _log_error(self, message):
        self.__logger.setLevel(logging.ERROR)
        self.__logger.error(message)

    def _log_debug(self, message):
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.debug(message)


class FileLogger(LoggerHelper):
    def __init__(self, log_file_path: str, retention_period: int = 45):
        self.__log_direction = log_file_path
        self.__retention_period_day = retention_period
        schedule.every().day.at("00:01").do(self.__cleanup_old_log_files_threaded)
        if not os.path.exists(self.__log_direction):
            os.makedirs(self.__log_direction)
        self.__setup_logger()
        super().__init__()

    def log(self, logType: LogType, msg):
        match logType:
            case LogType.INFO:
                self._log_info(msg)
            case LogType.DEBUG:
                self._log_debug(msg)
            case LogType.WARNING:
                self._log_warning(msg)
            case LogType.ERROR:
                self._log_error(msg)

    def _log_info(self, message):
        self.__logger.setLevel(logging.INFO)
        self.__logger.info(message)

    def _log_warning(self, message):
        self.__logger.setLevel(logging.WARNING)
        self.__logger.warning(message)

    def _log_error(self, message):
        self.__logger.setLevel(logging.ERROR)
        self.__logger.error(message)

    def _log_debug(self, message):
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.debug(message)

    def __cleanup_old_log_files_threaded(self):
        t = Thread(target=self.__cleanup_old_logs)
        t.start()

    def __cleanup_old_logs(self):
        cutoff_date = datetime.now() - timedelta(days=self.__retention_period_day)
        old_log_files = glob.glob(os.path.join(self.__log_direction, "*.log"))
        for log_file in old_log_files:
            file_date_str = os.path.splitext(os.path.basename(log_file))
            file_date = datetime.strptime(file_date_str[0], "%Y-%m-%d")

            if file_date < cutoff_date:
                os.remove(log_file)
        pass

    def get_filePath(self) -> str:
        date = datetime.now().strftime("%Y-%m-%d")
        file_name = f"{date}.log"
        full_path = os.path.join(self.__log_direction, file_name)
        return full_path

    def __setup_logger(self):
        self.__logger = logging.getLogger('file_logger')
        self.__logger.setLevel(logging.DEBUG)
        self.__formatter = logging.Formatter('[{asctime}] - [{levelname}] - [{message}]', style='{',
                                             datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = TimedRotatingFileHandler(self.get_filePath(), when='midnight',
                                                backupCount=self.__retention_period_day)
        file_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(file_handler)


class DBLogger(LoggerHelper):
    def __init__(self, connection, cursor, table_name='logs'):
        self.__logger = logging.getLogger('db_logger')
        self.__logger.setLevel(logging.DEBUG)
        self.__formatter = logging.Formatter('{asctime} - {levelname} - {message}', style='{',
                                             datefmt='%Y-%m-%d %H:%M:%S')
        db_handler = DbHandler(connection, cursor, table_name)
        db_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(db_handler)
        super().__init__()

    def log(self, logType: LogType, msg):
        match logType:
            case LogType.INFO:
                self._log_info(msg)
            case LogType.DEBUG:
                self._log_debug(msg)
            case LogType.WARNING:
                self._log_warning(msg)
            case LogType.ERROR:
                self._log_error(msg)

    def _log_info(self, message):
        self.__logger.setLevel(logging.INFO)
        self.__logger.info(message)

    def _log_warning(self, message):
        self.__logger.setLevel(logging.WARNING)
        self.__logger.warning(message)

    def _log_error(self, message):
        self.__logger.setLevel(logging.ERROR)
        self.__logger.error(message)

    def _log_debug(self, message):
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.debug(message)
