# Electronics E-Commerce API

A backend API for an electronics e-commerce platform built with **FastAPI** and **PostgreSQL**. The API handles users, products, categories, shopping carts, orders, and Stripe payments.

## 🚀 Live Demo

**Live API:**
https://ecom-fastapi-production.up.railway.app

**Swagger / OpenAPI Documentation:**
https://ecom-fastapi-production.up.railway.app/docs

The API is deployed using **Docker on Railway** with a **PostgreSQL database**.

## Tech Stack

- **Python / FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **JWT Authentication**
- **Stripe**
- **Docker / Docker Compose**
- **Railway**

## Features

- User registration and login
- JWT authentication and protected endpoints
- User roles and admin management
- Product and category management
- Product search and pagination
- Shopping cart management
- Order creation and management
- Stripe Checkout payments
- Payment verification and order confirmation
- PostgreSQL database integration
- Dockerized FastAPI and PostgreSQL services
- Swagger / OpenAPI documentation
- Production deployment with HTTPS

## Run with Docker

Create your `.env` file with the required database, authentication, and Stripe configuration.

Build the API image:

```bash
docker build -t electronics-ecommerce-api:latest .
```

Start the application:

```bash
docker compose up
```

The API will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

## Docker Services

```text
FastAPI API  →  PostgreSQL
   :8000          :5432
```

PostgreSQL data is persisted using a Docker volume.

## Payment

Stripe Checkout is integrated using Stripe's test environment. Successful payments update the payment and order status accordingly.

## Deployment

The application is deployed to **Railway** using Docker, with PostgreSQL as the production database.

The live Swagger documentation is available at:

```text
https://ecom-fastapi-production.up.railway.app/docs
```

## Author

**Abdulrahman Nganje**
https://github.com/asnganje

**Python | FastAPI | Web Scraping & Browser Automation Specialist**
