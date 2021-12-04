from passlib.context import CryptContext

pwd_context = CryptContext(
    # schemes=["pbkdf2_sha256", "des_crypt"],
    schemes=["bcrypt"], deprecated="auto", 
    pbkdf2_sha256__rounds = 29000,
    )

def hash(password: str):
    return pwd_context.hash(password)

def authenticate(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
