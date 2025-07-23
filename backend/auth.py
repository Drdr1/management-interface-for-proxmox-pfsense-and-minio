from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import pyotp
import qrcode 
import base64
import io

SECRET_KEY = 'supersecretkey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Dummy user store
users_db = {
    'admin': {
        'username': 'admin',
        'hashed_password': pwd_context.hash('admin'),
        'mfa_secret': pyotp.random_base32(),
    }
}

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in users_db:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def login_user(form_data):
    user = users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    # Issue JWT
    token = jwt.encode({"sub": user['username']}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

def setup_mfa(username):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate new secret if not exists
    if 'mfa_secret' not in user or not user['mfa_secret']:
        secret = pyotp.random_base32()
        user['mfa_secret'] = secret
    else:
        secret = user['mfa_secret']
    
    # Create TOTP object
    totp = pyotp.TOTP(secret)
    
    # Generate provisioning URI for QR code
    provisioning_uri = totp.provisioning_uri(
        name=username,
        issuer_name="Management Interface"
    )
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for web display
    buffer = io.BytesIO()
    qr_image.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        "secret": secret,
        "qr_code": f"data:image/png;base64,{qr_code_base64}",
        "provisioning_uri": provisioning_uri,
        "manual_entry_key": secret
    }

def verify_mfa(username, code):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if 'mfa_secret' not in user or not user['mfa_secret']:
        raise HTTPException(status_code=400, detail="MFA not set up for this user")
    
    totp = pyotp.TOTP(user['mfa_secret'])
    if totp.verify(code):
        return {"status": "MFA verified"}
    else:
        raise HTTPException(status_code=401, detail="Invalid MFA code")
        
def get_general_settings():
    return {"users": list(users_db.keys()), "ntp": "pool.ntp.org", "language": "en"}

def update_general_settings(params):
    # Implement settings update logic
    return {"status": "settings updated", "params": params}
