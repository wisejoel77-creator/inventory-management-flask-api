def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200