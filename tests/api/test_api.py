import uuid

from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)


def test_user():
    user_uuid = str(uuid.uuid4())

    response = client.post(
        '/coupon',
        json={
            'user_uuid': user_uuid,
            'parameters': {'user_verification': {'for_user_uuid': user_uuid}},
        },
    )
    assert response.status_code == 200
    coupon_uuid = response.json()['uuid']

    response = client.post(
        '/get_coupon',
        params={
            'coupon_uuid': coupon_uuid,
        },
        json={
            'user_verification': {'user_uuid': user_uuid},
        },
    )
    assert response.status_code == 200
    assert response.json()['exists']


def test_discount():
    user_uuid = str(uuid.uuid4())

    response = client.post(
        '/coupon',
        json={
            'user_uuid': user_uuid,
            'parameters': {'discount': {'discount_percentage': 50}},
        },
    )
    assert response.status_code == 200
    coupon_uuid = response.json()['uuid']

    response = client.post(
        '/get_coupon',
        params={
            'coupon_uuid': coupon_uuid,
        },
        json={},
    )
    assert response.status_code == 200
    assert response.json()['coupon']['parameters']['discount'] == {
        'discount_amount': None,
        'discount_percentage': 50.0,
    }


def test_taken():
    response = client.post('/coupon', json={})
    assert response.status_code == 200
    coupon_uuid = response.json()['uuid']

    params = {'coupon_uuid': coupon_uuid}
    response = client.put('/coupon/taken', params=params)
    assert response.status_code == 200

    response = client.put('/coupon/taken', params=params)
    assert response.status_code == 404
