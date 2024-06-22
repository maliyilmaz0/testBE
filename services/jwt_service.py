from config.jwt_config import ExpireType
from config.global_config import global_config
from fastapi.encoders import jsonable_encoder
import jwt
import datetime


class JwtService:
    
    @staticmethod
    def create_token(data, expire_count: int, expire_type: ExpireType):
        
        expire_date = datetime.datetime.now()    
        match (expire_type):
            case ExpireType.MINUTE:
                expire_date += datetime.timedelta(minutes=expire_count)
                pass
            case ExpireType.HOUR:
                expire_date += datetime.timedelta(hours=expire_count)
                pass
            case ExpireType.DAY:
                expire_date += datetime.timedelta(days=expire_count)
                pass
        data['exp'] = jsonable_encoder(expire_date)
        token = jwt.encode(payload=data, key=global_config['jwt_secret'], algorithm='HS256', headers={"expireIn": jsonable_encoder(expire_date)})
        return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, global_config['jwt_secret'], algorithms=['HS256'])
            
            return payload
        except jwt.ExpiredSignatureError as e:
            raise e

        except jwt.InvalidTokenError as e:
            raise e
    
            
    
    