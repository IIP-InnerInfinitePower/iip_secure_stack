import jwt

from .config import JWT_ALG, JWT_PUBLIC_KEY


def verify_jwt(token: str) -> dict:
    if not JWT_PUBLIC_KEY:
        return {}
    return jwt.decode(
        token, JWT_PUBLIC_KEY, algorithms=[JWT_ALG], options={"require": ["exp", "iat"]}
    )
