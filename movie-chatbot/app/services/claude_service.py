import anthropic
from app.config import Config


class ClaudeService:
    """Handles communication with the Claude API for script generation."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.MODEL

    def generate(self, prompt: str, page_count: int, reference_scripts: list[dict]) -> str:
        """Generate a movie script using Claude, informed by reference scripts."""
        system_prompt = self._build_system_prompt(reference_scripts, page_count)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=Config.MAX_TOKENS,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return message.content[0].text

    def _build_system_prompt(self, reference_scripts: list[dict], page_count: int) -> str:
        """Build the system prompt with reference scripts and formatting instructions."""
        script_context = ""
        for script in reference_scripts:
            script_context += f"\n--- {script['name']} ---\n{script['content']}\n"

        return f"""You are a professional screenwriter. You write movie scripts in proper
screenplay format (scene headings, action lines, character names, dialogue, parentheticals).

The user has provided the following reference scripts for you to study and learn from.
Absorb the tone, structure, pacing, dialogue style, and storytelling techniques from these
scripts. Use them as inspiration — do NOT copy them directly.

REFERENCE SCRIPTS:
{script_context if script_context else "(No reference scripts loaded yet.)"}

INSTRUCTIONS:
- Generate an original screenplay based on the user's prompt.
- The script should be approximately {page_count} pages long.
- One page of a screenplay is roughly 250 words, so target ~{page_count * 250} words.
- Use standard screenplay format throughout.
- Include a title page at the beginning.
- Deliver the full script in a single response."""
