import secrets


def generate_verification_code(len=16):
    return secrets.token_urlsafe(len)


def generate_forgot_pass_code(len=16):
    return secrets.token_urlsafe(len)


def generate_otp_code():
    pass
