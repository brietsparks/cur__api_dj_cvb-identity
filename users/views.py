from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
from .states import AccountStateFactory

import jwt
import time

JWT_ISSUER = 'me'
JWT_SECRET = 'secret'
JWT_DURATION_SECONDS = 600


@api_view(['POST'])
def registration_initialize(request):
    email = request.data['email']
    username = request.data['username']

    state = AccountStateFactory.get_state(email, username)
    
    if state.is_taken():
        return Response(state.__dict__)
    
    if state.exists_but_unclaimed():
        claim_token = create_claim_token(
            profile_uuid=state.profile_uuid,
            email=state.email,
            username=state.username
        )
        send_email(email, claim_token)
        return Response(state.__dict__)

    if state.does_not_exist():
        claim_token = create_claim_token(
            email=state.email,
            username=state.username
        )
        return Response(state.__dict__)


def create_claim_token(**claims):
    claims['iss'] = JWT_ISSUER
    claims['iat'] = int(time.time())
    claims['exp'] = int(time.time()) + JWT_DURATION_SECONDS

    return jwt.encode(claims, JWT_SECRET)


def send_email(email, claim_token):
    pass