from utilities.validations import auth_validations as validation
from utilities.helpers.password_helper import PasswordHelper
from utilities.helpers.unique_codes import generate_verification_code
from services.repo_service import RepositoryService
from services.logger_service import LoggerService
from config.log_configuration import LogType, LogLocation

import datetime
import uuid


class UserCases:

    @staticmethod
    async def createUser(body: validation.RegisterBody, repository: RepositoryService, logger: LoggerService):
        try:
            roles = await repository.repositories['role'].get_data_by_query(conditions={'name': 'USER'},
                                                                            conjunction="AND", params=None,
                                                                            aritmetic_operator="=")
            horoscope = await repository.repositories['horoscope'].get_data_by_id(body.horoscope_id)
            born_date = datetime.datetime.strptime(body.born_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
            verification_code = generate_verification_code()
            user_data = {
                "id": str(uuid.uuid4()),
                "first_name": body.first_name,
                "last_name": body.last_name,
                "password_hash": PasswordHelper.encrypt_password(body.password).decode(),
                "email": body.email,
                "role_id": roles[0]['id'],
                "registration_date": str(datetime.datetime.utcnow().isoformat()),
                "is_suspended": False,
                "is_frozen": False,
                "frozen_code": None,
                "updated_at": str(datetime.datetime.utcnow().isoformat()),
                "is_verified": '0',
                "verification_code": verification_code
            }
            user_details_data = {
                "id": str(uuid.uuid4()),
                "user_id": user_data['id'],
                "avatar": horoscope['image'],
                "born_date": str(born_date),
                "horoscope_id": body.horoscope_id,
                "updated_at": str(datetime.datetime.utcnow().isoformat()),
            }
            await repository.repositories['user'].insert_data(user_data)
            await repository.repositories['user-detail'].insert_data(user_details_data)
            return {"id": user_data['id'], "verification_code": user_data['verification_code']}
        except Exception as e:
            logger.log(log_type=LogType.ERROR, log_location=LogLocation.FILE_CONSOLE, msg=e.message)

    @staticmethod
    async def get_user_query(repository: RepositoryService, condition, conjuction, aritmetic, param=None):
        return await repository.repositories['user'].get_data_by_query(conditions=condition, conjunction=conjuction,
                                                                       aritmetic_operator=aritmetic, params=param)

    @staticmethod
    async def get_user_by_id(repository: RepositoryService, params=None):
        return await repository.repositories['user'].get_data_by_id(params['id'])

    async def delete_user(self):
        pass

    async def get_all_users(self):
        pass

    @staticmethod
    async def update_user(repository: RepositoryService, params=None):
        return await repository.repositories['user'].update_data(params['id'], params['user'])
