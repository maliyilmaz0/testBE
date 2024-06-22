import os
from config.mail_config import MailType
from services.logger_service import LoggerService
from services.db_service import DBService
from services.mail_service import SMTPMailService, APIMailService
from services.repo_service import RepositoryService
from utilities.helpers.db_connector_helper import PostgreHelper
from config.global_config import global_config
from config.log_configuration import LogType, LogLocation
from controllers.auth_controller import AuthController
from routing.auth_routes import AuthRouter
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
import psycopg2

import asyncio


def create_logger():
    logger_service = LoggerService()
    logger_service.log(LogType.INFO, LogLocation.CONSOLE, "logger created...")
    return logger_service


async def create_db_helper(db_type, logger):
    match db_type:
        case "POSTGRESQL":
            connect = await asyncio.to_thread(
                psycopg2.connect,
                database=global_config["db_name"],
                user=global_config["db_username"],
                host=global_config["db_host"],
                port=global_config["db_port"],
                password=global_config["db_password"])
            cursor = connect.cursor(cursor_factory=RealDictCursor)
            db_helper = PostgreHelper(connect, cursor)
            logger.log(LogType.INFO, LogLocation.CONSOLE, f"database connection helper created for {db_type}...")
            return db_helper
        case "MYSQL":
            pass
        case "SQLSERVER":
            pass
        case "SQLITE":
            pass


def create_db_service(db_type, table_name, db_helper, logger):
    match db_type:
        case "POSTGRESQL":
            logger.log(LogType.INFO, LogLocation.CONSOLE, f"Created Database Service For {table_name}...")
            return DBService(db_helper, table_name)
        case "MYSQL":
            pass
        case "SQLSERVER":
            pass
        case "SQLITE":
            pass


def initialize_logger():
    print("Initializing application...")
    logger_service = create_logger()
    return logger_service


async def initialize_repository_service(app: FastAPI, logger_service):
    db_helper = await create_db_helper(global_config["db_type"], logger_service)
    user_service = create_db_service(global_config["db_type"], "users", db_helper, logger_service)
    user_detail_service = create_db_service(global_config["db_type"], "userdetails", db_helper, logger_service)
    role_service = create_db_service(global_config["db_type"], "roles", db_helper, logger_service)
    horoscope_service = create_db_service(global_config["db_type"], "horoscopes", db_helper, logger_service)

    app.add_event_handler('shutdown', db_helper.shut_down_connection)

    repository_service = RepositoryService(
        user_service=user_service,
        user_details=user_detail_service,
        horoscopes=horoscope_service,
        roles=role_service
    )
    return repository_service


def initialize_mail_service(mailType: MailType, logger: LoggerService):
    match mailType:
        case MailType.SMTP:
            mail_service = SMTPMailService(
                host=global_config['smtp_host'],
                port=global_config['smtp_port'],
                username=global_config['smtp_username'],
                password=global_config['smtp_pass']
            )
            logger.log(log_type=LogType.INFO, log_location=LogLocation.CONSOLE, msg=f"Created Mail Service with [SMTP]")
            return mail_service
        case MailType.API:
            mail_service = APIMailService(None, None, None, None)
            return mail_service
    return None


async def initialize_routers(app: FastAPI, repo_service, logger):
    mail_service = initialize_mail_service(MailType.SMTP, logger)
    controller = AuthController(logger, repo_service, mail_service=mail_service)
    auth_router = AuthRouter(controller).register_routes()
    app.include_router(router=auth_router)


async def initialize_dependencies(app: FastAPI):
    logger = initialize_logger()
    repo_service = await initialize_repository_service(app, logger)
    await initialize_routers(app, repo_service, logger)
