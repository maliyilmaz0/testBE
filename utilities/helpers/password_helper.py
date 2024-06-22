import bcrypt


class PasswordHelper:

    @staticmethod
    def encrypt_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def compare_passwords(salt_password: str, encrypted_password: bytes) -> bool:
        return bcrypt.checkpw(salt_password.encode('utf-8'), encrypted_password)
