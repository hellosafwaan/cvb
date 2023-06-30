from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', '8000')
BACKEND_URL = os.getenv('BACKEND_URL')