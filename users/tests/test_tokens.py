import pytest
from users.tokens import Jwt
import jwt
import time


class TestJwt:
    def test_create_token_returns_a_jwt_signed_with_secret(self):
        token = Jwt.create_token()
        jwt.decode(token, Jwt.secret) # if fails, expection will throw

    def test_create_token_returns_a_jwt_with_given_kwargs_as_payload(self):
        token = Jwt.create_token(payload_a=1234, payload_b=5678)
        decoded = jwt.decode(token, verify=False)
        assert decoded['payload_a'] == 1234
        assert decoded['payload_b'] == 5678

    def test_create_token_returns_a_jwt_with_iss_and_iat(self):
        now = int(time.time())
        token = Jwt.create_token()
        decoded = jwt.decode(token, verify=False)
        assert decoded['iss'] == Jwt.issuer
        assert decoded['iat'] == now

    def test_create_token_without_duration_returns_a_jwt_without_exp(self):
        token = Jwt.create_token()
        decoded = jwt.decode(token, verify=False)
        assert 'exp' not in decoded

    def test_create_token_with_duration_returns_a_jwt_with_exp(self):
        later = int(time.time()) + 100
        token = Jwt.create_token(duration_seconds=100)
        decoded = jwt.decode(token, verify=False)
        assert decoded['exp'] == later



