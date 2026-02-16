import os
from uuid import uuid4

from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

from .auth import login_required
from .db import get_db

bp = Blueprint("main", __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
def index():
    if g.user:
        return redirect(url_for("main.dashboard"))
    return redirect(url_for("auth.login"))


@bp.route("/dashboard")
@login_required
def dashboard():
    notes = get_db().execute(
        "SELECT id, title, created_at FROM notes WHERE author_id = ? ORDER BY created_at DESC",
        (g.user["id"],),
    ).fetchall()
    return render_template("dashboard.html", notes=notes)


@bp.route("/profile", methods=("GET", "POST"))
@login_required
def profile():
    db = get_db()
    if request.method == "POST":
        bio = request.form.get("bio", "").strip()
        avatar = request.files.get("avatar")
        avatar_path = g.user["avatar_path"]

        if avatar and avatar.filename:
            if not allowed_file(avatar.filename):
                flash("Invalid file type. Allowed: png, jpg, jpeg, gif", "error")
                return redirect(url_for("main.profile"))

            filename = secure_filename(avatar.filename)
            extension = filename.rsplit(".", 1)[1].lower()
            final_name = f"{g.user['id']}_{uuid4().hex}.{extension}"
            disk_path = os.path.join(current_app.config["UPLOAD_FOLDER"], final_name)
            avatar.save(disk_path)
            avatar_path = final_name

        db.execute("UPDATE users SET bio = ?, avatar_path = ? WHERE id = ?", (bio, avatar_path, g.user["id"]))
        db.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("main.profile"))

    user = db.execute("SELECT * FROM users WHERE id = ?", (g.user["id"],)).fetchone()
    return render_template("profile.html", user=user)


@bp.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@bp.route("/notes/new", methods=("GET", "POST"))
@login_required
def create_note():
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        if not title:
            flash("Title is required.", "error")
            return render_template("note_form.html", action="Create", note=None)

        db = get_db()
        db.execute(
            "INSERT INTO notes (title, content, author_id) VALUES (?, ?, ?)",
            (title, content, g.user["id"]),
        )
        db.commit()
        return redirect(url_for("main.dashboard"))

    return render_template("note_form.html", action="Create", note=None)


def get_note_or_404(note_id):
    note = get_db().execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if note is None:
        abort(404)
    if note["author_id"] != g.user["id"] and not g.user["is_admin"]:
        abort(403)
    return note


@bp.route("/notes/<int:note_id>")
@login_required
def view_note(note_id):
    note = get_note_or_404(note_id)
    return render_template("note_view.html", note=note)


@bp.route("/notes/<int:note_id>/edit", methods=("GET", "POST"))
@login_required
def edit_note(note_id):
    note = get_note_or_404(note_id)
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()
        if not title:
            flash("Title is required.", "error")
            return render_template("note_form.html", action="Edit", note=note)

        db = get_db()
        db.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
        db.commit()
        return redirect(url_for("main.view_note", note_id=note_id))

    return render_template("note_form.html", action="Edit", note=note)


@bp.route("/notes/<int:note_id>/delete", methods=("POST",))
@login_required
def delete_note(note_id):
    get_note_or_404(note_id)
    db = get_db()
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    return redirect(url_for("main.dashboard"))
