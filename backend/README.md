# Atominate Infrastructure Dashboard Backend

## Overview
This backend is built with FastAPI and provides REST API endpoints for managing Proxmox VMs, MinIO buckets, pfSense firewall rules, and general settings. It supports login, MFA, and JWT authentication.

## Setup Instructions

1. **Install dependencies**
   ```bash
   cd backend
   /home/ahmeddarder/Desktop/Up/.venv/bin/python -m pip install -r requirements.txt
   ```

2. **Configure API credentials**
   - Edit `proxmox_api.py`, `minio_api.py`, and `pfsense_api.py` with your server credentials.

3. **Run the backend server**
   ```bash
   /home/ahmeddarder/Desktop/Up/.venv/bin/python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. **API Endpoints**
   - `/api/login` — Login and get JWT token
   - `/api/mfa/setup` — Setup MFA for user
   - `/api/mfa/verify` — Verify MFA code
   - `/api/vms` — List VMs
   - `/api/vm/{vm_id}/action` — Run/Stop/Hibernate/Restart VM
   - `/api/vm/{vm_id}/backup` — Schedule VM backup
   - `/api/vm/{vm_id}/replicate` — Setup VM replication
   - `/api/vm/{vm_id}/snapshot` — Manage VM snapshots
   - `/api/minio/buckets` — List MinIO buckets
   - `/api/minio/bucket` — Create MinIO bucket
   - `/api/pfsense/firewall` — List/Create pfSense firewall rules
   - `/api/settings` — Get/Update general settings

5. **Frontend Integration**
   - Update your dashboard JS to use AJAX calls to these endpoints.
   - Pass JWT token in `Authorization: Bearer <token>` header for protected endpoints.

## Notes
- For production, use HTTPS and secure your credentials.
- You may need to adjust API URLs and credentials for your environment.
