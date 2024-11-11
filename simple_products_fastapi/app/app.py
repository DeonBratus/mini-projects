from fastapi import FastAPI, Body, status, Query, Depends, responses
from typing import Optional, List
from models import Product, check_product_exists
from database_handler import ProductDB, get_db
from sqlalchemy.orm import Session

app = FastAPI(
    title="Products API",
    description="API для управления продуктами ",
    version="1.0.0",
    docs_url="/api/docs",
)

# Получение всех продуктов с возможностью фильтрации
@app.get("/api/products", response_model=List[Product])
def get_products(
        category: Optional[str] = Query(None),
        min_price: Optional[float] = Query(None), 
        max_price: Optional[float] = Query(None),
        db: Session = Depends(get_db)
        ):
    
    query = db.query(ProductDB)

    if category:
        query = query.filter(ProductDB.category == category)
    if min_price is not None:
        query = query.filter(ProductDB.price >= min_price)
    if max_price is not None:
        query = query.filter(ProductDB.price <= max_price)

    return query


# Получение информации о продукте по id
@app.get("/api/products/{id}", response_model=Product)
def get_product_info(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == id).first()
    check_product_exists(product)
    return product

# Создание нового продукта
@app.post("/api/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(data: Product = Body(), db: Session = Depends(get_db)):
    new_product = ProductDB(
        id=data.id,
        product_title=data.product_title,
        category=data.category,
        price=data.price,
        description=data.description
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Обновление информации о продукте
@app.put("/api/products/{id}", response_model=Product)
def update_product(id: int, data: Product = Body(), db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == id).first()
    check_product_exists(product)

    product.product_title = data.product_title or product.product_title
    product.category = data.category or product.category
    product.price = data.price or product.price
    product.description = data.description or product.description

    db.commit()
    db.refresh(product)
    return product

# Удаление продукта
@app.delete("/api/products/{id}", response_model=dict)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == id).first()
    check_product_exists(product)
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.get("/")
def just_start_page():
    return responses.FileResponse("public/index.html")