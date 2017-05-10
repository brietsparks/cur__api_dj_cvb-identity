from django.test import TestCase

from django.test import RequestFactory
from .. import views
from django.contrib.auth.models import AnonymousUser
from .factories import UserFactory
import pytest
pytestmark = pytest.mark.django_db

test_username = 'test_username'
test_email = 'test@test.test'


class TestRegistrationInitialize:
    def test_existing_username_and_email(self):
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

    def test_unclaimed_email_and_existing_profile(self):
        pass


import requests
import responses
@responses.activate
def test_dummy():
    responses.add(responses.GET, 'http://localhost:3000/foo', body='{"foo": 1}', status=200, content_type='application/json')
    resp = requests.get('http://localhost:3000/foo')

    assert resp.json() == {'foo': 1}

