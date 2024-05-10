# Estee Food Truck API

Welcome to the Estee Food Truck API! This API is designed to provide users with information about food trucks in a given area, including their locations, available food items, and more. Not only can it list the food trucks, but it can also find the closest food truck to your address!  Never go hungry again!

## Features

- **Get All Food Trucks**: Retrieve a list of all available food trucks.
- **Get Food Truck by ID**: Fetch details of a specific food truck using its unique ID.
- **Search Food Trucks by Name**: Search for food trucks by their names.
- **Create, Update, and Delete Food Trucks**: Perform CRUD operations on food truck data.
- **Find Closest Food Trucks**: Locate the closest food trucks based on the user's address.

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
    
## Design Thoughts

- I decided to go with an API because I really enjoy writing Python and I have been focused on API's for the past few months.  I wanted to create something a little more interesting than a basic CRUD API, so my original plan was to include an LLM.  Specifically, I had an idea of having the user specify what kind of food they wanted, then find the closest food trucks that were also rated highly.  So I figured that if I could pull reviews for a specific truck, I could use the LLM (or even just a vector database) to pick some trucks, and then pull in the reviews for those trucks and have the LLM decide which was rated highest.  I set up an account on Yelp and set up their API, but I started getting too deep in the weeds when the one endpoint I needed was only for Enterprise accounts.  And while hooking into OpenAI's API is easy, I'd either have my API key out in the open, or spend however long setting up secrets for it.  I also considered Ollama, but then I have to instruct the user to download Ollama separately, and then pick the correct model (I was going to use Llama 3, of course).  I realized it was a bit much for this assignment, but given another day I could have probably gotten it all set up.

- Just for the sake of having the data in a proper SQL database, I chose to ingest the CSV into a local sqlite database.  Obviously this is not a solution that is meant to scale at all.  In a real world situation, I'd set up a separate process to download the csv file every night and then update the info in a proper database like a Postgres instance or Aurora.  That way all the containers running this API would just hit that database and then it could scale appropriately.

- Which leads me to how I would scale it:  I'd just make a container, upload it to AWS ECR, and then spin up an ECS cluster or if I'm really feeling fancy, an EKS cluster.  But EKS would certainly be overkill for this small assignment.  For a global app, on the other hand, it is fantastic.  But ECS works fine, too!  As long as you set up separate clusters for each particular service, it's easy to scale.  But it is basic.  Definitely not as good or as powerful as Kubernetes, but sometimes simplicity is preferred.

- I chose Python because it is a fantastic language and very easy to develop for.  And for the vast majority of situation, it's good enough.  It's not as fast as other languages, but unless you're in a specific scenario that requires that speed, the development time saved by using Python is worth it.  Javascript/Typescript would have worked well, too, but I'm not as familiar with those languages.  And I chose Poetry to handle the project setup because it's very easy to use.

- I set up a couple of Github Actions for it, but I didn't get too deep into that.  With more time I would have it build the container and then upload it to ECR.  Perhaps even kick off deployment in ECS or EKS.