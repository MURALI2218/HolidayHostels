
from fastapi.testclient import TestClient
from HolidayHostels.main import app

client =TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World !!!!"}

# def test_create_user():
#     res = client.post("/createuser/", json={"username" : "hello", "emailid": "hello@gamil.com", "password":"123"})
#     assert res.json().get("emailid") == "hello@gamil.com"
#     assert res.status_code == 201