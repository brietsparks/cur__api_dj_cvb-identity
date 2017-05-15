from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from jwt import DecodeError, ExpiredSignatureError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.models import User
from ..services import Profiles, Emails
from ..tokens import Jwt
from ..models import User
import jwt


@api_view(['POST'])
def registration_finalize(request):
    # initial response data, which gets changed throughout the procedure
    response_data = {
        'claimTokenInvalid': not _request_has_valid_claim_token(request),
        'passwordInvalid': not _request_has_valid_password(request),
        'emailClaimed': None,
        'usernameClaimed': None,
        'authToken': None
    }

    # if the claim token or password is invalid then return 400
    if response_data['claimTokenInvalid'] or response_data['passwordInvalid']:
        return Response(response_data, status.HTTP_400_BAD_REQUEST)

    # get the password from request body
    password = request.data['password']

    # get the email and username from the claim token
    claim_token_data = Jwt.decode_token(request.data['claimToken'])
    email = claim_token_data['email']
    username = claim_token_data['username']

    # check if the user exists, which is unlikely at this point
    response_data['emailClaimed'] = User.objects.filter(email=email).exists()
    response_data['usernameClaimed'] = User.objects.filter(username=username).exists()

    # if either the email or username is taken, return a 400
    if response_data['emailClaimed'] or response_data['usernameClaimed']:
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # get the profile_uuid
    if 'profileUuid' in claim_token_data:
        profile_uuid = request.data['profile_uuid']
    else:
        profile_uuid = Profiles.create_new_profile(claim_token_data['email'])

    # create the user
    user = User.objects.create(email=email, username=username, password=password, profile_uuid=profile_uuid)


def _request_has_valid_claim_token(request):
    try:
        Jwt.decode_token(request.data['claimToken'])
        return True
    except (DecodeError, ExpiredSignatureError):
        return False


def _request_has_valid_password(request):
    data = request.data
    return 'password' in data and \
           data['password'] is not None and \
           len(request.data['password']) > 2

