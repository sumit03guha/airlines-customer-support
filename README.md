# Airline Customer Support API

This project is an Airline Customer Support API built with Flask and Flask-RESTX. It allows customers to create, modify, cancel bookings, and add Value Added Services (VAS) to their bookings. The data is stored in a MongoDB database.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)

## Installation

### Prerequisites

- Python 3.12+
- MongoDB
- [Poetry](https://github.com/python-poetry/poetry) (for dependency management)

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/airline-customer-support-api.git
   cd airline-customer-support-api
   ```

2. Install dependencies using Poetry:

   ```sh
   poetry install --no-root --without dev
   ```

3. Set up the MongoDB connection string:

   - Create a `.env` file at the root of the project
   - Add your MongoDB connection string in the `.env` file:

   ```sh
   MONGO_URI=mongodb://localhost:27017/airline_support_db
   ```

## Running the Application

1. Start your MongoDB server.

2. Run the Flask application:

   ```sh
   poetry run python run.py
   ```

3. The API will be available at `http://127.0.0.1:5000/`.

4. You can access the Swagger UI for the API documentation at `http://127.0.0.1:5000/`.

## API Endpoints

### Create a new booking

- **URL:** `/bookings/`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "customer_name": "John",
    "last_name": "Doe",
    "flight_number": "AB123",
    "departure_date": "2024-07-10"
  }
  ```

- **Response:**

  ```json
  {
    "customer_name": "John",
    "last_name": "Doe",
    "flight_number": "AB123",
    "departure_date": "2024-07-10",
    "status": "confirmed",
    "vas": [],
    "pnr": "ABC123"
  }
  ```

### Get a booking

- **URL:** `/bookings/{pnr}/{last_name}`
- **Method:** `GET`
- **Response:**

  ```json
  {
    "customer_name": "John",
    "last_name": "Doe",
    "flight_number": "AB123",
    "departure_date": "2024-07-10",
    "status": "confirmed",
    "vas": [],
    "pnr": "ABC123"
  }
  ```

### Modify a booking

- **URL:** `/bookings/{pnr}/{last_name}`
- **Method:** `PATCH`
- **Request Body:**

  ```json
  {
    "customer_name": "Jane"
  }
  ```

- **Response:**

  ```json
  {
    "customer_name": "Jane",
    "last_name": "Doe",
    "flight_number": "AB123",
    "departure_date": "2024-07-10",
    "status": "confirmed",
    "vas": [],
    "pnr": "ABC123"
  }
  ```

### Cancel a booking

- **URL:** `/bookings/{pnr}/{last_name}`
- **Method:** `DELETE`
- **Response:** `204 No Content`

### Add VAS to a booking

- **URL:** `/bookings/{pnr}/{last_name}/vas`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "vas": ["Extra legroom", "Meal"]
  }
  ```

- **Response:**

  ```json
  {
    "customer_name": "John",
    "last_name": "Doe",
    "flight_number": "AB123",
    "departure_date": "2024-07-10",
    "status": "confirmed",
    "vas": ["Extra legroom", "Meal"],
    "pnr": "ABC123"
  }
  ```

## Testing

### Unit and Integration Tests

1. Ensure MongoDB is running.
2. Run the tests using pytest:

   ```sh
   poetry run pytest
   ```

## Project Structure

```sh
airline-customer-support-api/
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── booking.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── repository.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── booking.py
│
├── tests/
│   ├── __init__.py
│   ├── test_integration.py
│   ├── conftest.py
│
├── .env
├── run.py
├── pyproject.toml
└── README.md
```

## Dependencies

- Flask
- Flask-RESTX
- PyMongo
- pytest
- pytest-flask
- Python-dotenv
- Poetry

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
