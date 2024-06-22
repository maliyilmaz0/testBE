from utilities.helpers.logger import FileLogger, DBLogger, ConsoleLogger
from config.global_config import global_config
from config.log_configuration import LogType, LogLocation
import os


class LoggerService:
    def __init__(self):
        full_path = os.path.join(os.getcwd(), global_config["log_location"])
        self.file_logger = FileLogger(log_file_path=full_path, retention_period=45)
        self.console_logger = ConsoleLogger()
        self.db_logger = None

    def log(self, log_type: LogType, log_location: LogLocation, msg):
        match log_location:
            case LogLocation.FILE:
                self.file_logger.log(log_type, msg)
            case LogLocation.DB:
                """TODO adding db loggin"""
            case LogLocation.CONSOLE:
                self.console_logger.log(log_type, msg)
            case LogLocation.DB_FILE:
                """TODO adding db loggin"""
                self.file_logger.log(log_type, msg)
            case LogLocation.FILE_CONSOLE:
                self.console_logger.log(log_type, msg)
                self.file_logger.log(log_type, msg)
            case LogLocation.ALL:
                self.console_logger.log(log_type, msg)
                self.file_logger.log(log_type, msg)
                """TODO adding db loggin"""
