import pytest

from django.contrib.auth import get_user_model, login, authenticate
from ninja.testing import TestClient
from API.api_views import posts_router


User = get_user_model()


@pytest.fixture
def user():
    user = User.objects.create_user(username='test1', password='password1')
    authenticate(user)
    return user


@pytest.fixture
def api_client():
    return TestClient(posts_router)


@pytest.mark.django_db
def test_create_post_invalid_data(api_client, user):
    token = user.token
    url = '/create-post/'
    data = {
        'title': '',
        'content': 'Test Content',
    }
    response = api_client.post(url, data, content_type='application/json', headers={'Authorization': 'Bearer ' + token})

    response_data = response.json()
    assert response_data['message'] == 'Invalid data'
