import pytest
from fastapi.testclient import TestClient

from payment.db import get_session_override, get_session
from payment.main import app

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Payment App running :-}"}


def test_notification_page(test_client):
    response = test_client.get("/payment/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Payment Page running :-}"}


# Test for creating a payment


def test_create_payment(test_client):
    payment_data = {
        "created_at": "2024-07-31T12:19:50.577337",
        "card_num": 123456,
        "cvv": 123,
        "valid_thru_month": 1,
        "valid_thru_year": 2024,
        "total_price": 100.0,
        "status": "pending"
    }
    response = test_client.post("/payment/pay-now/", json=payment_data)
    assert response.status_code == 200
    assert response.json()["total_price"] == 100.0


# Test for listing all payments


def test_read_payments(test_client):
    # First, add a test payment
    test_client.post("/payment/pay-now/", json={
        "created_at": "2024-07-31T12:19:50.577337",
        "card_num": 123456,
        "cvv": 123,
        "valid_thru_month": 1,
        "valid_thru_year": 2024,
        "total_price": 100.0,
        "status": "pending"
    })

    response = test_client.get("/payment/all/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Test for getting a specific payment by ID


def test_read_payment(test_client):
    # First, add a test payment
    create_response = test_client.post("/payment/pay-now/", json={
        "created_at": "2024-07-31T12:19:50.577337",
        "card_num": 123456,
        "cvv": 123,
        "valid_thru_month": 1,
        "valid_thru_year": 2024,
        "total_price": 100.0,
        "status": "pending"
    })
    payment_id = create_response.json()["payment_id"]

    response = test_client.get(f"/payment/{payment_id}")
    assert response.status_code == 200
    # assert response.json()["total_price"] == 100.0
    assert response.json()["payment_id"] == payment_id


# Test for getting a payment that does not exist


def test_read_payment_not_found(test_client):
    response = test_client.get("/payment/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found"}
