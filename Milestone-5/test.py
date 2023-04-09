import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_ticket_api(client):
    ticket_data = {"title": "Test Ticket", "description": "This is a test ticket"}
    response = client.post('/tickets', json=ticket_data)
    assert response.status_code == 201

    response = client.get('/tickets')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Ticket"
    assert response.json()[0]["description"] == "This is a test ticket"

    ticket_id = response.json()[0]["ticket_id"]
    response = client.get(f'/tickets/{ticket_id}')
    assert response.status_code == 200
    assert response.json()["title"] == "Test Ticket"
    assert response.json()["description"] == "This is a test ticket"

    updated_ticket_data = {"title": "Updated Test Ticket", "description": "This is an updated test ticket"}
    response = client.put(f'/tickets/{ticket_id}', json=updated_ticket_data)
    assert response.status_code == 200

    response = client.get(f'/tickets/{ticket_id}')
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Ticket"
    assert response.json()["description"] == "This is an updated test ticket"

    response = client.delete(f'/tickets/{ticket_id}')
    assert response.status_code == 204

def test_vote_api(client):
    ticket_data = {"title": "Test Ticket", "description": "This is a test ticket"}
    response = client.post('/tickets', json=ticket_data)
    assert response.status_code == 201

    ticket_id = response.json()["ticket_id"]
    response = client.put('/votes', json={"ticket_id": ticket_id})
    assert response.status_code == 200

    response = client.get('/votes')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["ticket_id"] == ticket_id
    assert response.json()[0]["upvotes"] == 1

def test_faq_api(client):
    faq_data = {"question": "Test Question", "answer": "This is a test answer"}
    response = client.post('/faqs', json=faq_data)
    assert response.status_code == 201

    response = client.get('/faqs')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["question"] == "Test Question"
    assert response.json()[0]["answer"] == "This is a test answer"

    faq_id = response.json()[0]["f_id"]
    response = client.get(f'/faqs/{faq_id}')
    assert response.status_code == 200
    assert response.json()["question"] == "Test Question"
    assert response.json()["answer"] == "This is a test answer"

    updated_faq_data = {"question": "Updated Test Question", "answer": "This is an updated test answer"}
    response = client.put(f'/faqs/{faq_id}', json=updated_faq_data)
    assert response.status_code == 200

    response = client.get(f'/faqs/{faq_id}')
    assert response.status_code == 200
    assert response.json()["question"] == "Updated Test Question"
    assert response.json()["answer"] == "This is an updated test answer"
