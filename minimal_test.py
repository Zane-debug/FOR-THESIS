#!/usr/bin/env python3
"""
Minimal test to isolate the server startup issue
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    return {"status": "working"}

if __name__ == "__main__":
    print("🧪 Starting minimal test server...")
    print("📡 Server will be available at: http://localhost:8004")
    uvicorn.run(app, host="127.0.0.1", port=8004)
