from fastapi import FastAPI, UploadFile, File
import uvicorn
import logging


from hub_api.dna_api import (
    MinioTenant
)

import hub_api.environment as env


from utils import constants as cnt

from kubernetes import client, config

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to DNACLOUD API GATEWAY"}


# test
# @app.get("/homeassistant/", tags = ["HA"])
# async def proxy_home_assistant():
#     v1 = client.CoreV1Api()
#     service = v1.read_namespaced_service(name="home-assistant-service", namespace="default")
#     cluster_ip, port  = service.spec.cluster_ip, service.spec.ports[0]
#     print(cluster_ip,type(port))
    # async with httpx.AsyncClient() as client:
    #     # url = f"http://dnacloudserver.home:8123/"  # Adjust IP/port
    #     # response = await client.get(url)
    #     return response.json() if response.headers.get("Content-Type") == "application/json" else response.text

# test
# HA_SERVICE_URL = "http://home-assistant-service.default.svc.cluster.local:8123"  # Adjust port if needed

# @app.get("/fetch-ha-data", tags = ["HA"])
# async def fetch_ha_data():
#     async with httpx.AsyncClient() as client:
#         try:
#             # Example: Fetch something from Home Assistant API
#             response = await client.get(f"{HA_SERVICE_URL}")
#             response.raise_for_status()  # Raise an error for bad responses
#             return response.json()
#         except httpx.HTTPError as e:
#             return {"error": str(e)}

@app.post("/dnastorage", tags = ["saas-storage"])
async def upload_file(file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        minio_client = MinioTenant("minio.test-tenant.svc.cluster.local:80", "minio","minio123")
        result = minio_client.insert(file_data ,"testing")
    except Exception as e:
        return "Error: ",str(e)

# To run locally
if __name__ == "__main__":
    uvicorn.run("main:app", host = '0.0.0.0',port = 6001, log_level = "info")
    
