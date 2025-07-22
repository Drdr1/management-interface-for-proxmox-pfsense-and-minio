from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import pyotp

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
    secret = pyotp.random_base32()
    user['mfa_secret'] = secret
    return {"secret": secret}

def verify_mfa(username, code):
    user = users_db.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
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
