import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'users_v2.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY', 'f48cba10aa8b4f23932575c55bfb6d6c')
    
    # Firebase Config
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
    FIREBASE_AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN')
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
    FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')
    FIREBASE_MESSAGING_SENDER_ID = os.getenv('FIREBASE_MESSAGING_SENDER_ID')
    FIREBASE_APP_ID = os.getenv('FIREBASE_APP_ID')
    FIREBASE_MEASUREMENT_ID = os.getenv('FIREBASE_MEASUREMENT_ID')