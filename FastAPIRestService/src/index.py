from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/{itemId}")
async def getItem(itemId: int):
    if itemId < 0:
        return {"error": "itemId must be a non-negative integer"}
    
    return {"itemId": itemId , "message": "Hello World"}