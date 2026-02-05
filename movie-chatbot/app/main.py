from flask import Flask, render_template
from app.config import Config
from app.routes.chat import chat_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(Config)

    app.register_blueprint(chat_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
