from flask import Blueprint, abort, g, render_template

from .auth import login_required
from .db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@login_required
def panel():
    if not g.user["is_admin"]:
        abort(403)

    db = get_db()
    users = db.execute(
        "SELECT id, username, is_admin, created_at FROM users ORDER BY created_at DESC"
    ).fetchall()
    notes_count = db.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
    return render_template("admin.html", users=users, notes_count=notes_count)
