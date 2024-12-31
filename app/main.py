from fastapi import FastAPI
import uvicorn
import logging
from volume_backend.vol import (
    fetching_pvs,
    create_pv
)
from volume_backend.schema import(
    CreatePVRequest
)
import volume_backend.environment as env

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI"}

@app.get("/volumeMount", tags = ["Volume Mount"])
async def get_persistent_volume():
    try:
        response = fetching_pvs()
        return response
    except Exception as e:
        logging.error("Error fetching Persistent Volume %s", e)
        return "Error fetching Persistent Volume.", 500

@app.post("/volumeMount", tags = ["Volume Mount"])
async def create_persistent_volume(request: CreatePVRequest):
    try:
        response = create_pv(request, env.PV_FILE_PATH, env.REPO_NAME)
        return response
    except Exception as e:
        logging.error("Error creating PV: %s", e)
        return "Error while creating PV.", 500

# To run locally
if __name__ == "__main__":
    uvicorn.run("main:app", host = '0.0.0.0',port = 6001, log_level = "info")