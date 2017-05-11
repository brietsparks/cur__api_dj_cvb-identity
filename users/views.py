from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
from .services import Profiles, Emails
from .tokens import JWT

CLAIM_TOKEN_DURATION_SECONDS = 600


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

    # check if the user exists
    exists = False
    if User.objects.filter(username=username).exists():
        exists = True
        response_data['usernameClaimed'] = True
    if User.objects.filter(email=email).exists():
        exists = True
        response_data['emailClaimed'] = True
    if exists:
        return Response(response_data)

    # check if the profile exists
    profile_uuid = Profiles.get_profile_uuid_by_email_or_none(email)
    if profile_uuid:
        claim_token = JWT.create_token(duration_seconds=CLAIM_TOKEN_DURATION_SECONDS,
                                       profile_uuid=profile_uuid, email=email, username=username)
        # send the claim token in the email
        Emails.send_account_claim_token_email(email, claim_token)
        # return the response without the claim token
        return Response(response_data)

    claim_token = JWT.create_token(duration_seconds=CLAIM_TOKEN_DURATION_SECONDS,
                                   email=email, username=username)
    response_data['claimToken'] = claim_token
    return Response(response_data)
