import os
from dotenv import load_dotenv


load_dotenv()

UPSCAYL_PATH = os.getenv('UPSCAYL_PATH')
MODEL_PATH = os.getenv('MODEL_PATH')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER')
