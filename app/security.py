from jose import jwt, JWTError
from passlib.context import CryptContext
from jose import jwt


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# JWT settings
SECRET_KEY = "hirehub-secret-key-change-this-later"
ALGORITHM = "HS256"


# -------------------------
# PASSWORD FUNCTIONS
# -------------------------

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------
# JWT FUNCTION
# -------------------------

def create_access_token(data: dict):
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None