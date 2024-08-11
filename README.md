## Table Of Contents

- [The Project](#about-the-project)
- [Features](#features)
- [Demo Video](#demo_video)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)

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
