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

#test to check behaviour when an item does not exist
def test_item_not_found(client):
    response = client.get("/inventory/91")  # Assuming 91 is not a valid ID

    assert response.status_code == 404
    assert response.json["message"] == "Item not found"

#test to add a new item
def test_add_item(client):
    new_item = {
        "name": "Eggs",
        "barcode": "9876543210987",
        "quantity": 30,
        "price": 4.00
    }
    response = client.post("/additem", json=new_item)

    assert response.status_code == 201
    assert response.json["message"] == "Item added to inventory!"

#test to update an existing item
def test_update_item(client):
    updated_data = {
        "name": "Almond Milk",
        "quantity": 25
    }
    response = client.patch("/edititem/1", json=updated_data)

    assert response.status_code == 201
    assert response.json["message"] == "Item updated in inventory!"

#test to remove an item from the inventory
def test_remove_item(client):
    response = client.delete("/removeitem/1")

    assert response.status_code == 200