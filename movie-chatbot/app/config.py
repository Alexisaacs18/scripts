import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    SCRIPTS_DIR = os.getenv("SCRIPTS_DIR", "scripts")
    MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8192"))
