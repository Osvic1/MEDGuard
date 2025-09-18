from flask import Blueprint, render_template, request, redirect, url_for
from backend.database import get_db
from datetime import datetime

verify_bp = Blueprint("verify", __name__)

# Handle POST from index.html form


@verify_bp.route("/verify", methods=["POST"])
def verify_from_form():
    batch_number = (request.form.get("batch_number") or "").strip()
    verified_on_str = datetime.now().strftime(
        "%B %d, %Y at %I:%M %p") + " in Lagos, Nigeria"

    if not batch_number:
        return render_template(
            "verify.html",
            error="❌ Please enter a batch number.",
            verified_on=verified_on_str,
            status="notfound",
            batch=None
        )

    # Redirect to the GET route
    return redirect(url_for("verify.verify_batch", batch_number=batch_number))


# Handle GET /verify/<batch_number>
@verify_bp.route("/verify/<batch_number>")
def verify_batch(batch_number):
    conn = get_db()
    batch_number = batch_number.strip()

    # Try both INT and TEXT storage cases
    try:
        batch_val = int(batch_number)
    except ValueError:
        batch_val = batch_number

    row = conn.execute("""
        SELECT name AS drug_name, batch_number, mfg_date, expiry_date, manufacturer
        FROM drugs
        WHERE batch_number = ?
    """, (batch_val,)).fetchone()

    verified_on_str = datetime.now().strftime(
        "%B %d, %Y at %I:%M %p") + " in Lagos, Nigeria"

    # Case 1: Not found
    if not row:
        return render_template(
            "verify.html",
            error="❌ Batch number not found in the system.",
            verified_on=verified_on_str,
            status="notfound",
            batch=None
        )

    # Case 2: Expired
    expiry_date = None
    try:
        expiry_date = datetime.strptime(
            str(row["expiry_date"]), "%Y-%m-%d").date()
    except Exception:
        pass

    today = datetime.today().date()
    if expiry_date and expiry_date < today:
        return render_template(
            "verify.html",
            error=f"⚠️ Batch {row['batch_number']} has expired on {row['expiry_date']}.",
            verified_on=verified_on_str,
            status="expired",
            batch=row
        )

    # Case 3: Valid
    return render_template(
        "verify.html",
        batch=row,
        verified_on=verified_on_str,
        status="valid",
        error=None
    )
