from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_sheep():
    response = client.get("/sheep/1")

    assert response.status_code == 200

    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }


def test_add_sheep():
    # Prepare the new sheep data in a dictionary format.
    new_sheep_data = {
        "id": 7,
        "name": "Bella",
        "breed": "Babydoll",
        "sex": "ewe"
    }

    # Send a POST request to the endpoint "/sheep" with the new sheep data.
    response = client.post("/sheep", json=new_sheep_data)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response JSON matches the new sheep data
    assert response.json() == new_sheep_data

    # Verify that the sheep was actually added to the database by retrieving the new sheep by ID.
    get_response = client.get(f"/sheep/{new_sheep_data['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep_data


def test_delete_sheep():
    delete_response = client.delete("/sheep/1")

    # Assert that the response status code is 204 (No Content)
    assert delete_response.status_code == 204

    # Assert that the response content is empty, as expected for a 204 response
    assert delete_response.content == b''

    # Verify that the sheep was actually deleted by attempting to retrieve it
    get_response = client.get("/sheep/1")
    assert get_response.status_code == 404


def test_update_sheep():
    # First, add a sheep to update
    new_sheep_data = {
        "id": 10,
        "name": "Daisy",
        "breed": "Merino",
        "sex": "ewe"
    }
    client.post("/sheep", json=new_sheep_data)

    # Prepare the updated data
    updated_sheep_data = {
        "id": 10,
        "name": "Daisy",
        "breed": "Updated Merino",
        "sex": "ewe"
    }

    # Send a PUT request to update the sheep data
    response = client.put(f"/sheep/{updated_sheep_data['id']}", json=updated_sheep_data)
    assert response.status_code == 200
    assert response.json() == updated_sheep_data

    # Verify that the sheep data was updated
    get_response = client.get(f"/sheep/{updated_sheep_data['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == updated_sheep_data


def test_read_all_sheep():
    # Get all sheep data
    response = client.get("/sheep")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Check that each item in the list has necessary fields
    for sheep in response.json():
        assert "id" in sheep
        assert "name" in sheep
        assert "breed" in sheep
        assert "sex" in sheep
