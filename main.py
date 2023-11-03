from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# TODO: get instantclient connection in python to work here, reference OCI-Connection

# all routes must be defined above mounting build directory else fastapi will think the route is a static file
@app.get("/test/hello")
async def hello():
    return {"message": "Hello World"}

# mount build directory
app.mount("/", StaticFiles(directory="build", html=True), name="static")
