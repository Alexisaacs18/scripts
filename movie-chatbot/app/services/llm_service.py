from openai import OpenAI
from app.config import Config


class LLMService:
    """Handles communication with LM Studio's OpenAI-compatible API."""

    def __init__(self):
        self.client = OpenAI(
            base_url=Config.LM_STUDIO_BASE_URL,
            api_key=Config.LM_STUDIO_API_KEY,
        )
        self.model = Config.MODEL

    def generate(self, messages: list[dict], page_count: int, reference_scripts: list[dict]) -> str:
        """Generate or revise a scene using the conversation history."""
        system_prompt = self._build_system_prompt(reference_scripts, page_count)

        # Trim conversation history to stay within context limits
        trimmed = messages
        max_msgs = Config.MAX_HISTORY_MESSAGES * 2
        if len(messages) > max_msgs:
            trimmed = messages[-max_msgs:]

        full_messages = [{"role": "system", "content": system_prompt}] + trimmed

        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE,
        )

        return response.choices[0].message.content

    def _build_system_prompt(self, reference_scripts: list[dict], page_count: int) -> str:
        """Build a compact system prompt for scene generation."""
        script_snippets = ""
        max_chars = Config.MAX_SCRIPT_CHARS
        for script in reference_scripts:
            snippet = script["content"][:max_chars]
            if len(script["content"]) > max_chars:
                snippet += "\n[...truncated for context]"
            script_snippets += f"\n--- {script['name']} ---\n{snippet}\n"

        word_target = page_count * 250

        return f"""You are a screenwriter. Write scenes in standard screenplay format.

FORMAT RULES:
- Scene headings: ALL CAPS, flush left (INT. LOCATION - TIME or EXT. LOCATION - TIME)
- Action: Present tense, flush left. First character appearance in ALL CAPS.
- Character name: ALL CAPS, centered above their dialogue
- Parentheticals: (lowercase, centered) on own line before dialogue
- Dialogue: Centered block below character name
- Transitions: ALL CAPS, right-aligned (CUT TO:, FADE OUT., etc.)

{f"REFERENCE STYLE (mimic tone/pacing, do not copy):{script_snippets}" if script_snippets else ""}
OUTPUT: Write a {page_count}-page scene (~{word_target} words). Use proper screenplay format. Deliver the complete scene."""
