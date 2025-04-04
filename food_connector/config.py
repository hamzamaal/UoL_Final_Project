# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
