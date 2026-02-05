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
        """Generate or revise a movie script using the full conversation history."""
        system_prompt = self._build_system_prompt(reference_scripts, page_count)

        full_messages = [{"role": "system", "content": system_prompt}] + messages

        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE,
        )

        return response.choices[0].message.content

    def _build_system_prompt(self, reference_scripts: list[dict], page_count: int) -> str:
        """Build the system prompt with reference scripts and screenplay formatting rules."""
        script_context = ""
        for script in reference_scripts:
            script_context += f"\n--- {script['name']} ---\n{script['content']}\n"

        return f"""You are a professional Hollywood screenwriter. You produce screenplays in
industry-standard format. Every script you write MUST follow these formatting rules exactly:

═══════════════════════════════════════════════
SCREENPLAY FORMATTING RULES
═══════════════════════════════════════════════

1. TITLE PAGE (first page only):
   - Title in ALL CAPS, centered
   - "Written by" centered below
   - Author name centered below that
   - Blank line, then "FADE IN:" flush left to begin the script

2. SCENE HEADINGS (slug lines):
   - ALL CAPS, flush left
   - Format: INT. or EXT. (or INT./EXT.) followed by LOCATION - TIME
   - Examples:
     INT. DETECTIVE'S OFFICE - NIGHT
     EXT. CITY ROOFTOP - DAWN
     INT./EXT. MOVING CAR - DAY

3. ACTION / DESCRIPTION:
   - Written in present tense, flush left
   - Brief, visual, cinematic — show don't tell
   - Introduce characters in ALL CAPS the first time only
   - Example:
     SARAH CHEN (30s, sharp eyes, ink-stained fingers) pushes through
     the revolving door into the marble lobby.

4. CHARACTER NAME (before dialogue):
   - ALL CAPS, centered (indented ~3.7 inches / ~37 spaces from left)
   - If off-screen, add (O.S.) — if voice over, add (V.O.)
   - Example:
                                     SARAH
                                     DETECTIVE HARRIS (O.S.)

5. PARENTHETICALS:
   - On their own line, indented (~3.1 inches / ~31 spaces from left)
   - Lowercase, in parentheses — used sparingly
   - Example:
                               (whispering)
                               (into phone)

6. DIALOGUE:
   - Indented (~2.5 inches / ~25 spaces from left)
   - Wraps at ~3.5 inches width
   - Example:
                         I told you — I don't know where
                         the money went. And even if I
                         did, I wouldn't tell you.

7. TRANSITIONS:
   - ALL CAPS, flush right (or flush left)
   - Use sparingly: CUT TO:, SMASH CUT TO:, DISSOLVE TO:, MATCH CUT TO:
   - "FADE IN:" at the start, "FADE OUT." at the end

8. SPECIAL ELEMENTS:
   - MONTAGE: labeled "MONTAGE - DESCRIPTION" as a slug line
   - INTERCUT: "INTERCUT - LOCATION A / LOCATION B"
   - SUPER: "SUPER: 'Text to display on screen'"
   - (MORE) at bottom of page when dialogue continues, (CONT'D) after character name on next page

═══════════════════════════════════════════════

REFERENCE SCRIPTS (study these for tone, pacing, and style):
{script_context if script_context else "(No reference scripts loaded yet. Write in a polished, cinematic Hollywood style.)"}

INSTRUCTIONS:
- Generate an original screenplay based on the user's prompt.
- The script MUST be approximately {page_count} pages long.
- One screenplay page ≈ 250 words, so target approximately {page_count * 250} words total.
- Apply the formatting rules above precisely — use spaces for indentation, not tabs.
- Include a title page at the very beginning.
- Structure the story with clear three-act structure (setup, confrontation, resolution).
- If the user asks for changes, revisions, or edits to a previously generated script, apply
  those changes and return the full updated screenplay.
- Always deliver the COMPLETE screenplay in your response — never truncate or summarize."""
