"""
Seed the MedGuard database with demo data for hackathon presentations.
Run this once before the demo:  python -m backend.seed_demo
"""

from datetime import datetime, timedelta
from backend.database import init_db, get_conn
from backend.models import insert_drug


def seed():
    init_db()
    conn = get_conn()
    c = conn.cursor()

    # Clear existing data (optional for a clean demo)
    c.execute("DELETE FROM drugs")
    c.execute("DELETE FROM reports")
    conn.commit()

    today = datetime.now()

    demo_batches = [
        # Valid drug
        {
            "name": "Malaria Cure",
            "batch_number": "BATCH-VALID-001",
            "expiry_date": (today + timedelta(days=365)).strftime("%Y-%m-%d"),
            "manufacturer": "HealthPharma Ltd"
        },
        # Expired drug
        {
            "name": "Pain Relief",
            "batch_number": "BATCH-EXPIRED-002",
            "expiry_date": (today - timedelta(days=30)).strftime("%Y-%m-%d"),
            "manufacturer": "MediCare Inc"
        },
        # Another valid drug
        {
            "name": "Antibiotic X",
            "batch_number": "BATCH-VALID-003",
            "expiry_date": (today + timedelta(days=730)).strftime("%Y-%m-%d"),
            "manufacturer": "BioHealth Corp"
        }
    ]

    for drug in demo_batches:
        try:
            insert_drug(**drug)
            print(f"Inserted: {drug['batch_number']}")
        except Exception as e:
            print(f"Skipping {drug['batch_number']}: {e}")

    # Add some counterfeit reports for demo effect
    c.execute(
        "INSERT INTO reports (batch_number, location, note) VALUES (?, ?, ?)",
        ("BATCH-EXPIRED-002", "Lagos", "Expired stock found in market")
    )
    c.execute(
        "INSERT INTO reports (batch_number, location, note) VALUES (?, ?, ?)",
        ("FAKE-BATCH-999", "Abuja", "Counterfeit packaging detected")
    )
    conn.commit()
    conn.close()
    print("Demo data seeded successfully.")


if __name__ == "__main__":
    seed()
