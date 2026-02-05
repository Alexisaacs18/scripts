import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
    LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")
    MODEL = os.getenv("LM_STUDIO_MODEL", "default")
    SCRIPTS_DIR = os.getenv("SCRIPTS_DIR", "scripts")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8192"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
