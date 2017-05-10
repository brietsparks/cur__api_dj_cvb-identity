from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
from .states import RegistrationStateFactory


@api_view(['POST'])
def registration_initialize(request):
    email = request.data['email']
    username = request.data['username']

    registration_state = RegistrationStateFactory.get_state(email, username)



    pass



