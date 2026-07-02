#test to check if the inventory route is working
import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200