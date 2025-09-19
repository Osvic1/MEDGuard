---
# 🛡️ MedGuard – Counterfeit Drug Reporting & Verification System

MedGuard is a web-based platform designed to **detect, report, and manage counterfeit drugs**. It empowers users to scan drug packaging, verify authenticity, and submit reports of suspected counterfeit products. Administrators can review reports, mark them as checked, and monitor trends to protect public health.
---

## ✨ Features

- **QR Code Scanning** – Verify drug authenticity instantly.
- **Counterfeit Reporting** – Users can submit reports with drug name, batch number, location, and notes.
- **Admin Dashboard** – View all reports, filter by date, and mark reports as checked.
- **Real-Time Notifications** – Badge counter and blinking alerts for new reports.
- **Status Tracking** – Reports are flagged as `New` (amber) or `Checked` (green).
- **Session Management** – Automatic session timeout with warning modal.
- **Responsive UI** – Clean, modern design with medical-grade color palette.

---

## 🏗️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Styling**: Custom CSS with medical-themed palette
- **QR Scanning**: Integrated QR reader panel

---

## 📂 Project Structure

```
medguard/
│
├── backend/
│   ├── database.py        # SQLite connection helper
│   ├── report.py          # API routes for reports
│   └── admin.py           # Admin dashboard routes
│
├── static/
│   ├── style.css          # Global styles (color palette, UI components)
│   ├── admin.js           # Admin dashboard logic
│   └── admin_timer.js     # Session timeout handling
│
├── templates/
│   ├── base.html          # Shared layout
│   ├── admin.html         # Admin dashboard
│   └── index.html         # User-facing scanning/reporting
│
├── medguard.db            # SQLite database
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/MEDGuard.git
   cd medguard
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Initialize the database**

   ```bash
   sqlite3 medguard.db < schema.sql
   ```

4. **Run the Flask app**

   ```bash
   flask run
   ```

5. **Access the app**
   - User interface: `http://localhost:5000/`
   - Admin dashboard: `http://localhost:5000/admin`

---

## 🗄️ Database Schema

**Table: `reports`**

| Column       | Type      | Description                  |
| ------------ | --------- | ---------------------------- |
| id           | INTEGER   | Primary key                  |
| drug_name    | TEXT      | Name of the drug             |
| batch_number | TEXT      | Batch number (required)      |
| location     | TEXT      | Location of report           |
| note         | TEXT      | Additional notes             |
| reported_on  | TIMESTAMP | Auto-set to current datetime |
| status       | INTEGER   | `0 = New`, `1 = Checked`     |

---

## 🎨 UI & Design

- **Primary Accents**: Soft Teal `#00B8A9`, Muted Cyan `#4ECDC4`, Medical Green `#1ABC9C`
- **Warnings**: Warm Amber `#F39C12`, Coral Orange `#E67E22`
- **Buttons**: Dark Teal `#008080`, Navy Blue `#2C3E50`, Soft Emerald `#2ECC71`
- **Backgrounds**: Light Grey-Blue `#ECF0F1`, Pale Aqua `#E8F8F5`

Badges:

- 🟠 **New** → Amber (`badge-new`)
- 🟢 **Checked** → Emerald (`badge-checked`)

---

## 🚀 Future Enhancements

- Role-based authentication (Admin vs User).
- Analytics dashboard for counterfeit trends.
- Email/SMS alerts for new reports.
- Multi-language support.
- Cloud database integration (PostgreSQL/MySQL).

---

## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request with detailed notes.

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## 🧑‍💻 Author

Developed by **Timothy Victor** with support from Myself and Myself  
Designed to protect communities from counterfeit drugs and safeguard public health.

---
