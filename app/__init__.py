import os

from flask import Flask

from .db import ensure_initialized, init_app


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-change-me"),
        DATABASE=os.path.join(app.instance_path, "vulnlab.sqlite"),
        UPLOAD_FOLDER=os.path.join(app.instance_path, "uploads"),
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    init_app(app)

    with app.app_context():
        ensure_initialized()

    from . import auth, main, admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)

    return app
