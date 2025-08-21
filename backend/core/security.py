from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import yaml
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def load_secret_key() -> str:
    """Load SECRET_KEY from config. Fallback to API section if security not present."""
    config_path = os.getenv("CONFIG_PATH", "../config/settings.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    # Prefer security.secret_key, fallback to api.secret_key
    if isinstance(config, dict):
        security = config.get("security", {}) or {}
        api = config.get("api", {}) or {}
        return security.get("secret_key") or api.get("secret_key") or "change-me"
    return "change-me"


SECRET_KEY = load_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
