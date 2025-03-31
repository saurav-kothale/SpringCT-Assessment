from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import session
from database import get_db
from src.products.model import ProductModel
from src.products.schema import ProductSchema
import uuid

product_router = APIRouter()


@product_router.get("/products")
def get_products(db : session = Depends(get_db)):

    db_product = db.query(ProductModel).filter(ProductModel.is_deleted == False).all()

    if not db_product:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Product not found"
        )    
    
    return {
        "product" : db_product,
        "status" : status.HTTP_200_OK, 
        "message" : "products fetched successfully"
    }


@product_router.post("/products")
def create_product(
    schema : ProductSchema,
    db : session = Depends(get_db)
):
    
    db_product = db.query(ProductModel).filter(ProductModel.name == schema.name).first()

    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is already exist"
        )
    
    new_product = ProductModel(
        id = str(uuid.uuid4()),
        name = schema.name,
        description = schema.description,
        price = schema.price,
        quantity_in_stock = schema.quantity_in_stock,
    )

    db.add(new_product)

    db.commit()

    db.refresh()


    
    return{
        "product" : new_product,
        "status" : status.HTTP_201_CREATED,
        "message" : "Product created successfully"
    }


@product_router.get("/products/{product_id}")
def get_product(
    product_id : str,
    db : session = Depends(get_db)
):
    
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id, ProductModel.is_deleted == False).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not found or deleted"
        )
    
    return{
        "product" : db_product,
        "status" : status.HTTP_200_OK,
        "message" : "product fetched successfully"
    }


@product_router.patch("/products/{product_id}")
def update_product(
    product_id : str,
    schema : ProductSchema,
    db : session = Depends(get_db)
):
    
    db_product = db.query(ProductModel).filter(ProductModel.product_id == product_id, ProductModel.is_deleted == False).first()


    if not db_product:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Product not found or deleted"
        )
    
    db_product.name = schema.name
    db_product.description = schema.description
    db_product.price = schema.price
    db_product.quantity_in_stock = schema.quantity_in_stock

    db.commit()
    db.refresh()

    return{
        "product" : db_product,
        "status" : status.HTTP_200_OK,
        "message" : "Product updated successfully"
    }


@product_router.delete("/products")
def delete_product(
    product_id : str,
    db : session = Depends(get_db)
):
    
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id, ProductModel.is_deleted == False).first()

    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Product not found to delete"
        )
    
    db_product.is_deleted = True

    db.commit()

    return{
        "product_id" : product_id,
        "status" : status.HTTP_200_OK,
        "message" : "Product deleted successfully"
    }
