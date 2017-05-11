import jwt
import time


class JWT:
    issuer = 'me'
    secret = 'secret'

    def __call__(self, duration_seconds=None, **payload):
        JWT.create_token(duration_seconds=duration_seconds, **payload)

    @staticmethod
    def create_token(duration_seconds=None, **payload):
        payload['iss'] = JWT.issuer
        payload['iat'] = int(time.time())

        if duration_seconds:
            payload['exp'] = int(time.time()) + duration_seconds

        return jwt.encode(payload, JWT.secret)
