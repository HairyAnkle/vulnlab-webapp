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

    @app.cli.command("seed-lab")
    def seed_lab_command():
        db = get_db()

        demo_user = db.execute("SELECT id FROM users WHERE username = ?", ("demo",)).fetchone()
        if demo_user is None:
            db.execute(
                "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, 0)",
                ("demo", generate_password_hash("demo123")),
            )
            db.commit()
            demo_user = db.execute("SELECT id FROM users WHERE username = ?", ("demo",)).fetchone()

        note_count = db.execute("SELECT COUNT(*) AS c FROM notes WHERE author_id = ?", (demo_user["id"],)).fetchone()["c"]
        if note_count == 0:
            db.execute(
                "INSERT INTO notes (title, content, author_id) VALUES (?, ?, ?)",
                ("Welcome note", "This is baseline sample data for the lab.", demo_user["id"]),
            )
            db.execute(
                "INSERT INTO notes (title, content, author_id) VALUES (?, ?, ?)",
                ("Second note", "Use this account to test workflow and security scenarios.", demo_user["id"]),
            )
            db.commit()

        print("Seeded lab data: demo / demo123 with sample notes.")
