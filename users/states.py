from users.models import User
import jwt
import time

JWT_ISSUER = 'me'
JWT_SECRET = 'secret'
JWT_DURATION_SECONDS = 600


class RegistrationState:
    def __init__(self, email_claimed, username_claimed, claim_token, profile_uuid):
        self.email_claimed = email_claimed
        self.username_claimed = username_claimed
        self.claim_token = claim_token
        self.profile_uuid = profile_uuid




class RegistrationStateFactory:

    @staticmethod
    def get_state(email, username):
        email_claimed = User.objects.filter(email=email).exists()
        username_claimed = User.objects.filter(username=username).exists()

        if email_claimed or username_claimed:
            return RegistrationState(email_claimed, username_claimed, False, False)

        profile_uuid = get_profile_uuid_by_email_or_none(email)
        if profile_uuid:
            claim_token = create_claim_token(profile_uuid=profile_uuid, email=email, username=username)
            return RegistrationState(False, False, claim_token, profile_uuid)

        claim_token = create_claim_token(email=email, username=username)
        return RegistrationState(False, False, claim_token, None)


def create_claim_token(**payload):
    payload['iss'] = JWT_ISSUER
    payload['iat'] = int(time.time())
    payload['exp'] = int(time.time()) + JWT_DURATION_SECONDS

    return jwt.encode(payload, JWT_SECRET)


def get_profile_uuid_by_email_or_none(email):
    # todo: send a request to the profile service to get-or-none profile uuid given email address
    return 1


def send_email(email, claim_token):
    pass
