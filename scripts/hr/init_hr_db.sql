-- init_hr_db.sql
-- Schema for HR Applicant Intake Demo

CREATE TABLE IF NOT EXISTS hr_applicants (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(255),
    iso_country VARCHAR(3),
    role VARCHAR(100),
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS hr_applicants_quarantine (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(255),
    iso_country VARCHAR(3),
    role VARCHAR(100),
    failure_reason TEXT,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
