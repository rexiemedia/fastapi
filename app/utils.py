from passlib.context import CryptContext

pwd_context = CryptContext(
    # schemes=["pbkdf2_sha256", "des_crypt"],
    schemes=["bcrypt"],

    deprecated="auto",

    pbkdf2_sha256__rounds = 29000,
    )

def hash(password: str):
    return pwd_context.hash(password)

def verify_user(email: str, password: str):
    pass

def verify_admin(email: str, password: str):
    pass