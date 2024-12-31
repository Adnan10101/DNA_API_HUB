from pydantic import BaseModel
from typing import Optional

class Metadata(BaseModel):
    name: str
    uuid: Optional[str]
    
class PVClaimReference(BaseModel):
    kind: str
    claim_name: str
    claim_namespace: str
    
class NFSSystem(BaseModel):
    nfs_path: str
    nfs_server: str
    
class PVCSpec(BaseModel):
    access_modes: list
    storage_capacity: str
    claimRef: Optional[PVClaimReference]
    nfs: Optional[NFSSystem] = None
    
class GetPersistentVolume(BaseModel):
    meta: Metadata
    spec: PVCSpec
    
class CreatePVRequest(BaseModel):
    meta: Metadata
    capacity: str
    access_modes: list
    nfs: Optional[NFSSystem]
    pv_reclaim_policy: str
    
class CreatePVResponse(BaseModel):
    meta: Metadata
    message: str