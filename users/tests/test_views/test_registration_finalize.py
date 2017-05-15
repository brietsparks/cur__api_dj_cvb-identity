from django.test import RequestFactory
from users.tests.factories import UserFactory
from users.services import Profiles
import jwt
from users.tokens import Jwt
import pytest

from users.views.registration_finalize import registration_finalize

pytestmark = pytest.mark.django_db
test_email = 'test@test.test'
test_username = 'testUsername'
test_password = 'password'
test_profile_uuid = 'test_profile_uuid'


def create_claim_token(existing_profile = False):
    data = {
        'email': test_email,
        'username': test_username,
    }
    if existing_profile:
        data['profileUuid'] = test_profile_uuid

    return jwt.encode(data, key=Jwt.secret)


class TestRegistrationFinalize:
    def test_invalid_claim_token_and_password(self):
        invalid_claim_token = jwt.encode({}, 'wrong_secret')
        post_req = RequestFactory().post('/', {
            'claimToken': invalid_claim_token,
            'password': ''
        })
        resp = registration_finalize(post_req)
        data = resp.data

        assert resp.status_code == 400

        assert data['claimTokenInvalid'] is True, \
            'Response data claimTokenInvalid should be True when Request claimToken is invalid'

        assert data['passwordInvalid'] is True and \
            data['emailClaimed'] is None and \
            data['usernameClaimed'] is None and \
            data['authToken'] is None, \
            'All other response data fields should be None when Request claimToken is invalid'

    def test_existing_username_and_email(self):
        UserFactory(username=test_username, email=test_email)
        claim_token = create_claim_token().decode()

        post_req = RequestFactory().post('/', {
            'claimToken': claim_token,
            'password': test_password
        })

        resp = registration_finalize(post_req)
        data = resp.data

        assert resp.status_code == 400

        assert data['claimTokenInvalid'] is False, \
            'Response data claimTokenInvalid should be False when Request existing username or email'

        assert data['emailClaimed'] is True, \
            'Response data emailClaimed should be True when Request existing username or email'

        assert data['usernameClaimed'] is True, \
            'Response data usernameClaimed should be True when Request existing username or email'

    # def test_unclaimed_but_existing_profile(self, mocker):
    #     mocker.patch.object(Profiles, 'create_new_profile')
    #     Profiles.create_new_profile.return_value = 1


