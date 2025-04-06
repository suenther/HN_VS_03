from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.models.product import ProductCreate, Product

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["fastapi_db"]
products_collection = db["products"]

async def get_products():
    products = await products_collection.find().to_list(100)
    for product in products:
        product["id"] = str(product["_id"])
    return products


async def add_product(product: ProductCreate, response_model=Product):
    result = await products_collection.insert_one(product.dict())
    new_product = await products_collection.find_one({"_id": result.inserted_id})
    new_product["id"] = str(new_product["_id"])
    return new_product

async def update_product(product_id: str, product: dict):
    await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict(exclude_unset=True)}  # nur geaenderte Felder
    )
    updated_product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if updated_product:
        updated_product["id"] = str(updated_product["_id"])
    return updated_product

async def delete_product(product_id: str):
    await products_collection.delete_one({"_id": ObjectId(product_id)})
