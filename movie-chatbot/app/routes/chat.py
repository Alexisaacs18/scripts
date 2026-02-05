from flask import Blueprint, request, jsonify
from app.services.script_service import ScriptService
from app.services.claude_service import ClaudeService

chat_bp = Blueprint("chat", __name__)

script_service = ScriptService()
claude_service = ClaudeService()


@chat_bp.route("/generate", methods=["POST"])
def generate_script():
    """Generate a movie script based on prompt and page count."""
    data = request.get_json()

    prompt = data.get("prompt")
    page_count = data.get("page_count", 90)

    if not prompt:
        return jsonify({"error": "A prompt is required"}), 400

    if page_count not in range(30, 130, 10):
        return jsonify({"error": "Page count must be between 30-120 in increments of 10"}), 400

    reference_scripts = script_service.load_scripts()

    result = claude_service.generate(
        prompt=prompt,
        page_count=page_count,
        reference_scripts=reference_scripts,
    )

    return jsonify({"script": result})


@chat_bp.route("/scripts", methods=["GET"])
def list_scripts():
    """List all loaded reference scripts."""
    scripts = script_service.list_scripts()
    return jsonify({"scripts": scripts})
