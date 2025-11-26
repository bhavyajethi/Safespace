# 2) Receive and validate the request from backend 
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agent import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()

class Query(BaseModel):
    message: str

# 1) Setup the backend 
@app.post("/ask")
async def ask(query: Query):
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
    stream = graph.stream(inputs, stream_mode="updates")
    final_response = parse_response(stream)

    # 3) Send response to the frontend
    return {"response": final_response}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)