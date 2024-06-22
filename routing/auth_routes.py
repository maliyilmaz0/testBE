from fastapi import APIRouter, Depends, BackgroundTasks, Path
from utilities.validations import auth_validations as validations
from controllers.auth_controller import AuthController
from config.global_config import global_config
from config.http_config import BaseResponse
from middlewares.api_key import validate_api_key


class AuthRouter:
    def __init__(self, controller: AuthController):
        self.controller = controller

    async def register(self, body: validations.RegisterBody, background_tasks: BackgroundTasks):
        return await self.controller.register(body=body, background_tasks=background_tasks)

    async def verify_email(self, email_verification_token: str = Path(...), user: str = Path(...)):
        return await self.controller.verify_email(email_verification_token, user)

    async def login(self, body: validations.LoginBody):
        return await self.controller.login(body)

    async def logout(self, request: validations.LogoutBody):
        return await self.controller.logout()

    async def forgot_password(self, body: validations.ForgotPasswordBody, background_tasks: BackgroundTasks):
        return await self.controller.forgot_password(body=body, background_tasks=background_tasks)

    async def forgot_password_confirm(self, body: validations.ForgotPasswordConfirm):
        return await self.controller.forgot_password_confirm(body)

    async def otp_auth(self, body: validations.OTPBody):
        return await self.controller.otp_auth(body)

    def register_routes(self):
        auth_router = APIRouter(prefix=f'/api/{global_config["api_version"]}/auth',
                                dependencies=[Depends(validate_api_key)], tags=["Authentication"])
        auth_router.post("/register", response_model=BaseResponse, summary="Register a new user",
                         dependencies=[Depends(validate_api_key)])(self.register)
        auth_router.put("/{user}/verify-email/{email_verification_token}", response_model=BaseResponse,
                        summary="Verify email", dependencies=[Depends(validate_api_key)])(self.verify_email)
        auth_router.post("/login", response_model=BaseResponse, summary="Login",
                         dependencies=[Depends(validate_api_key)])(self.login)
        auth_router.post("/logout", response_model=BaseResponse, summary="Logout",
                         dependencies=[Depends(validate_api_key)])(self.logout)
        auth_router.post("/forgot-password", response_model=BaseResponse, summary="Send forgot password email",
                         dependencies=[Depends(validate_api_key)])(
            self.forgot_password)
        auth_router.post("/forgot-password-confirm", response_model=BaseResponse, summary="Confirm forgot password",
                         dependencies=[Depends(validate_api_key)])(
            self.forgot_password_confirm)
        auth_router.post("/otp-auth", response_model=BaseResponse, summary="OTP authentication",
                         dependencies=[Depends(validate_api_key)])(self.otp_auth)
        return auth_router
