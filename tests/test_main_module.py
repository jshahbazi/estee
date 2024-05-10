import pytest
from fastapi.testclient import TestClient
from main import app, Database
from database import FoodTruck
from main import db, CSV_FILE, DB_FILE
import os
import random


# Test database file path
TEST_DB_FILE = "test_food_trucks.db"
CSV_FILE = "./Mobile_Food_Facility_Permit.csv"


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Create an instance of the Database class with the test database file
    test_db = Database(TEST_DB_FILE)

    # Initialize the test database with data from the CSV file
    test_db.create_database(CSV_FILE)

    yield test_db

    # Teardown: Remove the test database file
    os.remove(TEST_DB_FILE)


client = TestClient(app)

# Test data
location_id = random.randint(1, 1000)
applicant_name = "Test applicant"

sample_food_truck = {
    "location_id": location_id,
    "applicant": applicant_name,
    "facility_type": "Truck",
    "cnn": 1234567,
    "location_description": "Sample location",
    "address": "123 Sample St",
    "blocklot": "1234",
    "block": "123",
    "lot": "456",
    "permit": "123456",
    "status": "approved",
    "food_items": "Sample Food Items",
    "x": 37.12345,
    "y": -122.54321,
    "latitude": 37.12345,
    "longitude": -122.54321,
    "schedule": "Mon-Fri",
    "dayshours": "9AM-5PM",
    "NOISent": "Yes",
    "approved": "Yes",
    "received": "Yes",
    "prior_permit": "No",
    "expiration_date": "2025-01-01",
    "location": "Sample location",
    "fire_prevention_districts": 1,
    "police_districts": 2,
    "supervisor_districts": 3,
    "zip_codes": 12345,
    "neighborhoods_old": 6789,
}
test_food_truck = FoodTruck(**sample_food_truck)


# Test database initialization
def test_create_and_read_food_trucks_db(setup_test_db):
    results = setup_test_db.get_all_food_trucks()
    assert isinstance(results, list)


# Test POST /food_trucks/
def test_create_food_truck():
    response = client.post("/food_trucks/", json=test_food_truck.model_dump())
    assert response.status_code == 200
    assert response.json()["location_id"] == location_id


# Test GET /food_trucks/
def test_get_food_trucks():
    response = client.get("/food_trucks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0  # Checking if there's at least one food truck

    # Verifying if each item in the response contains 'applicant' and 'food_items' keys
    for item in data:
        assert "applicant" in item
        assert "food_items" in item
        assert "address" in item


# Test GET /food_trucks/{location_id}
def test_read_food_truck():
    response = client.get(f"/food_trucks/{location_id}")
    assert response.status_code == 200
    assert response.json()["location_id"] == location_id


# Test GET /food_trucks/by_name/
def test_read_food_truck_by_name():
    response = client.get("/food_trucks/by_name/", params={"name": applicant_name})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test PUT /food_trucks/{location_id}
def test_update_food_truck():
    updated_truck = test_food_truck.model_copy(
        update={"applicant": "Updated applicant"}
    )
    response = client.put(
        f"/food_trucks/{location_id}", json=updated_truck.model_dump()
    )
    assert response.status_code == 200
    assert response.json()["applicant"] == "Updated applicant"


# Test food truck not found
def test_read_food_truck_not_found():
    response = client.get("/food_trucks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Food truck not found"

# Test non-existent food truck name
def test_read_food_truck_by_name_not_found():
    response = client.get("/food_trucks/by_name/", params={"name": "Non-existent Name"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Food truck not found"

# Test update food truck not found
def test_update_food_truck_not_found():
    updated_truck = test_food_truck.model_copy(
        update={"applicant": "Updated applicant"}
    )
    response = client.put("/food_trucks/99999999", json=updated_truck.model_dump())
    assert response.status_code == 404
    assert response.json()["detail"] == "Food truck not found"

# Test DELETE /food_trucks/{location_id}
def test_delete_food_truck():
    response = client.delete(f"/food_trucks/{location_id}")
    assert response.status_code == 200

# Test food truck not found
def test_read_applicant_fooditems_not_found():
    response = client.get(f"/food_trucks/{location_id}/applicant_fooditems")
    assert response.status_code == 404
    assert response.json()["detail"] == "Food truck not found"

# Test GET /food_trucks/closest/
def test_find_closest_food_trucks():
    response = client.get("/food_trucks/closest/?address=90 BROADWAY, San Francisco, CA")
    assert response.status_code == 200
    assert response.json() == [
        {
            "applicant": "Senor Sisig",
            "food_items": "Various menu items & drinks",
            "address": "90 BROADWAY",
            "latitude": 37.799260113502285,
            "longitude": -122.39961794865545,
        },
        {
            "applicant": "Senor Sisig",
            "food_items": "Senor Sisig: Filipino fusion food: tacos: burritos: nachos: rice plates. Various beverages.Chairman Bao: Vegetable and meat sandwiches filled with Asian-flavored meats and vegetables.",
            "address": "90 BROADWAY",
            "latitude": 37.799260113502285,
            "longitude": -122.39961794865545,
        },
        {
            "applicant": "Roadside Rotisserie Corporation / Country Grill",
            "food_items": "Rotisserie Chicken: Ribs: Kickass Salad: Potatos w/fat dripping: chicken wrap.",
            "address": "90 BROADWAY",
            "latitude": 37.799260113502285,
            "longitude": -122.39961794865545,
        },
    ]
