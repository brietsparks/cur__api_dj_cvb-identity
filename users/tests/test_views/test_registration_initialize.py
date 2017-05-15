from users.tests.factories import UserFactory
from users.views.registration_initialize import registration_initialize
from users.services import Profiles, Emails
from users.tokens import Jwt
from django.test import RequestFactory
from rest_framework import status
import pytest
import jwt

pytestmark = pytest.mark.django_db
test_username = 'test_username'
test_email = 'test@test.test'

invalid_request_inputs = [
    {},
    {'username': '', 'email': ''},
    # {'username': None, 'email': None} # todo: get this working
]


class TestRegistrationInitialize:
    @pytest.mark.parametrize("req_input", invalid_request_inputs)
    def test_missing_username_and_email(self, mocker, req_input):
        mocker.patch.object(Emails, 'send_account_claim_token_email')
        Emails.send_account_claim_token_email.return_value = None

        post_req = RequestFactory().post('/', req_input)
        resp = registration_initialize(post_req)
        data = resp.data

        assert data['usernameInvalid'] is True, \
            'Response data usernameInvalid should be True when Request username is invalid'

        assert data['emailInvalid'] is True, \
            'Response data emailInvalid should be True when Request email is invalid'

        assert data['usernameClaimed'] is None and \
            data['emailClaimed'] is None and \
            data['claimToken'] is None, \
            'All other response data fields should be None when email or username input is invalid'

    def test_existing_username_and_email(self, mocker):
        mocker.patch.object(Emails, 'send_account_claim_token_email')
        Emails.send_account_claim_token_email.return_value = None

        UserFactory(username=test_username, email=test_email)

        post_req = RequestFactory().post('/', {
            'username': test_username,
            'email': test_email
        })

        resp = registration_initialize(post_req)
        data = resp.data

        assert resp.data['usernameInvalid'] is False, \
            'Response data usernameInvalid should be False when Request valid username is given'

        assert resp.data['emailInvalid'] is False, \
            'Response data emailInvalid should be False when Request valid email is given'

        assert data['usernameClaimed'] is True, \
            'Response data usernameClaimed should be True when a user is registered with that username'

        assert data['emailClaimed'] is True, \
            'Response data emailClaimed should be True when a user is registered with that email'

        assert data['profileExists'] is None, \
            'Response data profileExists should be None when a user is registered with that email'

        assert data['claimToken'] is None, \
            'Response data claimToken should be None when a user is registered with that email or username'

    def test_unclaimed_but_existing_profile(self, mocker):
        mocker.patch.object(Emails, 'send_account_claim_token_email')
        Emails.send_account_claim_token_email.return_value = None

        mocker.patch.object(Profiles, 'get_profile_uuid_by_email_or_none')
        Profiles.get_profile_uuid_by_email_or_none.return_value = 1

        mocker.patch.object(Jwt, 'create_token')
        Jwt.create_token.return_value = 'mocked.jwt.string'

        mocker.patch.object(Jwt, 'create_token')
        Jwt.create_token.return_value = 'mocked.jwt.string'

        post_req = RequestFactory().post('/', {
            'username': test_username,
            'email': test_email
        })

        resp = registration_initialize(post_req)
        data = resp.data

        assert resp.data['usernameInvalid'] is False, \
            'Response data usernameInvalid should be False when Request valid username is given'

        assert resp.data['emailInvalid'] is False, \
            'Response data emailInvalid should be False when Request valid email is given'

        assert data['usernameClaimed'] is False, \
            'Response data usernameClaimed should be False when a username is unclaimed'

        assert data['emailClaimed'] is False, \
            'Response data emailClaimed should be True when an email is unclaimed'

        assert data['profileExists'] is True, \
            'Response data profileExists should be True when a profile is unclaimed'

        assert data['claimToken'] is 'mocked.jwt.string', \
            'Response data claimToken should be a jwt string when a profile is unclaimed'

    def test_non_existent_profile(self, mocker):
        mocker.patch.object(Emails, 'send_account_claim_token_email')
        Emails.send_account_claim_token_email.return_value = None

        mocker.patch.object(Profiles, 'get_profile_uuid_by_email_or_none')
        Profiles.get_profile_uuid_by_email_or_none.return_value = None

        mocker.patch.object(Jwt, 'create_token')
        Jwt.create_token.return_value = 'mocked.jwt.string'

        post_req = RequestFactory().post('/', {
            'username': test_username,
            'email': test_email
        })

        resp = registration_initialize(post_req)
        data = resp.data

        assert resp.data['usernameInvalid'] is False, \
            'Response data usernameInvalid should be False when Request valid username is given'

        assert resp.data['emailInvalid'] is False, \
            'Response data emailInvalid should be False when Request valid email is given'

        assert data['usernameClaimed'] is False, \
            'Response data usernameClaimed should be False when a username is non-existent'

        assert data['emailClaimed'] is False, \
            'Response data emailClaimed should be True when an email is non-existent'

        assert data['claimToken'] is 'mocked.jwt.string', \
            'Response data claimToken should be a jwt string when a profile is non-existent'




        # @responses.activate
        # def test_unclaimed_but_existing_profile(self):
        #     post_req = RequestFactory().post('/', {
        #         'username': test_username,
        #         'email': test_email
        #     })
        #
        #     responses.add(responses.GET, views.PROFILES_API,
        #                   body='{"person_uuid": "some_email@test.com"}',
        #                   status=200,
        #                   content_type='application/json'
        #                   )
        #     resp = registration_initialize(post_req)

# @responses.activate
# def test_dummy():
#     responses.add(responses.GET, 'http://localhost:3000/foo', body='{"foo": 1}', status=200, content_type='application/json')
#     resp = requests.get('http://localhost:3000/foo')
#
#     assert resp.json() == {'foo': 1}
