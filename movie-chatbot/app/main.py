import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from app.config import Config
from app.routes.chat import chat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    app.register_blueprint(chat_bp, url_prefix="/api")

    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        """Serve the React build. Skip /api routes — those are handled by the blueprint."""
        if path.startswith("api/"):
            return jsonify({"error": "Not found"}), 404

        if path and os.path.isfile(os.path.join(static_dir, path)):
            return send_from_directory(static_dir, path)

        index_path = os.path.join(static_dir, "index.html")
        if os.path.isfile(index_path):
            return send_from_directory(static_dir, "index.html")

        return jsonify({
            "message": "Flask backend is running. Frontend not built yet.",
            "hint": "Run 'cd frontend && npm run build' or use 'npm run dev' on port 3000",
        })

    return app
