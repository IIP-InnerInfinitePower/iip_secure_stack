import jwt
from .config import JWT_PUBLIC_KEY, JWT_ALG
def verify_jwt(token: str) -> dict:
    if not JWT_PUBLIC_KEY:
        return {}
    return jwt.decode(token, JWT_PUBLIC_KEY, algorithms=[JWT_ALG], options={"require": ["exp","iat"]})
