"""
Integration tests for the booking API endpoints.
"""

import json

import pytest


def test_create_booking(client, db):
    """
    Test creating a booking through the API.
    """
    data = {
        "customer_name": "John",
        "last_name": "Doe",
        "flight_number": "AB123",
        "departure_date": "2024-07-10",
    }
    response = client.post(
        "/bookings/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    response_data = response.get_json()
    assert "pnr" in response_data
    assert response_data["customer_name"] == "John"


def test_get_booking(client, db):
    """
    Test fetching a booking through the API.
    """
    data = {
        "customer_name": "John",
        "last_name": "Doe",
        "flight_number": "AB123",
        "departure_date": "2024-07-10",
    }
    create_response = client.post(
        "/bookings/", data=json.dumps(data), content_type="application/json"
    )
    pnr = create_response.get_json()["pnr"]
    response = client.get(f"/bookings/{pnr}/Doe")
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["customer_name"] == "John"


def test_update_booking(client, db):
    """
    Test updating a booking through the API.
    """
    data = {
        "customer_name": "John",
        "last_name": "Doe",
        "flight_number": "AB123",
        "departure_date": "2024-07-10",
    }
    create_response = client.post(
        "/bookings/", data=json.dumps(data), content_type="application/json"
    )
    pnr = create_response.get_json()["pnr"]

    update_data = {"customer_name": "Jane"}
    response = client.patch(
        f"/bookings/{pnr}/Doe",
        data=json.dumps(update_data),
        content_type="application/json",
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["customer_name"] == "Jane"


def test_delete_booking(client, db):
    """
    Test deleting a booking through the API.
    """
    data = {
        "customer_name": "John",
        "last_name": "Doe",
        "flight_number": "AB123",
        "departure_date": "2024-07-10",
    }
    create_response = client.post(
        "/bookings/", data=json.dumps(data), content_type="application/json"
    )
    pnr = create_response.get_json()["pnr"]
    response = client.delete(f"/bookings/{pnr}/Doe")
    assert response.status_code == 204


def test_add_vas(client, db):
    """
    Test adding value-added services to a booking through the API.
    """
    data = {
        "customer_name": "Alice",
        "last_name": "Smith",
        "flight_number": "CD456",
        "departure_date": "2024-07-15",
    }
    create_response = client.post(
        "/bookings/", data=json.dumps(data), content_type="application/json"
    )
    assert create_response.status_code == 201
    pnr = create_response.get_json()["pnr"]

    vas_data = {"vas": ["Extra legroom", "Meal"]}
    response = client.post(
        f"/bookings/{pnr}/Smith/vas",
        data=json.dumps(vas_data),
        content_type="application/json",
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert "Extra legroom" in response_data["vas"]
    assert "Meal" in response_data["vas"]
