#import kubernetes.client.models.v1_persistent_volume
from fastapi import HTTPException
import requests
import yaml
from jinja2 import Template
from kubernetes import client, config
from  volume_backend.schema import (
    Metadata,
    GetPersistentVolume,
    PVClaimReference,
    NFSSystem,
    PVCSpec,
    CreatePVRequest,
    CreatePVResponse
)
import logging
import volume_backend.environment as env
from volume_backend.gitea import GitWrapper
import argocd_client


logger = logging.getLogger("fastapi_app")
config.load_config()

pv_claim = """
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {{ meta.name }}
spec:
  capacity:
    storage: {{ capacity }}  # Adjust this size as needed
  accessModes:
  {% for mode in access_modes %}
  - {{mode}}  # NFS supports ReadWriteMany
  {% endfor %}
  nfs:
    path: {{ nfs.nfs_path }}  # Path on the NFS server
    server: {{ nfs.nfs_server }}
  persistentVolumeReclaimPolicy: {{ pv_reclaim_policy }}
"""

def fetching_pvs():
    v1 = client.CoreV1Api()
    pv_list = v1.list_persistent_volume()
    Responses = []
    for pv in pv_list.items:
        metadata = Metadata(
            name = pv.metadata.name,
            uuid = pv.metadata.uid
        )
        
        spec = GetPVSpec(pv.spec)
        Response = GetPersistentVolume(
            meta = metadata,
            spec = spec
        )
        Responses.append(Response)
        
    return Responses

def GetPVSpec(spec):
    return PVCSpec(
        access_modes = spec.access_modes,
        storage_capacity = spec.capacity['storage'],
        claimRef = GetPVClaim(spec.claim_ref),
        nfs = GetNFS(spec.nfs)
    )

def GetPVClaim(claim):
    if claim == None:
        return None
    return PVClaimReference(
        kind = claim.kind,
        claim_name = claim.name,
        claim_namespace = claim.namespace,
    )
    
def GetNFS(nfs):
    if nfs == None:
        return None
    return NFSSystem(nfs_path = nfs.path, nfs_server = nfs.server)

def create_pv(request: CreatePVRequest, FILE_PATH, REPO_NAME):
    yaml_contents, file_name = pv_template(request)
    git_create(yaml_contents, file_name, FILE_PATH, REPO_NAME)
    response = CreatePVResponse(
        meta = request.meta,
        message = "Created and Pushed PV to gitea!"
    )
    return response

def git_create(yaml_contents, file_name, FILE_PATH, REPO_NAME):
    git = GitWrapper()
    git.create_file(yaml_contents, file_name, FILE_PATH, REPO_NAME)

def pv_template(request):
    template = Template(pv_claim)
    rendered_yaml = template.render(request.dict())
    file_name = f'{request.meta.name}.yaml'
    return rendered_yaml, file_name
