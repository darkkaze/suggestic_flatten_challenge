from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_main_error():
    response = client.get("/flatten")
    assert response.status_code == 405


def test_post_string_to_main_error():
    response = client.post("/flatten", json={"items": "string"})
    assert response.status_code == 422


def test_post_a_list_with_string_to_main_error():
    response = client.post("/flatten", json={"items": ["string"]})
    assert response.status_code == 422


def test_post_a_list_with_anidate_string_to_main_error():
    response = client.post("/flatten", json={"items": [1, 2, ["string"]]})
    assert response.status_code == 422


def test_post_flat_list_to_main_ok():
    response = client.post("/flatten", json={"items": [1, 2, 3, 4, 5]})
    assert response.status_code == 200
    assert response.json()["results"] == [1, 2, 3, 4, 5]


def test_post_1_anidate_level_list_to_main_ok():
    response = client.post("/flatten", json={"items": [1, [2, 3], [4, 5]]})
    assert response.status_code == 200
    assert response.json()["results"] == [1, 2, 3, 4, 5]


def test_post_2_anidate_level_list_to_main_ok():
    response = client.post("/flatten", json={"items": [1, [2, [3, 4], 5]]})
    assert response.status_code == 200
    assert response.json()["results"] == [1, 2, 3, 4, 5]
