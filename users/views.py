from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
# import jwt
import time
# import requests

JWT_ISSUER = 'me'
JWT_SECRET = 'secret'
JWT_DURATION_SECONDS = 600


@api_view(['POST'])
def registration_initialize(request):
    username = request.data['username']
    email = request.data['email']
    response_data = {
        'usernameClaimed': False,
        'emailClaimed': False,
        'profileUuid': None,
        'claimToken': None
    }

    exists = False
    if User.objects.filter(username=username).exists():
        exists = True
        response_data['usernameClaimed'] = True
    if User.objects.filter(email=email).exists():
        exists = True
        response_data['emailClaimed'] = True
    if exists:
        return Response(response_data)

    pass

    # todo: untested:
    profile_uuid = get_profile_uuid_by_email_or_none(email)
    if profile_uuid:
        claim_token = create_claim_token(profile_uuid=profile_uuid, email=email, username=username)
        send_email(email, claim_token)
        Response(response_data)

    create_claim_token(email=email, username=username)
    return Response(response_data)


def create_claim_token(**payload):
    payload['iss'] = JWT_ISSUER
    payload['iat'] = int(time.time())
    payload['exp'] = int(time.time()) + JWT_DURATION_SECONDS

    return jwt.encode(payload, JWT_SECRET)


def get_profile_uuid_by_email_or_none(email):
    return 1


def send_email(email, claim_token):
    pass