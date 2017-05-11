from .factories import UserFactory
from .. import views
from ..services import Profiles, Emails
from ..tokens import JWT
from django.test import RequestFactory
import pytest
import jwt

pytestmark = pytest.mark.django_db
test_username = 'test_username'
test_email = 'test@test.test'


class TestRegistrationInitialize:
    def test_existing_username_and_email(self, mocker):
        mocker.patch.object(Emails, 'send_account_claim_token_email')
        Emails.send_account_claim_token_email.return_value = None

        UserFactory(username=test_username, email=test_email)

        post_req = RequestFactory().post('/', {
            'username': test_username,
            'email': test_email
        })

        resp = views.registration_initialize(post_req)

        assert resp.data['usernameClaimed'], \
            'Response data usernameClaimed should be True when a user is registered with that username'

        assert resp.data['emailClaimed'], \
            'Response data emailClaimed should be True when a user is registered with that email'

        assert resp.data['profileUuid'] is None, \
            'Response data profile_uuid should be None when a user is registered with that email or username'

        assert resp.data['claimToken'] is None, \
            'Response data claimToken should be None when a user is registered with that email or username'

    def test_unclaimed_but_existing_profile(self, mocker):
        mocker.patch.object(Emails, 'send_account_claim_token_email')
        Emails.send_account_claim_token_email.return_value = None

        mocker.patch.object(Profiles, 'get_profile_uuid_by_email_or_none')
        Profiles.get_profile_uuid_by_email_or_none.return_value = 1

        mocker.patch.object(JWT, 'create_token')
        JWT.create_token.return_value = 'mocked.jwt.string'

        post_req = RequestFactory().post('/', {
            'username': test_username,
            'email': test_email
        })

        resp = views.registration_initialize(post_req)

        assert resp.data['usernameClaimed'] is False, \
            'Response data usernameClaimed should be False when a username is unclaimed'

        assert resp.data['emailClaimed'] is False, \
            'Response data emailClaimed should be True when an email is unclaimed'

        assert resp.data['profileUuid'] is None, \
            'Response data profile_uuid should be None when a profile is unclaimed (it is sent via email)'

        assert resp.data['claimToken'] is None, \
            'Response data claimToken should be None when a profile is unclaimed (it is sent via email)'

    def test_non_existent_profile(self, mocker):
        mocker.patch.object(Emails, 'send_account_claim_token_email')
        Emails.send_account_claim_token_email.return_value = None

        mocker.patch.object(Profiles, 'get_profile_uuid_by_email_or_none')
        Profiles.get_profile_uuid_by_email_or_none.return_value = None

        mocker.patch.object(JWT, 'create_token')
        JWT.create_token.return_value = 'mocked.jwt.string'

        post_req = RequestFactory().post('/', {
            'username': test_username,
            'email': test_email
        })

        resp = views.registration_initialize(post_req)

        assert resp.data['usernameClaimed'] is False, \
            'Response data usernameClaimed should be False when a username is non-existent'

        assert resp.data['emailClaimed'] is False, \
            'Response data emailClaimed should be True when an email is non-existent'

        assert resp.data['profileUuid'] is None, \
            'Response data profile_uuid should be None when a profile is non-existent'

        assert resp.data['claimToken'] is 'mocked.jwt.string', \
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
    #     resp = views.registration_initialize(post_req)


# @responses.activate
# def test_dummy():
#     responses.add(responses.GET, 'http://localhost:3000/foo', body='{"foo": 1}', status=200, content_type='application/json')
#     resp = requests.get('http://localhost:3000/foo')
#
#     assert resp.json() == {'foo': 1}

