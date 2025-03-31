from fastapi import FastAPI
import uvicorn
from src.products.route import product_router

app = FastAPI()

app.include_router(product_router, tags=["Products"])

@app.get("/")
def get_message():
    return {
        "message" : "working"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)