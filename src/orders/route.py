from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import session
from database import get_db
from src.orders.model import OrderModel
from src.products.model import ProductModel
from src.orders.schema import OrderSchema, OrderUpdateSchema
import uuid

order_router = APIRouter()


@order_router.get("/orders")
def get_orders(db : session = Depends(get_db)):

    db_order = db.query(OrderModel).filter(OrderModel.is_deleted == False).all()

    if not db_order:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Order not found"
        )    
    
    return {
        "order" : db_order,
        "status" : status.HTTP_200_OK, 
        "message" : "Orders fetched successfully"
    }


@order_router.post("/orders")
def create_order(
    schema : OrderSchema,
    db : session = Depends(get_db)
):
    db_product = db.query(ProductModel).filter(ProductModel.id == schema.product_id).first()

    if db_product.quantity_in_stock < schema.quantity_ordered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select valide quantity"
        )
    
    new_order = OrderModel(
        id = str(uuid.uuid4()),
        product_id = schema.product_id,
        user_id = schema.user_id,
        quantity_ordered = schema.quantity_ordered,
    )

    db_product.quantity_in_stock = db_product.available_quantity - schema.quantity_ordered

    db.add(new_order)

    db.commit()

    db.refresh()


    
    return{
        "order" : new_order,
        "status" : status.HTTP_201_CREATED,
        "message" : "Order Placed successfully"
    }


@order_router.get("/orders/{order_id}")
def get_order(
    order_id : str,
    db : session = Depends(get_db)
):
    
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.is_deleted == False).first()

    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order not found or deleted"
        )
    
    return{
        "order" : db_order,
        "status" : status.HTTP_200_OK,
        "message" : "order fetched successfully"
    }


@order_router.patch("/orders/{order_id}")
def update_order(
    order_id : str,
    schema : OrderUpdateSchema,
    db : session = Depends(get_db)
):
    
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id, ProductModel.is_deleted == False).first()

    db_product = db.query(ProductModel).filter(ProductModel.id == db_order.product_id).first()

    if not db_order:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Product not found or deleted"
        )
    
    db_order.product_id = schema.product_id
    db_order.quantity_ordered = schema.quantity_ordered

    db.commit()
    db.refresh()

    return{
        "product" : db_order,
        "status" : status.HTTP_200_OK,
        "message" : "Product updated successfully"
    }


@order_router.delete("/orders")
def delete_order(
    order_id : str,
    db : session = Depends(get_db)
):
    
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id, OrderModel.is_deleted == False).first()

    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Order not found to delete"
        )
    
    db_order.is_deleted = True

    db.commit()

    return{
        "order_id" : order_id,
        "status" : status.HTTP_200_OK,
        "message" : "Product deleted successfully"
    }
