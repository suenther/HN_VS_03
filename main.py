from fastapi import Request, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.product_service import get_products, add_product, delete_product, update_product
from app.models.product import ProductCreate, Product, ProductUpdate


app = FastAPI()
templates = Jinja2Templates(directory="app/views/templates")

@app.get("/products/view", response_class=HTMLResponse)
async def view_products(request: Request):
    products = await get_products()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.post("/products", response_model=Product)
async def handle_add_product(product: ProductCreate):
   return await add_product(product)

@app.get("/products", response_model=list[Product])
async def handle_get_products():
   return await get_products()

@app.delete("/products/{id}")
async def handle_delete_product(id: str):
    return await delete_product(id)

@app.put("/products/{id}", response_model=Product)
async def handle_update_product(id: str, product: ProductUpdate):
    return await update_product(id, product)