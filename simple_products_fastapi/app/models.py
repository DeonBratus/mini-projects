from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    product_title: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

def check_product_exists(product):
    if product == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "product is not found"}
        )