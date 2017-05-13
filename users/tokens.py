import jwt
import time


class Jwt:
    issuer = 'me'
    secret = 'secret'

    def __init__(self, decoded=None, encoded=None):
        if decoded and encoded:
            raise ValueError("Jwt wrapper init should be given decoded or encoded, but not both")

        if not(decoded or encoded):
            raise ValueError("Jwt wrapper init should be given either decoded or encoded")

        self.decoded = decoded
        self.encoded = encoded


    @staticmethod
    def create_token(duration_seconds=None, **payload):
        payload['iss'] = Jwt.issuer
        payload['iat'] = int(time.time())

        if duration_seconds:
            payload['exp'] = int(time.time()) + duration_seconds

        return jwt.encode(payload, Jwt.secret)

    def decode(self):
        if self._encoded_is_valid(self.encoded):
            decoded = jwt.decode(self.encoded)
            self.decoded = decoded
            return decoded
        else:
            raise Exception  # todo

    def _encoded_is_valid(self, encoded):
        return True



