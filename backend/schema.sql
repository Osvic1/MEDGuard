-- ==========================================
-- MedGuard Database Schema
-- ==========================================

PRAGMA foreign_keys = ON;

-- =========================
-- Admin Users Table
-- =========================
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_on TIMESTAMP DEFAULT (datetime('now'))
);

-- =========================
-- Drugs Table
-- =========================
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    batch_number TEXT NOT NULL UNIQUE,
    manufacturer TEXT,
    mfg_date DATE,
    exp_date DATE,
    qr_code TEXT UNIQUE,
    created_on TIMESTAMP DEFAULT (datetime('now'))
);

-- =========================
-- Reports Table
-- =========================
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_name TEXT,
    batch_number TEXT NOT NULL,
    location TEXT,
    note TEXT,
    reported_on TIMESTAMP DEFAULT (datetime('now')),
    status INTEGER DEFAULT 0  -- 0 = New, 1 = Checked
);

-- =========================
-- Indexes for Performance
-- =========================
CREATE INDEX IF NOT EXISTS idx_reports_batch ON reports(batch_number);
CREATE INDEX IF NOT EXISTS idx_drugs_batch ON drugs(batch_number);
