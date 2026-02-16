import os
import sqlite3

from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


def ensure_initialized():
    if not os.path.exists(current_app.config["DATABASE"]):
        init_db()


def init_app(app):
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("Initialized the database.")

    @app.cli.command("create-admin")
    def create_admin_command():
        db = get_db()
        exists = db.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
        if exists:
            print("Admin user already exists.")
            return

        db.execute(
            "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 1)",
            ("admin", generate_password_hash("admin123")),
        )
        db.commit()
        print("Created admin user: admin / admin123")
