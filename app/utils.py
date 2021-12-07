from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# def hash_password(password: str):
#    return pwd_context.hash(password)

hashed_pass = lambda password : pwd_context.hash(password)

#verify user password
verify_user = lambda hashed_password, plain_password: pwd_context.verify(hashed_password, plain_password)