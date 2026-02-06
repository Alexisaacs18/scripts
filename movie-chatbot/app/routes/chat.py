import os
import urllib.request
import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.script_service import ScriptService
from app.services.llm_service import LLMService
from app.config import Config

chat_bp = Blueprint("chat", __name__)

script_service = ScriptService()
llm_service = LLMService()


@chat_bp.route("/generate", methods=["POST"])
def generate_script():
    """Generate or revise a scene based on conversation history."""
    data = request.get_json()

    messages = data.get("messages")
    page_count = data.get("page_count", 2)

    if not messages or not isinstance(messages, list):
        return jsonify({"error": "A messages array is required"}), 400

    if page_count not in range(1, 6):
        return jsonify({"error": "Page count must be between 1 and 5"}), 400

    # Validate message format
    for msg in messages:
        if msg.get("role") not in ("user", "assistant"):
            return jsonify({"error": "Each message must have role 'user' or 'assistant'"}), 400
        if not msg.get("content"):
            return jsonify({"error": "Each message must have non-empty content"}), 400

    reference_scripts = script_service.load_scripts()

    try:
        result = llm_service.generate(
            messages=messages,
            page_count=page_count,
            reference_scripts=reference_scripts,
        )
    except Exception as e:
        return jsonify({"error": f"LM Studio error: {str(e)}"}), 502

    return jsonify({"script": result})


@chat_bp.route("/health", methods=["GET"])
def health_check():
    """Check if LM Studio is reachable using a direct HTTP call."""
    base_url = Config.LM_STUDIO_BASE_URL.rstrip("/")
    models_url = f"{base_url}/models"
    try:
        req = urllib.request.Request(models_url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            model_ids = [m.get("id", "unknown") for m in data.get("data", [])]
            return jsonify({
                "status": "connected",
                "url": base_url,
                "models": model_ids,
            })
    except urllib.error.URLError as e:
        return jsonify({
            "status": "disconnected",
            "url": base_url,
            "error": f"Cannot reach LM Studio at {base_url}: {str(e.reason)}",
        }), 503
    except Exception as e:
        return jsonify({
            "status": "disconnected",
            "url": base_url,
            "error": str(e),
        }), 503


@chat_bp.route("/scripts", methods=["GET"])
def list_scripts():
    """List all loaded reference scripts."""
    scripts = script_service.list_scripts()
    return jsonify({"scripts": scripts})


@chat_bp.route("/scripts/upload", methods=["POST"])
def upload_script():
    """Upload a reference script file."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    allowed = (".txt", ".fountain", ".fdx", ".pdf")
    if not filename.lower().endswith(allowed):
        return jsonify({"error": f"Unsupported file type. Use: {', '.join(allowed)}"}), 400

    os.makedirs(Config.SCRIPTS_DIR, exist_ok=True)
    file.save(os.path.join(Config.SCRIPTS_DIR, filename))
    return jsonify({"message": "Uploaded", "filename": filename})


@chat_bp.route("/scripts/<filename>", methods=["DELETE"])
def delete_script(filename):
    """Delete a reference script."""
    filename = secure_filename(filename)
    filepath = os.path.join(Config.SCRIPTS_DIR, filename)
    if not os.path.isfile(filepath):
        return jsonify({"error": "Script not found"}), 404

    os.remove(filepath)
    return jsonify({"message": "Deleted", "filename": filename})
