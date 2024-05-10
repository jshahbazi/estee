from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from .database import Database, FoodTruck
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

app = FastAPI()
db = Database("food_trucks.db")

CSV_FILE = "./data/Mobile_Food_Facility_Permit.csv"
DB_FILE = "food_trucks.db"

if not os.path.exists(DB_FILE):
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"File {CSV_FILE} not found. Please download the file from https://data.sfgov.org/api/views/rqzj-sfat/rows.csv and place it in the data directory."
        )
    db.create_database(CSV_FILE)

geolocator = Nominatim(user_agent="address_finder")


async def get_coordinates(address, geolocator):
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None


async def calculate_distances(target_coord, all_truck_data):
    return [
        geodesic(
            target_coord, (truck_data["latitude"], truck_data["longitude"])
        ).kilometers
        for truck_data in all_truck_data
    ]


async def find_closest_applicants(all_truck_data, target_coord, num_closest=3):
    # Calculate distances between target address and all other addresses
    target_distances = await calculate_distances(target_coord, all_truck_data)

    # Create pairs of (distance, index)
    distance_indices = list(enumerate(target_distances))

    # Sort the distance-index pairs based on distances
    distance_indices.sort(key=lambda x: x[1])

    # Get the indices of the top num_closest applicants
    closest_indices = [idx for idx, _ in distance_indices[:num_closest]]

    return [all_truck_data[idx] for idx in closest_indices]


@app.get("/food_trucks/")
async def get_food_trucks():
    results = db.get_all_food_trucks()
    # Extracting applicant and food_items from each food truck
    data = [
        {
            "applicant": truck.applicant,
            "food_items": truck.food_items,
            "address": truck.address,
        }
        for truck in results
    ]

    return data


@app.get("/food_trucks/{location_id}")
async def get_food_truck(location_id: int):
    food_truck = db.get_food_truck_by_id(location_id)
    if food_truck is None:
        raise HTTPException(status_code=404, detail="Food truck not found")
    return food_truck


@app.get("/food_trucks/by_name/")
async def get_food_truck_by_name(
    name: str = Query(..., description="Name of the food truck")
):
    results = db.get_food_truck_by_name(name)
    if not results:
        raise HTTPException(status_code=404, detail="Food truck not found")
    return results


@app.post("/food_trucks/")
async def create_food_truck(food_truck: FoodTruck):
    db.insert_food_truck(food_truck)
    return food_truck


@app.put("/food_trucks/{location_id}")
async def update_food_truck(location_id: int, food_truck: FoodTruck):
    updated_truck = db.update_food_truck(location_id, food_truck)
    if updated_truck is None:
        raise HTTPException(status_code=404, detail="Food truck not found")
    return updated_truck


@app.delete("/food_trucks/{location_id}")
async def delete_food_truck(location_id: int):
    deleted_truck = db.delete_food_truck(location_id)
    if deleted_truck is None:
        raise HTTPException(status_code=404, detail="Food truck not found")
    return status.HTTP_200_OK


@app.get("/food_trucks/{location_id}/applicant_fooditems")
async def get_truck_food(location_id: int):
    food_truck = db.get_food_truck_by_id(location_id)
    if food_truck is None:
        raise HTTPException(status_code=404, detail="Food truck not found")

    data = {
        "applicant": food_truck.applicant,
        "food_items": food_truck.food_items,
        "address": food_truck.address,
    }

    return JSONResponse(content=data)


@app.get("/food_trucks/closest/")
async def find_closest_food_trucks(
    address: str = Query(..., description="User's address"),
):
    results = db.get_all_food_trucks()
    if not results:
        raise HTTPException(status_code=404, detail="Food trucks not found")

    # Extracting name, food_items, and coordinates from each food truck
    data = [
        {
            "applicant": truck.applicant,
            "food_items": truck.food_items,
            "address": truck.address,
            "latitude": truck.latitude,
            "longitude": truck.longitude,
        }
        for truck in results
    ]

    user_coordinates = await get_coordinates(address, geolocator)
    closest_trucks = await find_closest_applicants(data, user_coordinates)

    return closest_trucks
