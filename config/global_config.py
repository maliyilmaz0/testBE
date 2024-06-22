from dotenv import load_dotenv
import os

load_dotenv()

global_config = {
    "is_production": os.environ.get('ENVIRONMENT') == 'PRODUCTION',
    "base_url": os.environ.get('BASE_URL'),
    "api_version": os.environ.get('VERSION'),
    "api_key": os.environ.get('API_KEY'),
    "db_type": os.environ.get('DB_TYPE'),
    "db_name": os.environ.get('DB_NAME'),
    "db_username": os.environ.get('DB_USERNAME'),
    "db_password": os.environ.get('DB_PASSWORD'),
    "db_port": os.environ.get('DB_PORT'),
    "db_host": os.environ.get('DB_HOST'),
    "log_location": os.environ.get('LOG_LOCATION'),
    "smtp_port": os.environ.get('SMTP_PORT'),
    "smtp_username": os.environ.get('SMTP_USERNAME'),
    "smtp_pass": os.environ.get('SMTP_PASS'),
    "smtp_host": os.environ.get('SMTP_HOST'),
    "redis_cli": os.environ.get('REDIS_CLI'),
    "jwt_secret": os.environ.get('JWT_SECRET'),
}