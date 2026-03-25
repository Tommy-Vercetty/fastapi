from typing import Union
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"Welcome to Tommy's FAST Api!"}

@app.get("/getSingleProduct")

@app.get("/getAll")

@app.post("/addNew")

@app.get("/deleteOne")

@app.get("/startsWith")

@app.get("/paginate")

@app.get("/convert")


