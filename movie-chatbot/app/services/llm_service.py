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

        return f"""You are a professional screenwriter. Write vivid, cinematic scenes in industry-standard screenplay format.

FORMAT RULES:
- Scene headings: ALL CAPS, flush left (INT. LOCATION - TIME or EXT. LOCATION - TIME)
- Action/description: Present tense, flush left. Paint the picture — describe the setting, lighting, atmosphere, character body language, and what the camera sees. First character appearance in ALL CAPS with a brief physical description.
- Camera directions: ALL CAPS on their own line when needed (CLOSE ON, WIDE SHOT, ANGLE ON, POV, TRACKING SHOT, PAN TO, OVER THE SHOULDER, TWO SHOT, INSERT, etc.)
- Character name: ALL CAPS, centered above their dialogue
- Parentheticals: (lowercase, centered) on own line before dialogue — for tone, action during speech
- Dialogue: Centered block below character name
- Transitions: ALL CAPS, right-aligned (CUT TO:, SMASH CUT TO:, FADE OUT., MATCH CUT TO:, etc.)
- Beats: Use "(beat)" parenthetical or describe pauses/silences in action lines to control pacing

WRITING STYLE:
- Balance dialogue with rich action/description. Do NOT write dialogue-only scenes.
- Describe what the audience SEES and HEARS — camera movement, lighting shifts, sound design, environment details.
- Use camera directions to emphasize key moments (a reaction shot, a revealing close-up, a dramatic wide shot).
- Include beats and pauses for tension and rhythm.
- Show character emotions through physical behavior, not just words.

{f"REFERENCE STYLE (mimic tone/pacing, do not copy):{script_snippets}" if script_snippets else ""}
OUTPUT: Write a {page_count}-page scene (~{word_target} words). Use proper screenplay format with camera directions, visual descriptions, and beats throughout. Deliver the complete scene."""
