from passlib.context import CryptContext
pass_context = CryptContext(schemes=["sha256_crypt"])

def hash(password: str):
    # This is already salted --
    # -- from passlib docs --
    # sha256_crypt is complex password hash algo
    # containaing a randomly generated salt,
    # variable rounds, etc.
    return pass_context.hash(password)

def verify(plain_password, hashed_password):
    # look for verify_and_update?
    return pass_context.verify(plain_password, hashed_password)

