# Medication Reconciliation & Conflict Reporting Service

## Overview

This service ingests medication lists for patients from multiple sources (clinic EMR, hospital discharge, patient-reported), maintains a longitudinal history of these lists, detects conflicts between sources, and provides reporting capabilities.

The goal is to surface unresolved medication conflicts clearly while preserving full historical context.

---

## Setup Instructions

```bash
git clone https://github.com/jogit25/medication-reconciliation-service.git

cd medication-reconciliation-service

uv venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

uv add fastapi uvicorn motor python-dotenv

uv run uvicorn app.main:app --reload

#seed data(optional)
uv run python app/seed.py
```

Open:
http://127.0.0.1:8000/docs

---

## Architecture Overview

### Flow

Client → FastAPI → Normalization → Conflict Detection → MongoDB

---

### Collections

#### `medication_snapshots`

* Each document represents a **medication list from a specific source at a specific time**
* Every ingestion creates a new version of the medication list (longitudinal history)
* Older versions are always preserved

**Versioning logic:**

* A new snapshot is created for each incoming medication list
* Exception:

  * If the same source updates a list within a very short time window (e.g., correcting a missed medication), the existing latest snapshot can be updated instead of creating a new version
* This avoids unnecessary duplicate versions while still preserving meaningful history

---

#### `conflicts`

* Conflicts are stored separately from snapshots
* Each conflict document contains:

  * patient_id
  * conflict type (dose mismatch, active vs stopped)
  * medications involved
  * source(s)
  * status (unresolved / resolved)
  * timestamps for creation and resolution

**Flow:**

* After storing a medication snapshot, the system compares it with the latest snapshot for that patient
* Any detected conflicts are stored as separate documents
* These conflicts are then tracked independently and can be resolved later

---

## Features

* Ingest medication lists per patient and source
* Normalize medication data:

  * lowercase names
  * trim spaces
  * remove duplicates
* Detect conflicts:

  * same drug, different dose
  * active vs stopped
* Store conflicts with full audit trail
* Resolve conflicts with reason, user, and timestamp
* Aggregation endpoints:

  * patients with ≥1 unresolved conflict per source
  * patients with ≥2 conflicts in last 30 days

---

## Assumptions & Trade-offs

### Assumptions

* The `source` field (`clinic_emr`, `hospital_discharge`, `patient_reported`) is treated as the clinic/system since no explicit clinic entity was provided
* Conflict detection compares the incoming snapshot with the **most recent snapshot only**
* Timestamps and patient identifiers are assigned by the backend

---

### Trade-offs

* **Denormalized snapshots (MongoDB):**
  Medication lists are stored as embedded documents for simpler reads and queries

* **Separate conflict collection:**
  Conflicts are stored independently to support:

  * auditability
  * resolution tracking
  * efficient reporting

* **Event-based conflict detection:**
  Only comparing with the latest snapshot keeps logic simple and avoids duplicate conflicts, but does not re-evaluate full history

* **No external drug database:**
  Conflict detection is based on simple rules (dose mismatch, status mismatch). This can be extended with a rules JSON or drug interaction database

---

## Known Limitations

* No drug class interaction rules (can be added via static JSON)
* No authentication/authorization
* No pagination for reporting endpoints
* Limited validation on medication fields beyond basic checks

---

## Future Improvements

* Add static JSON-based drug interaction rules
* Introduce clinic entity instead of relying on `source`
* Add background processing for large-scale ingestion
* Add authentication and role-based access
* Improve conflict resolution workflow (e.g., prioritization, notes)


---

## Use of AI

### What AI was used for

* Clarifying FastAPI + MongoDB (Motor) integration
* Debugging issues (ObjectId handling, dependency conflicts)
* Verifying aggregation pipeline structure
* General guidance on structuring the implementation

---

### What was reviewed and changed manually

* API design decisions (especially path vs body usage)
* Data modeling (snapshots vs conflicts separation)
* Conflict detection logic and flow
* Aggregation endpoints and behavior

---

### Example of disagreement

A suggestion was made to include `patient_id` in the request body.
This was rejected in favor of passing it via the URL path, to avoid duplication and maintain consistency with REST design principles.

---
