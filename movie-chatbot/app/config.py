import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
    LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")
    MODEL = os.getenv("LM_STUDIO_MODEL", "openai/gpt-oss-20b")
    SCRIPTS_DIR = os.getenv("SCRIPTS_DIR", "scripts")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    # Max characters to include from each reference script (keeps context small)
    MAX_SCRIPT_CHARS = int(os.getenv("MAX_SCRIPT_CHARS", "1500"))
    # Max conversation history messages to send (user + assistant pairs)
    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "4"))
