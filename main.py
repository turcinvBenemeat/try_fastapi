from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/hi")
def greet():
    return f"Hello? World?"

# URL Path
@app.get("/hi/{name}")
def greet(name: str):
    return f"Hello? {name}?"

# Query Parameters
@app.get("/hello")
def hello(name: str):
    return f"Hello, {name}?"

@app.get("/ping")
def ping():
    return {"ping": "pong"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)