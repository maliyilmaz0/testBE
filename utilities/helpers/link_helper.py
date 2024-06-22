from config.global_config import global_config


def generate_verify_link(user_id, verification_code):
    is_production = global_config["is_production"] == 'PRODUCTION'
    url = ""
    if is_production:
        url = f"{global_config['base_url']}/api/v1/auth/{user_id}/verify-link/{verification_code}"
    else:
        url = f"localhost:3000/api/v1/auth/{user_id}/verify-link/{verification_code}"

    return url


def generate_forgot_pass_link(secret_token):
    is_production = global_config["is_production"] == 'PRODUCTION'
    url = ""
    if is_production:
        url = f"{global_config['base_url']}/api/v1/auth/forgot-pass/{secret_token}"
    else:
        url = f"localhost:3000/api/v1/auth/forgot-pass/{secret_token}"

    return url
