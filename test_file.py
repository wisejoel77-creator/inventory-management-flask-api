#test to check if the inventory route is working
import pytest
from app import app

#Creates a test client for the Flask app.
#This allows us to simulate API requests without running the server.
@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

#test to get inventory items
def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.json, list)  # Check if the response is a list

#test to get a single item from the inventory
def test_get_single_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.json["id"] == 1  # Check if the returned item has the correct ID