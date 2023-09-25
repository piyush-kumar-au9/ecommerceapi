# E-Commerce FastAPI Application (Backend Assignment)

Welcome to the E-Commerce FastAPI Application! This application serves as a basic e-commerce system with CRUD operations for products and order management.

## Prerequisites

Before you can run this application, make sure you have the following prerequisites installed:

- Python (>= 3.10)
- MongoDB (Make sure it's running and accessible at `mongodb://localhost:27017/`)

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone <repository_url>
   cd <repository_directory>

# On macOS and Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate


# To install python packages
pip install -r requirements.txt

# to start the application
python main.py
The application should now be running at http://localhost:8000/

# Swagger docs
http://localhost:8000/docs


# API Endpoints
* GET /api/products/: List all available products.
* PUT /api/product/{product_id}: Update the quantity of a product by its ID.
* POST /api/orders/: Create a new order.
* GET /api/allOrders: List all orders with pagination support.
* GET /api/getOrder/{order_id}: Retrieve details of a specific order.

