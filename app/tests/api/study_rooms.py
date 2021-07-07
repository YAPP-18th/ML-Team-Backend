from app.core           import settings
from app.tests.conftest import client


api_address = settings.API_V1_STR


def test_get_study_room_success():
    room_id  = 'be6172b4-c388-4b5d-832a-b30110e11bd5'
    response = client.get(
        f'{api_address}/study-rooms/{room_id}'
    )
    assert response.status_code == 200


def test_get_study_room_uuid():
    room_id  = '7aa4556e-bdc2-4fe9-813a-1a4'
    response = client.get(
        f'{api_address}/study-rooms/{room_id}'
    )
    assert response.status_code == 500


def test_get_study_room_not_found():
    room_id  = '7aa4556e-bdc2-4fe9'
    response = client.get(
        f'{api_address}/study_rooms/{room_id}'
    )
    print(response.json())
    assert response.status_code == 404


def test_get_study_rooms():
    response = client.get(
        f'{api_address}/study-rooms'
    )
    print(response.json())
    assert response.status_code == 200


def test_create_study_room():
    data = {
        "title": "스터디 룸 생성 테스트",
        "description": "스터디룸 생성 설명",
        "is_public": True,
        "owner_id": 1
    }
    response = client.post(
        f'{api_address}/study-rooms',
        json = { **data }
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == None