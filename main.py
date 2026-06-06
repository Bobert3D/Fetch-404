from fastapi import FastAPI

app = FastAPI()

#  Fixed: Explicit root route
@app.get("/")
def read_root():
    return {"message": "Hello World"}
