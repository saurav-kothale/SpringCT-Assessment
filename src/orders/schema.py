from pydantic import BaseModel

class OrderSchema(BaseModel):
    product_id : str
    user_id : str
    quantity_ordered : int

class OrderUpdateSchema(BaseModel):
    product_id : str
    quantity_ordered : int
    