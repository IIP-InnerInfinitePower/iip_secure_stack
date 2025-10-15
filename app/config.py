import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = <redacted>
DATABASE_URL = os.getenv("DATABASE_URL","")
RATE_PER_MIN = int(os.getenv("RATE_PER_MINUTE","60"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS","").split(",") if os.getenv("CORS_ORIGINS") else []
JWT_PUBLIC_KEY = <redacted> if os.getenv("JWT_PUBLIC_KEY") else None
JWT_ALG = os.getenv("JWT_ALG","RS256")
