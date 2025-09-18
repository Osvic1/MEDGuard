from flask import Blueprint, jsonify, request
from backend.database import get_db
from datetime import datetime

report_bp = Blueprint("report_api", __name__)

# =========================
# POST: Save a new counterfeit report
# =========================


@report_bp.post("/report")
def create_report():
    data = request.get_json()
    drug_name = data.get("drug_name")
    batch_number = data.get("batch_number")
    location = data.get("location")
    note = data.get("note")

    if not batch_number:
        return jsonify({"message": "❌ Batch number is required"}), 400

    conn = get_db()
    conn.execute(
        """
        INSERT INTO reports (drug_name, batch_number, location, note, reported_on, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (drug_name, batch_number, location, note, datetime.now(), 0)  # 0 = New
    )
    conn.commit()

    return jsonify({"message": "🚨 Report received. Thank you for helping keep patients safe."}), 201


# =========================
# GET: Fetch counterfeit reports (supports search & date filters)
# =========================
@report_bp.get("/report")
def get_reports():
    conn = get_db()
    search = request.args.get("search", "").strip()
    start = request.args.get("start", "").strip()
    end = request.args.get("end", "").strip()

    query = """
        SELECT id, drug_name, batch_number, location, note, reported_on, status
        FROM reports
        WHERE 1=1
    """
    params = []

    # Optional search filter
    if search:
        query += " AND (drug_name LIKE ? OR batch_number LIKE ? OR location LIKE ? OR note LIKE ?)"
        params.extend([f"%{search}%"] * 4)

    # Optional date range filter
    if start and end:
        query += " AND date(reported_on) BETWEEN date(?) AND date(?)"
        params.extend([start, end])

    query += " ORDER BY reported_on DESC"

    rows = conn.execute(query, params).fetchall()

    # Convert rows to dicts
    reports = []
    for row in rows:
        r = dict(row)
        r["status_label"] = "New" if r["status"] == 0 else "Checked"
        reports.append(r)

    return jsonify(reports)


# =========================
# POST: Mark a report as Checked
# =========================
@report_bp.post("/report/<int:report_id>/mark_checked")
def mark_report_checked(report_id):
    try:
        conn = get_db()
        conn.execute(
            "UPDATE reports SET status = 1 WHERE id = ?", (report_id,))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        print("Error updating report status:", e)
        return jsonify({"error": "Failed to update status"}), 500


# =========================
# GET: Count of New reports (for notification badge)
# =========================
@report_bp.get("/report/count")
def count_new_reports():
    conn = get_db()
    row = conn.execute(
        "SELECT COUNT(*) as count FROM reports WHERE status = 0").fetchone()
    return jsonify({"count": row["count"] if row else 0})
