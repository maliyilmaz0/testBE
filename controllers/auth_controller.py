import datetime
from fastapi import BackgroundTasks
import jwt

from services.mail_service import BaseMailService
from .base import BaseController
from config.log_configuration import LogLocation, LogType
from config.jwt_config import ExpireType
from utilities.validations import auth_validations as validations
from utilities.helpers.response_generator import generate_response
from utilities.helpers.link_helper import generate_verify_link, generate_forgot_pass_link
from jobs.base import celery_run_job
from jobs.send_email_job import SendEmailJob
from services.repo_service import RepositoryService
from services.logger_service import LoggerService
from services.jwt_service import JwtService
from cases.user_usecases import UserCases
from utilities.helpers.password_helper import PasswordHelper


class AuthController(BaseController):
    def __init__(self, logger: LoggerService, repositoryService: RepositoryService, mail_service: BaseMailService):
        super().__init__(logger, repositoryService)
        self.mail_service = mail_service

    async def register(self, body: validations.RegisterBody, background_tasks: BackgroundTasks):
        is_found_account = await UserCases.get_user_query(
            repository=self._repositoryService, condition={'email': body.email}, conjuction='AND', aritmetic="=",
            param=None
        )

        if is_found_account:
            self._logger.log(
                log_type=LogType.WARNING,
                log_location=LogLocation.FILE_CONSOLE,
                msg="Attempt to register again with an email already existing in the system."
            )
            return generate_response({}, "This email or phone number is in use.", "", 400)
        data = await UserCases.createUser(body=body, repository=self._repositoryService, logger=self._logger)

        if data:
            self._logger.log(
                log_type=LogType.INFO,
                log_location=LogLocation.FILE_CONSOLE,
                msg=f"New User joined us. [{data['id']}"
            )
            background_tasks.add_task(
                self.__send_verify_email,
                email=body.email,
                data=data
            )
            return generate_response({},
                                     "You have successfully registered. Please check your email to confirm and verify "
                                     "your email account.",
                                     "", 201)
        else:
            return generate_response({}, "An error occurred while registering.", "", 500)

    async def login(self, body: validations.LoginBody):
        user_data = await UserCases.get_user_query(
            repository=self._repositoryService,
            condition={'email': body.email},
            aritmetic="=", conjuction="AND", param=None)

        if not user_data or len(user_data) == 0:
            return generate_response({}, "Wrong email", "", 404)

        if int(user_data[0]['is_verified']) == 0:
            return generate_response({}, "You need to verify your email address", "", 401)

        if not PasswordHelper.compare_passwords(
                salt_password=body.password,
                encrypted_password=user_data[0]['password_hash'].encode('utf-8')
        ):
            return generate_response({}, "Wrong Password", "", 400)
        token = JwtService.create_token(data={'id': user_data[0]['id']}, expire_count=7, expire_type=ExpireType.DAY)
        return generate_response({"token": token, "expireDate": datetime.datetime.now() + datetime.timedelta(days=7)}, "Logging in", "HOME_PAGE", 200)

    async def verify_email(self, email_verification_token: str, user: str):
        found_user = await UserCases.get_user_by_id(repository=self._repositoryService, params={'id': user})
        if not user:
            return generate_response({}, "Invalid User", "", 404)

        condition = found_user['is_verified'] == '1' and found_user["verification_code"] == ""
        if condition:
            return generate_response({}, "Already verified", "", 400)
        elif email_verification_token == found_user['verification_code']:
            found_user['is_verified'] = '1'
            found_user['verification_code'] = ""

            await UserCases.update_user(repository=self._repositoryService,
                                        params={"id": found_user['id'], "user": found_user})
            self._logger.log(
                log_location=LogLocation.FILE_CONSOLE,
                log_type=LogType.INFO,
                msg=f"User [{found_user['id']}] has been verified email"
            )
            return generate_response({}, "Email Has been verified", "LOGIN_PAGE", 200)
        else:
            self._logger.log(
                log_location=LogLocation.FILE_CONSOLE,
                log_type=LogType.WARNING,
                msg=f"CRITICAL REQUEST [{found_user['id']}] try to send wrong verification code"
            )
            return generate_response({}, "Wrong verification Code", "", 403)

    async def forgot_password(self, body: validations.ForgotPasswordBody, background_tasks: BackgroundTasks):
        found_user = await UserCases.get_user_query(
            repository=self._repositoryService,
            aritmetic="=",
            conjuction="AND",
            param=None, condition={'email': body.email})
        if not found_user:
            return generate_response({}, "Invalid email address", "", 400)
        background_tasks.add_task(
            func=self.__send_forgot_pass_email,
            id=found_user[0]['id'],
            email=found_user[0]['email'],
        )
        
        return generate_response({}, "Forgot password email has been sent to your mail. Please check your mail...", "",
                                 200)

    async def forgot_password_confirm(self, body: validations.ForgotPasswordConfirm):
        try:
            decoded = JwtService.verify_token(body.token)
            print(decoded)
            is_found_user = await UserCases.get_user_query(
                repository=self._repositoryService,
                aritmetic="=",
                condition={'id': decoded['id'], "email": decoded['email']},
                conjuction="AND",
                param=None)
            if is_found_user is None or len(is_found_user) == 0:
                self._logger.log(LogType.WARNING, LogLocation.FILE_CONSOLE, f"Someone try to reset password this account [{decoded['email']}]")
                return generate_response({}, "Invalid User", "", 400)
            
            if PasswordHelper.compare_passwords(salt_password=body.new_password, encrypted_password=is_found_user[0]['password_hash'].encode('utf-8')):
                return generate_response({}, "The new password must not be the same as the old one.", "", 400)
            
            is_found_user[0]['password_hash'] = PasswordHelper.encrypt_password(body.new_password).decode()
            await UserCases.update_user(repository=self._repositoryService, params={'id': is_found_user[0]['id'], 'user': is_found_user[0]})
            self._logger.log(LogType.INFO, LogLocation.FILE_CONSOLE, f"[{decoded['id']}] has been changed his/her password")            
            return generate_response({}, "Success", "", 200)
        except Exception as e:
            print(e)
            return generate_response({}, "Invalid token", e, 400)
            
        pass

    async def otp_auth(self, body: validations.OTPBody):
        pass

    async def logout(self):
        pass

    async def __send_forgot_pass_email(self, id,email):
        # todo jwt integration for short term token for forgot-pass
        secret_token = JwtService.create_token(data={"id": id, "email": email},expire_count=7, expire_type=ExpireType.MINUTE)
        await celery_run_job(job_class=SendEmailJob,
                             mail_service=self.mail_service,
                             to=email,
                             subject="Forgot Password | Noreply",
                             message=generate_forgot_pass_link(secret_token))

    async def __send_verify_email(self, email, data):
        await celery_run_job(job_class=SendEmailJob,
                             mail_service=self.mail_service,
                             to=email,
                             subject="Verify Email | Noreply",
                             message=generate_verify_link(user_id=data['id'],
                                                          verification_code=data['verification_code']))
