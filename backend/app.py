from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext
import pyotp
from proxmoxer import ProxmoxAPI
from minio import Minio
import requests

from .proxmox_api import *
from .minio_api import *
from .pfsense_api import *
from .auth import *

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/vms")
def list_vms(token: str = Depends(verify_token)):
    return proxmox_list_vms()

@app.post("/api/vm/{vm_id}/action")
def vm_action(vm_id: int, action: str, token: str = Depends(verify_token)):
    return proxmox_vm_action(vm_id, action)

@app.post("/api/vm/{vm_id}/backup")
def vm_backup(vm_id: int, schedule: dict, token: str = Depends(verify_token)):
    return proxmox_vm_backup(vm_id, schedule)

@app.post("/api/vm/{vm_id}/replicate")
def vm_replicate(vm_id: int, params: dict, token: str = Depends(verify_token)):
    return proxmox_vm_replicate(vm_id, params)

@app.post("/api/vm/{vm_id}/snapshot")
def vm_snapshot(vm_id: int, params: dict, token: str = Depends(verify_token)):
    return proxmox_vm_snapshot(vm_id, params)

@app.get("/api/minio/buckets")
def list_buckets(token: str = Depends(verify_token)):
    return minio_list_buckets()

@app.post("/api/minio/bucket")
def create_bucket(params: dict, token: str = Depends(verify_token)):
    return minio_create_bucket(params)

@app.get("/api/pfsense/firewall")
def list_firewall(token: str = Depends(verify_token)):
    return pfsense_list_firewall()

@app.post("/api/pfsense/firewall")
def create_firewall(params: dict, token: str = Depends(verify_token)):
    return pfsense_create_firewall(params)

@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_user(form_data)

@app.post("/api/mfa/setup")
def mfa_setup(username: str):
    return setup_mfa(username)

@app.post("/api/mfa/verify")
def mfa_verify(username: str, code: str):
    return verify_mfa(username, code)

@app.get("/api/settings")
def get_settings(token: str = Depends(verify_token)):
    return get_general_settings()

@app.post("/api/settings")
def update_settings(params: dict, token: str = Depends(verify_token)):
    return update_general_settings(params)
