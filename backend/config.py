import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_MODEL_ID = os.getenv("AWS_MODEL_ID")