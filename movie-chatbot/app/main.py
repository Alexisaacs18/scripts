from flask import Flask, send_from_directory
from flask_cors import CORS
from app.config import Config
from app.routes.chat import chat_bp


def create_app():
    app = Flask(
        __name__,
        static_folder="../static",
        static_url_path="",
    )
    app.config.from_object(Config)

    CORS(app)

    app.register_blueprint(chat_bp, url_prefix="/api")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        """Serve the React build. Falls back to index.html for client-side routing."""
        try:
            return send_from_directory(app.static_folder, path)
        except Exception:
            return send_from_directory(app.static_folder, "index.html")

    return app
