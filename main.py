from datetime import datetime
from typing import List
from fastapi.responses import JSONResponse, HTMLResponse
from pymongo import MongoClient
from fastapi import FastAPI, HTTPException
from models import Order, Product
import sys
from bson import ObjectId

app = FastAPI()

MONGODB_URI = "mongodb://localhost:27017/"

try:
    client = MongoClient(MONGODB_URI)
except:
    print("Database not connected")
    sys.exit(1)


db = client["ecommerce"]
products_collection = db["products"]
user_info = db["user_info"]
ordered_items = db["ordered_items"]
orders_collection = db["orders"]


# to add products in mongodb collection
# with open('products.json') as file:
#     file_data = json.load(file)
#     products_collection.insert_many(file_data)


@app.get("/")
async def home_page():
    return HTMLResponse(content='<h1>Welcome to E-Commerce API</h1>', status_code=200)


@app.get("/api/products/", response_model=List[Product])
async def list_products():
    products = list(products_collection.find({}))
    if not len(products):
        raise HTTPException(status_code=404, detail="No products to display")
    else:
        product_list = []
        for product in products:
            # Create a custom field with the ObjectId as a string
            product["product_id"] = str(product["_id"])
            product.pop("_id")  
            product_list.append(product)
    return JSONResponse(
        status_code=200,
        content={"products": product_list}
    )


@app.put('/api/product/{product_id}', response_model=Product)
async def update_product_quantity(product_id: str, updated_quantity: int):
    try:
        product_id = ObjectId(product_id)
        update_query = {"_id": product_id}
        update_operation = {
            "$set": {"available_quantity": updated_quantity}}
        result = products_collection.update_one(update_query, update_operation)
        if result.modified_count == 1:
            # If modified_count is 1, the update was successful
            return JSONResponse(
                status_code=201,
                content={"message": "Product quantity updated successfully"}
            )
        else:
            # If modified_count is not 1, the product with the given ID was not found
            raise HTTPException(status_code=404, detail="Product not found")
    except:
        raise HTTPException(status_code=404, detail="Product not found")


@app.post("/api/orders/", response_model=Order)
async def create_order(order: Order):
    order.timestamp = datetime.utcnow()
    insert_result = orders_collection.insert_one(order.model_dump())

    if not insert_result.inserted_id:
        raise HTTPException(status_code=400, detail="order failed !!!")
    return JSONResponse(
        status_code=201,
        content={'message': 'order placed successfully!'}
    )


@app.get("/api/allOrders", response_model=List[Order])
# pageNo is used instead of offset to make it easier for pagination working
async def get_all_orders(pageNo: int = 0, limit: int = 10):
    orders = list(orders_collection.find({}).skip(pageNo*limit).limit(limit))
    if not len(orders):
        raise HTTPException(status_code=404, detail="No orders to display")
    else:
        order_list = []
        for order in orders:
            order["order_id"], order["placedAt"] = str(
                order["_id"]), str(order["timestamp"])
            order.pop("_id")
            order.pop("timestamp")
            order_list.append(order)
    return JSONResponse(
        status_code=200,
        content={'data': order_list}
    )


@app.get("/api/getOrder/{order_id}", response_model=Order)
async def get_specific_order(order_id: str):
    try:
        order_id = ObjectId(order_id)
        filter_query = {"_id": order_id}
        result = orders_collection.find_one(filter_query)
        if result:
            result["order_id"], result["placedAt"] = str(
                result["_id"]), str(result["timestamp"])
            result.pop("_id")
            result.pop("timestamp")
            return JSONResponse(
                status_code=200,
                content={"order_details": result}
            )
        else:
            print("else")
            raise HTTPException(status_code=404, detail="Order not found")
    except:
        print("exe")
        raise HTTPException(status_code=404, detail="Order not found")


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    app_module = "main:app"
    uvicorn.run(app_module, host="localhost", port=8000, reload=True)
