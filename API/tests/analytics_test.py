import pytest

from ninja.testing import TestClient
from API.api_views import comments_router

@pytest.fixture
def api_client():
    return TestClient(comments_router)


@pytest.mark.django_db
def test_comments_daily_breakdown_invalid_date(api_client):
    date_from = 'invalid-date'
    date_to = 'invalid-date'
    url = f'daily-breakdown?date_from={date_from}&date_to={date_to}'

    response = api_client.get(url, {'date_from': date_from, 'date_to': date_to})
    response_data = response.json()
    print(response_data)
    assert response_data['detail'][0]['msg'] == 'Input should be a valid datetime or date, invalid character in year'
