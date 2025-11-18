import logging
import os

# Base configuration for the Flask application
class BaseConfig:
    # Set the timezone to Europe/Rome for consistency with Italy
    TIMEZONE = 'Europe/Rome' 
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.INFO
    UPLOAD_FOLDER = os.path.abspath('temp_uploads')
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024 # 20MB Max file size

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    # Local environment variables should be set here if not using Docker
