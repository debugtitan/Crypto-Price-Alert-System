## Table Of Contents

- [The Project](#about-the-project)
- [Features](#features)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Docs](#documentation)

## About The Project

This is a Price Alert System to monitor the price of Solana (SOL) and send real-time alerts when the prices cross set thresholds. The system helps users make timely trading decisions by notifying them via email when the price reaches their target values. Users can customize alerts for price movements in both upward and downward directions.

## Features

- User authentication using email login
- User can add different price range to monitor price movements either up or down
- user can delete price

## Built With

- Python
- Django
- Postgresql
- Celery
- Redis (for Celery broker)

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

- install python3.10 or above
- install postgresql
- Install Docker (optional, if you prefer using Docker for setup).

### Installation

- Clone your project locally:

```bash
git clone https://github.com/debugtitan/Crypto-Price-Alert-System.git
cd Crypto-Price-Alert-System
```

- Create a .env file and use the .env.example as a template to set up your environment variables.

- ## Using Docker

  Run the following command to start the services

  - Run docker compose up

- ## Manually

  - Create and activate your virtual environment

  - Install project dependencies::

    ```bash
    # With python
    pip install requirements.txt
    ```

  - Apply migrations:

    ```bash
    python3 manage.py migrate
    ```

  - Start the development server
    ```bash
    python3 manage.py runserver
    ```

### DOcumentation

# AuthViewSet

The `AuthViewSet` class provides endpoints for user authentication using email login.

## BASE URL

```bash
https://price-watcher.debugtitan.com/api/v1
```

### Initialize Email Login

`POST /auth/initialize_email_login/`

#### Description

Sends a login code to the user's email address.

#### Request

**Headers:**

- `Content-Type: application/json`

**Body:**

```json
{
  "email": "user@debug.com"
}
```

**Response**

Status: 200 OK

**Body:**

```json
{
  "message": "A login code has been sent to user@debug.com"
}
```

## Finalize Email Login

`POST /auth/finalize_email_login`

### Description

Login a user.

### Request

**Headers:**

- `Content-Type: application/json`

**Body:**

```json
{
  "email": "user@debug.com",
  "token": "190651"
}
```

**Response**

Status: 200 OK

**Body:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "token": {
    "refresh": "refresh_token",
    "access": "access_token"
  }
}
```

## Alert Management

### List Alerts

**Endpoint:** `GET /alerts/`

**Description:**  
Retrieve all alerts created by the authenticated user.

**Request:**

**Headers:**

- `Authorization: Bearer <your_token>`

**Response:**

**Status Code:** 200 OK

**Body:**

```json
[
  {
    "id": 1,
    "target_price": 5000,
    "owner": 1
  },
  {
    "id": 2,
    "target_price": 10000,
    "owner": 1
  }
]
```

### Create Alert

**Endpoint:** `POST /alerts/`

**Description:**  
Create a new price alert for the authenticated user. This alert requires both a target price and a direction to trigger notifications.

**Request:**

**Headers:**

- `Content-Type: application/json`
- `Authorization: Bearer <your_token>`

**Body:**

```json
{
  "target_price": 7500,
  "direction": "HIGH"
}
```

### Fields:

- target_price (required): The price at which the alert should trigger.
- direction (optional): The direction for the alert. Can be "HIGH" or "LOW". default is "HIGH"

Response:

Status Code: 201 Created

**Body:**

```json
{
  "id": 3,
  "target_price": 7500,
  "direction": "above",
  "owner": 1
}
```

### Delete Alert

**Endpoint:** `DELETE /alerts/{id}/`

**Description:**  
Delete an existing alert created by the authenticated user.

**Request:**

**Headers:**

- `Authorization: Bearer <your_token>`

**Path Parameters:**

- `id` (required): The ID of the alert to be deleted.

**Response:**

**Status Code:** 204 No Content

**Description:**  
The alert was successfully deleted.

**Errors:**

**Status Code:** 404 Not Found

**Body:**

```json
{
  "detail": "Not found."
}
```
