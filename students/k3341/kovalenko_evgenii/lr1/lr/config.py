from dotenv import load_dotenv
from os import getenv

load_dotenv()

DB_URL = getenv('DB_URL')
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = getenv('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = getenv('ACCESS_TOKEN_EXPIRE_MINUTES')