import datetime

from pydantic import BaseModel, Extra


class RegisterBody(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    horoscope_id: str
    born_date: str

    class Config:
        extra = Extra.forbid


class LoginBody(BaseModel):
    email: str
    password: str

    class Config:
        extra = Extra.forbid


class VerifyEmailBody(BaseModel):
    user_id: str
    verify_token: str

    class Config:
        extra = Extra.forbid


class ForgotPasswordBody(BaseModel):
    email: str

    class Config:
        extra = Extra.forbid


class ForgotPasswordConfirm(BaseModel):
    token: str
    new_password: str
    new_password_confirm: str

    class Config:
        extra = Extra.forbid


class OTPBody(BaseModel):
    user_id: str
    code: str

    class Config:
        extra = Extra.forbid


class LogoutBody(BaseModel):
    user_id: str

    class Config:
        extra = Extra.forbid
