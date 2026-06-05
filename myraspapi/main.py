from fastapi import FastAPI
import uvicorn

app = FastAPI()
@app.get("/hello")
def hello():
    return {"message": "Hello, RaspAPI!"}

uvicorn.run(app)