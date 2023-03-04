def test_home(client):
    response = client.get("/")
    assert b"<title>Battleborn Mobile</title>" in response.data