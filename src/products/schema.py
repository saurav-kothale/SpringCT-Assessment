from pydantic import BaseModel

class ProductSchema(BaseModel):
    name : str
    description : str
    price : float
    quantity_in_stock : int