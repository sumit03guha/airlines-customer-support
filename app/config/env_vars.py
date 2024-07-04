import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FLASK_ENV: str = os.environ["FLASK_ENV"]

# Mongo credential
MONGO_HOST: str = os.environ["MONGO_HOST"]
MONGO_PORT: int = int(os.environ["MONGO_PORT"])
MONGO_ADMIN: str = os.environ["MONGO_ADMIN"]
MONGO_USER: str = os.environ["MONGO_USER"]
MONGO_PASSWORD: str = os.environ["MONGO_PASSWORD"]
DB_NAME: str = os.environ["DB_NAME"]
