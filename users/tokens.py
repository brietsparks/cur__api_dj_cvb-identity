import jwt
import time


"""
Wraps jwt
"""
class Jwt:
    issuer = 'me'
    secret = 'secret'

    @staticmethod
    def create_token(duration_seconds=None, **payload):
        payload['iss'] = Jwt.issuer
        payload['iat'] = int(time.time())

        if duration_seconds:
            payload['exp'] = int(time.time()) + duration_seconds

        return jwt.encode(payload, Jwt.secret)

    @staticmethod
    def decode_token(token):
        return jwt.decode(token, key=Jwt.secret)



