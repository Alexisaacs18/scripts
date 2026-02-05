import os
from app.config import Config


class ScriptService:
    """Handles loading and managing reference movie scripts."""

    SUPPORTED_EXTENSIONS = (".txt", ".fountain", ".pdf", ".fdx")

    def __init__(self):
        self.scripts_dir = Config.SCRIPTS_DIR

    def load_scripts(self) -> list[dict]:
        """Load all scripts from the scripts directory."""
        scripts = []
        if not os.path.isdir(self.scripts_dir):
            return scripts

        for filename in sorted(os.listdir(self.scripts_dir)):
            if filename.lower().endswith(self.SUPPORTED_EXTENSIONS):
                filepath = os.path.join(self.scripts_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    scripts.append({"name": filename, "content": content})
                except Exception:
                    continue

        return scripts

    def list_scripts(self) -> list[str]:
        """Return names of all available reference scripts."""
        if not os.path.isdir(self.scripts_dir):
            return []
        return [
            f for f in sorted(os.listdir(self.scripts_dir))
            if f.lower().endswith(self.SUPPORTED_EXTENSIONS)
        ]
