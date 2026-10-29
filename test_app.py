from app import app


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_database_health():
    client = app.test_client()
    response = client.get("/health")
    # Ce test ne passera au vert QUE si une vraie base PostgreSQL est allumée !
    assert response.status_code == 200
    assert response.get_json()["database"] == "connected"