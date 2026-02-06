import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


COURIER = "Courier"
COURIER_BOLD = "Courier-Bold"

# Standard screenplay margins: 1.5" left, 1" right, 1" top/bottom
PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT_MARGIN = 1.5 * inch
RIGHT_MARGIN = 1.0 * inch
TOP_MARGIN = 1.0 * inch
BOTTOM_MARGIN = 1.0 * inch

STYLES = {
    "scene_heading": ParagraphStyle(
        "SceneHeading", fontName=COURIER_BOLD, fontSize=12,
        leading=12, alignment=TA_LEFT, spaceAfter=12, spaceBefore=12,
        textTransform="uppercase",
    ),
    "action": ParagraphStyle(
        "Action", fontName=COURIER, fontSize=12,
        leading=12, alignment=TA_LEFT, spaceAfter=6,
    ),
    "character": ParagraphStyle(
        "Character", fontName=COURIER, fontSize=12,
        leading=12, alignment=TA_LEFT, spaceBefore=12, spaceAfter=0,
        leftIndent=2.2 * inch,
    ),
    "parenthetical": ParagraphStyle(
        "Parenthetical", fontName=COURIER, fontSize=12,
        leading=12, alignment=TA_LEFT, spaceAfter=0,
        leftIndent=1.6 * inch, rightIndent=2.0 * inch,
    ),
    "dialogue": ParagraphStyle(
        "Dialogue", fontName=COURIER, fontSize=12,
        leading=12, alignment=TA_LEFT, spaceAfter=0,
        leftIndent=1.0 * inch, rightIndent=1.5 * inch,
    ),
    "transition": ParagraphStyle(
        "Transition", fontName=COURIER, fontSize=12,
        leading=12, alignment=TA_RIGHT, spaceBefore=12, spaceAfter=12,
    ),
    "camera": ParagraphStyle(
        "Camera", fontName=COURIER_BOLD, fontSize=12,
        leading=12, alignment=TA_LEFT, spaceBefore=6, spaceAfter=2,
    ),
    "title": ParagraphStyle(
        "Title", fontName=COURIER_BOLD, fontSize=14,
        leading=16, alignment=TA_CENTER, spaceAfter=4,
    ),
}

CAMERA_RE = re.compile(
    r"^(CLOSE ON|CLOSE UP|EXTREME CLOSE UP|WIDE SHOT|MEDIUM SHOT|LONG SHOT|"
    r"ANGLE ON|POV|TRACKING SHOT|PAN TO|PAN ACROSS|DOLLY|CRANE SHOT|AERIAL SHOT|"
    r"OVER THE SHOULDER|TWO SHOT|THREE SHOT|INSERT|REVERSE ANGLE|HIGH ANGLE|"
    r"LOW ANGLE|BIRD'S EYE|STEADICAM|PUSH IN|PULL BACK|RACK FOCUS|SPLIT SCREEN|"
    r"FREEZE FRAME|SLOW MOTION|BACK TO SCENE|CONTINUOUS)\b", re.IGNORECASE
)

TRANSITION_RE = re.compile(
    r"^(FADE IN:|FADE OUT\.|FADE TO BLACK\.|CUT TO:|SMASH CUT TO:|MATCH CUT TO:|"
    r"DISSOLVE TO:|JUMP CUT TO:|INTERCUT|THE END\.?)$", re.IGNORECASE
)


def _is_character_name(line):
    if len(line) > 50:
        return False
    cleaned = re.sub(r"\s*\(.*?\)\s*", "", line).strip()
    if not cleaned or len(cleaned) < 2:
        return False
    return bool(re.match(r"^[A-Z][A-Z\s\-\.']+$", cleaned))


def _escape(text):
    """Escape XML special characters for ReportLab Paragraph."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def generate_pdf(script_text, title="Untitled Scene"):
    """Convert raw screenplay text to a formatted PDF. Returns bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=LEFT_MARGIN, rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN,
    )

    story = []
    lines = script_text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        trimmed = line.strip()

        if not trimmed:
            story.append(Spacer(1, 6))
            i += 1
            continue

        # Title page lines (first few lines)
        if i < 20 and _is_title_line(trimmed, lines, i):
            story.append(Paragraph(_escape(trimmed), STYLES["title"]))
            i += 1
            continue

        # Scene headings
        if re.match(r"^(INT\.|EXT\.|INT\./EXT\.|I/E\.)", trimmed):
            story.append(Paragraph(_escape(trimmed), STYLES["scene_heading"]))
            i += 1
            continue

        # Camera directions
        if CAMERA_RE.match(trimmed) and trimmed == trimmed.upper():
            story.append(Paragraph(_escape(trimmed), STYLES["camera"]))
            i += 1
            continue

        # Transitions
        if TRANSITION_RE.match(trimmed):
            story.append(Paragraph(_escape(trimmed), STYLES["transition"]))
            i += 1
            continue

        # Character + dialogue block
        if _is_character_name(trimmed) and i + 1 < len(lines):
            next_trimmed = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if next_trimmed and (next_trimmed.startswith("(") or not next_trimmed.isupper() or len(next_trimmed) > 50):
                story.append(Paragraph(_escape(trimmed), STYLES["character"]))
                i += 1
                while i < len(lines):
                    dl = lines[i].strip()
                    if not dl:
                        break
                    if dl.startswith("(") and dl.endswith(")"):
                        story.append(Paragraph(_escape(dl), STYLES["parenthetical"]))
                    elif _is_character_name(dl) or re.match(r"^(INT\.|EXT\.)", dl) or TRANSITION_RE.match(dl):
                        break
                    else:
                        story.append(Paragraph(_escape(dl), STYLES["dialogue"]))
                    i += 1
                continue

        # Action (default)
        story.append(Paragraph(_escape(trimmed), STYLES["action"]))
        i += 1

    doc.build(story)
    buf.seek(0)
    return buf.read()


def _is_title_line(line, all_lines, index):
    lower = line.lower()
    if lower.startswith("written by") or lower.startswith("by "):
        return True
    if lower == "fade in:":
        return False
    if index == 0 and line == line.upper() and len(line) < 60:
        return True
    if 0 < index < 6 and not line.startswith("INT.") and not line.startswith("EXT."):
        prev_count = len([l for l in all_lines[:index] if l.strip()])
        if prev_count <= 2:
            return True
    return False
