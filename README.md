# Estee Food Truck API

Welcome to the Estee Food Truck API! This API is designed to provide users with information about food trucks in a given area, including their locations, available food items, and more. Not only can it list the food trucks, but it can also find the closest food truck to your address!  Never go hungry again!

## Features

- **Get All Food Trucks**: Retrieve a list of all available food trucks.
- **Get Food Truck by ID**: Fetch details of a specific food truck using its unique ID.
- **Search Food Trucks by Name**: Search for food trucks by their names.
- **Create, Update, and Delete Food Trucks**: Perform CRUD operations on food truck data.
- **Find Closest Food Trucks**: Locate the closest food trucks based on user's address.

## Setup

To set up the project locally, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/jshahbazi/estee.git
   ```

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies using Poetry:

    ```bash
    cd estee
    poetry install
    ````

3. **Run the Server**: Start the FastAPI server using the following command:

    ```bash
    poetry run uvicorn src.main:app --reload
    ```

4. **Access the API**: Once the server is running, you can access the API at http://localhost:8000 via API client tools like Postman or even just curl.

5. **Run tests**: If you'd like to see the tests run and verify it's operation, simply use the following command:

    ```bash
    poetry run pytest tests/test_main_module.py
    ```

## Endpoints

The following endpoints are available in the API:

- **GET /food_trucks/**: Get a list of all food trucks.
- **GET /food_trucks/{location_id}**: Get details of a specific food truck by its ID.
- **GET /food_trucks/by_name/**: Search for food trucks by name.
- **POST /food_trucks/**: Create a new food truck entry.
- **PUT /food_trucks/{location_id}**: Update an existing food truck entry.
- **DELETE /food_trucks/{location_id}**: Delete a food truck entry.
- **GET /food_trucks/{location_id}/applicant_fooditems**: Get details of a specific food truck along with its food items.
- **GET /food_trucks/closest/**: Find the closest food trucks based on user's address.


## Data Source

The data used in this project is sourced from the San Francisco government's Mobile Food Facility Permit dataset. You can find the dataset [here](https://data.sfgov.org/api/views/rqzj-sfat/rows.csv).

## Github Actions

This repo has two Github actions that will be run on every push:

- **Pylint**
- **Black**

The code itself has already been formatted using Black.

## Example Code

If you'd like to give it a try using Python, here is some sample code to retrieve the closest 3 food trucks using an address:

```python
import requests

url = "http://localhost:8000/food_trucks/closest/"

user_address = "90 BROADWAY, San Francisco, CA"
params = {"address": user_address}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("Closest Food Trucks:")
    for idx, truck in enumerate(response.json()):
        print(f"Truck {idx + 1}:")
        print(f"Applicant: {truck['applicant']}")
        print(f"Food Items: {truck['food_items']}")
        print(f"Address: {truck['address']}")
        print(f"Latitude: {truck['latitude']}")
        print(f"Longitude: {truck['longitude']}")
        print()
else:
    print(f"Failed to retrieve closest food trucks: {response.text}")
```
    