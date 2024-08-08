# Stores REST API

This is a RESTful API for managing stores, items, and user authentication. It is built with Flask, Flask-Smorest, Flask-JWT-Extended, and SQLAlchemy. Redis is used for token blacklisting.

## Features

- **Store Management:** Create, read, update, and delete stores.
- **Item Management:** CRUD operations for items associated with stores.
- **User Authentication:** JWT-based authentication with token blacklisting.
- **Tagging System:** Associate tags with items.
- **Swagger UI:** Automatically generated API documentation.

## Technologies Used

- **Flask:** For creating the web application.
- **Flask-Smorest:** For building the REST API with OpenAPI support.
- **Flask-JWT-Extended:** For handling JWT-based authentication.
- **SQLAlchemy:** For database interactions.
- **Redis:** For storing the JWT blocklist.
- **SQLite:** Default database (can be configured to use other databases).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/p-forghani/stores-flask-api.git
    cd stores-flask-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    - `DATABASE_URL`: URL for the database connection.
    - `JWT_SECRET_KEY`: Secret key for JWT authentication.

5. Run the application:

    ```bash
    python app.py
    ```

## Usage

- **API Documentation:** Access Swagger UI at `http://localhost:5000/swagger-ui` to interact with the API.

## Example Requests

- **Get all stores:**

    ```bash
    GET /stores
    ```

- **Create a new item:**

    ```bash
    POST /items
    ```

## Deployment

Instructions for deploying this application to a production environment will be added later.

## Contributing

Contributions are welcome! Please create an issue or submit a pull request.
