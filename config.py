import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY') or 'your-secret-key-here'
    
    # File uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16000 * 1024 * 1024  # 20000 MB limit
    ALLOWED_EXTENSIONS = {'rar','zip','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    
    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)