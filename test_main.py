from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_width_query():
    response = client.post("/v1/query", json={
        "text": "What is the width of a Yamaha P-150?"
    })

    assert response.status_code == 200
    data = response.json()

    assert "Yamaha P-150" in data["query"]
    assert "sparql" in data
    assert "results" in data
    assert data["results"] is not None


def test_height_query():
    response = client.post("/v1/query", json={
        "text": "What is the height of a Yamaha P-150?"
    })

    assert response.status_code == 200
    data = response.json()

    assert "sparql" in data
    assert "results" in data


def test_danish_query():
    response = client.post("/v1/query", json={
        "text": "Hvad er bredden på Yamaha P-150?"
    })

    assert response.status_code == 200
    data = response.json()

    assert "sparql" in data
    assert "results" in data


def test_empty_text_rejected():
    response = client.post("/v1/query", json={"text": ""})
    assert response.status_code == 400


if __name__ == "__main__":
    test_width_query()
    test_height_query()
    test_danish_query()
    test_empty_text_rejected()
    print("All tests passed!")
