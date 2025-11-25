# 2) Receive and validate the request from backend 
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Query(BaseModel):
    message: str

# 1) Setup the backend 
@app.post("/ask")
async def ask(query: Query):
    response = "This is the backend response"
    # 3) Send response to the frontend
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)