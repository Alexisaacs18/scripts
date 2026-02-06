import os
from app.config import Config


class ScriptService:
    """Handles loading and managing reference movie scripts."""

    SUPPORTED_EXTENSIONS = (".txt", ".fountain", ".fdx", ".pdf")

    def __init__(self):
        self.scripts_dir = Config.SCRIPTS_DIR

    def _read_text_file(self, filepath: str) -> str:
        """Read plain text file (e.g. .txt, .fountain, .fdx)."""
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def _read_pdf(self, filepath: str) -> str:
        """Extract text from a PDF file."""
        from pypdf import PdfReader

        reader = PdfReader(filepath)
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        return "\n".join(parts)

    def load_scripts(self) -> list[dict]:
        """Load all scripts from the scripts directory."""
        scripts = []
        if not os.path.isdir(self.scripts_dir):
            return scripts

        for filename in sorted(os.listdir(self.scripts_dir)):
            if not filename.lower().endswith(self.SUPPORTED_EXTENSIONS):
                continue
            filepath = os.path.join(self.scripts_dir, filename)
            try:
                if filename.lower().endswith(".pdf"):
                    content = self._read_pdf(filepath)
                else:
                    content = self._read_text_file(filepath)
                if content.strip():
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
