import './ScriptRenderer.css';

/**
 * Parses raw screenplay text and renders it with proper formatting classes.
 * Detects scene headings, character names, parentheticals, dialogue,
 * transitions, and action lines based on standard screenplay conventions.
 */
export default function ScriptRenderer({ content }) {
  if (!content) return null;

  const lines = content.split('\n');
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Empty line
    if (!trimmed) {
      elements.push(<div key={i} className="script-blank" />);
      i++;
      continue;
    }

    // Title page elements (centered, at the start)
    if (i < 20 && isTitlePageLine(trimmed, lines, i)) {
      elements.push(
        <div key={i} className="script-title-line">{trimmed}</div>
      );
      i++;
      continue;
    }

    // Scene headings: INT. / EXT. / INT./EXT.
    if (/^(INT\.|EXT\.|INT\.\/EXT\.|I\/E\.)/.test(trimmed)) {
      elements.push(
        <div key={i} className="script-scene-heading">{trimmed}</div>
      );
      i++;
      continue;
    }

    // Camera directions: CLOSE ON, WIDE SHOT, ANGLE ON, etc.
    if (/^(CLOSE ON|CLOSE UP|EXTREME CLOSE UP|WIDE SHOT|MEDIUM SHOT|LONG SHOT|ANGLE ON|POV|TRACKING SHOT|PAN TO|PAN ACROSS|DOLLY|CRANE SHOT|AERIAL SHOT|OVER THE SHOULDER|TWO SHOT|THREE SHOT|INSERT|REVERSE ANGLE|HIGH ANGLE|LOW ANGLE|BIRD'S EYE|STEADICAM|PUSH IN|PULL BACK|RACK FOCUS|SPLIT SCREEN|FREEZE FRAME|SLOW MOTION|BACK TO SCENE|CONTINUOUS)\b/i.test(trimmed) && trimmed === trimmed.toUpperCase()) {
      elements.push(
        <div key={i} className="script-camera">{trimmed}</div>
      );
      i++;
      continue;
    }

    // Transitions: CUT TO:, FADE IN:, FADE OUT., DISSOLVE TO:, etc.
    if (/^(FADE IN:|FADE OUT\.|FADE TO BLACK\.|CUT TO:|SMASH CUT TO:|MATCH CUT TO:|DISSOLVE TO:|JUMP CUT TO:|INTERCUT|THE END\.?)$/i.test(trimmed)) {
      elements.push(
        <div key={i} className="script-transition">{trimmed}</div>
      );
      i++;
      continue;
    }

    // Character name: all caps line (possibly with (V.O.), (O.S.), (CONT'D))
    // followed by dialogue or parenthetical
    if (isCharacterName(trimmed) && i + 1 < lines.length) {
      const nextTrimmed = lines[i + 1]?.trim();
      if (nextTrimmed && (nextTrimmed.startsWith('(') || isDialogueLine(lines, i + 1))) {
        elements.push(
          <div key={i} className="script-character">{trimmed}</div>
        );
        i++;

        // Collect parentheticals and dialogue
        while (i < lines.length) {
          const dl = lines[i];
          const dTrimmed = dl.trim();

          if (!dTrimmed) break;

          if (dTrimmed.startsWith('(') && dTrimmed.endsWith(')')) {
            elements.push(
              <div key={i} className="script-parenthetical">{dTrimmed}</div>
            );
          } else if (isCharacterName(dTrimmed) || /^(INT\.|EXT\.)/.test(dTrimmed) || /^(CUT TO:|FADE)/.test(dTrimmed)) {
            break;
          } else {
            elements.push(
              <div key={i} className="script-dialogue">{dTrimmed}</div>
            );
          }
          i++;
        }
        continue;
      }
    }

    // Action / description (default)
    elements.push(
      <div key={i} className="script-action">{trimmed}</div>
    );
    i++;
  }

  return <div className="script-page">{elements}</div>;
}

function isTitlePageLine(line, allLines, index) {
  const lower = line.toLowerCase();
  if (lower.startsWith('written by') || lower.startsWith('by ')) return true;
  if (lower === 'fade in:') return false;
  // If the first non-empty line or preceded by empty lines, and is all caps or short
  if (index === 0 && line === line.toUpperCase() && line.length < 60) return true;
  if (index > 0 && index < 6 && !line.startsWith('INT.') && !line.startsWith('EXT.')) {
    const prev = allLines.slice(0, index).filter((l) => l.trim()).length;
    if (prev <= 2) return true;
  }
  return false;
}

function isCharacterName(line) {
  if (line.length > 50) return false;
  // Remove extensions like (V.O.), (O.S.), (CONT'D)
  const cleaned = line.replace(/\s*\(.*?\)\s*/g, '').trim();
  if (!cleaned) return false;
  // Must be all uppercase letters, spaces, hyphens, periods, apostrophes
  return /^[A-Z][A-Z\s\-\.']+$/.test(cleaned) && cleaned.length >= 2;
}

function isDialogueLine(lines, index) {
  const line = lines[index]?.trim();
  if (!line) return false;
  // Dialogue is mixed case, not a scene heading, not a transition
  if (/^(INT\.|EXT\.)/.test(line)) return false;
  if (/^(CUT TO:|FADE)/.test(line)) return false;
  return line !== line.toUpperCase() || line.length > 50;
}
