# AegisGate — Offline-First AI Security Gateway

AegisGate is an offline-first, privacy-preserving AI Security Gateway designed to operate entirely locally on standard consumer hardware without external cloud dependencies, API keys, or GPU hardware.

> [!NOTE]
> **Stage 4 (AegisGate Verify: Unified Hash-Based Identity & Integrity Verification) Overview:**
> Stage 4 introduces **AegisGate Verify**, a unified verification subsystem supporting:
> - **Streaming SHA-256 File Hashing:** High-throughput, bounded-memory chunked hashing (default 64 KiB) for files, documents, models, and binaries up to 50 MiB with concurrent modification detection.
> - **Trusted-Reference Registry:** SQLite-backed registry of authorized SHA-256 references with explicit confirmation for registration, update, and revocation.
> - **Digital Signatures & Signer Trust (Ed25519):** Cryptographic signature verification using standard Ed25519 public keys, key fingerprinting (SHA-256), and local trust policy evaluation. Private keys are never collected or stored.
> - **Signed Software & AI Model Manifests:** Deterministic canonical serialization, detached signature verification, and file-tree integrity checks (detecting verified, modified, missing, and unexpected files) with path-traversal prevention.
> - **Media Integrity & Provenance Adapter:** Safe header parsing for JPEG, PNG, GIF, WAV, and MP4 files, detecting C2PA JUMBF provenance metadata containers as an extension point.
> - **Exportable JSON Verification Reports:** Standardized reports with full audit traceability and cryptographic health validation.
> - **Complete Audit Integration:** Every reference change, key import, revocation, and verification operation is atomically appended to the tamper-evident SHA-256 audit chain.
>
> > [!TIP]
> > **Stage 5 (Security Validation, Adversarial Testing & Release Readiness):**
> > Comprehensive security hardening and adversarial test suites were added in Stage 5, bringing total test coverage to **113 passing automated tests**. Detailed findings, remediations, and disaster recovery procedures are documented in [`docs/SECURITY_REVIEW.md`](docs/SECURITY_REVIEW.md).

---

## 1. System Requirements

- **Operating System:** Windows 10/11 (or Linux/macOS)
- **RAM:** Minimum 4 GB (tested on 12 GB RAM)
- **Disk:** Standard HDD or SSD storage
- **Python:** Python 3.12 (standard CPython)
- **Hardware:** No GPU or external cloud account required

---

## 2. Windows PowerShell Setup Guide

Follow these exact steps in PowerShell from the project root directory (`g:\startup\AEGIS GATE`):

### Step 1: Check Python Version
Ensure Python 3.12 is installed:
```powershell
python --version
```

### Step 2: Create a Virtual Environment
Create a clean virtual environment named `.venv`:
```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
Activate the environment in your PowerShell session:
```powershell
.\.venv\Scripts\Activate.ps1
```
> **Troubleshooting Execution Policy:**
> If PowerShell shows an error stating *`running scripts is disabled on this system`*, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```
> Then re-run `.\.venv\Scripts\Activate.ps1`.

### Step 4: Install Dependencies
Upgrade pip and install the lightweight requirements:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. First-Run Account Initialization & CLI Administration

AegisGate enforces an explicit, documented first-run account setup. There are **no hardcoded default passwords**.

### Option A: Initialize Administrator via CLI (Recommended)
You can initialize the first administrator directly from PowerShell:
```powershell
python -m app.cli init-admin --username admin --password "YourStrongPassword123!"
```
*(If you omit `--password`, you will be prompted securely without displaying the password).*

### Option B: Initialize Administrator via Dashboard
1. Start the application:
   ```powershell
   python app/main.py
   ```
2. Navigate to `http://127.0.0.1:8000/`.
3. If no user exists, the dashboard automatically presents the **First-Run Account Setup** form.
4. Once created, setup is permanently locked (further setup requests return `409 Conflict`).

### Account Recovery / Password Reset
If the administrator password is forgotten, an authorized local administrator can reset it via the CLI:
```powershell
python -m app.cli reset-password --username admin --new-password "NewSecurePassword456!" --confirm
```

### Audit Chain Verification CLI
To verify the integrity of the audit log directly from the terminal:
```powershell
python -m app.cli verify-audit
```

### Online Backup & Recovery CLI
AegisGate supports safe live SQLite backups in WAL mode without locking or partial copies:
```powershell
# Create a verified online backup
python -m app.cli backup-db

# Verify an existing backup file
python -m app.cli verify-backup --backup-path "data/backups/aegisgate_backup_*.db"

# Restore database from backup (with automatic pre-restore safety copy)
python -m app.cli restore-db --backup-path "data/backups/aegisgate_backup_*.db"

# Local system diagnostics
python -m app.cli diagnostics
```

---

## 4. Running the Test Suite

Run the full pytest suite (129 automated tests across 22 test modules) covering streaming hashing, trusted references, Ed25519 signatures, manifests, media adapters, API hardening, authentication, normalization, rule matching, policy evaluation, audit chain integrity, adversarial attack vectors, automated backup/recovery, and executable packaging smoke tests:
```powershell
pytest -v
```

Expected output:
```
================= 129 passed in ~125s =================
```

---

## 5. Windows Standalone Executable Release Candidate

AegisGate provides an automated build script generating a single-file Windows binary:
```powershell
.\.venv\Scripts\python.exe scripts/build_windows_exe.py
```
Output executable: `dist/release_candidate/aegisgate.exe` (~18.7 MB).
See [`docs/WINDOWS_RELEASE_GUIDE.md`](docs/WINDOWS_RELEASE_GUIDE.md) for full deployment runbooks and standalone testing instructions.

---

## 5. Starting the Application & Dashboard

Start AegisGate on the local loopback interface (`127.0.0.1`):
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Or directly run:
```powershell
python app/main.py
```

### Accessing the Local Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

The dashboard is completely offline (HTML/CSS/vanilla JavaScript with zero external CDN dependencies) and features:
- **Authentication Panel:** First-run setup, secure login, active session status display, and single-click logout.
- **Security Analysis Inspection:** Text analysis, live rule matching, prompt injection detection, and policy decisions (`ALLOW`, `FLAG`, `BLOCK`, `REVIEW`).
- **AegisGate Verify:**
  - *File & Media Integrity Tab:* File dropzone, streaming SHA-256 calculation, category selection, reference matching, and provenance detection.
  - *Trusted References Registry Tab:* Reference listing, quick registration, and revocation.
  - *Digital Signatures & Keys Tab:* Ed25519 public key import, key fingerprint inspection, and detached signature verification.
  - *Verification History Tab:* Real-time record audit log with one-click JSON report downloads.
- **Audit Hash Chain Verifier:** Live cryptographic check of the entire event sequence.

---

## 6. AegisGate Verify Architecture

```
                       [ Incoming File / Media / Data ]
                                      │
                                      ▼
                        [ Streaming SHA-256 Engine ]
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
 [ Reference Registry ]      [ Ed25519 Signatures ]        [ Manifest Engine ]
        │                             │                             │
   Compare hash vs              Verify signature            Canonical serialization
   trusted references           against trusted key         & file-tree verification
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                       [ Media & Provenance Adapter ]
                         (JPEG, PNG, WAV, MP4, C2PA)
                                      │
                                      ▼
                      [ Common Verification Result ]
               (VERIFIED_MATCH, MISMATCH, SIGNER_TRUSTED, etc.)
                                      │
                                      ▼
                    [ Tamper-Evident SHA-256 Audit Chain ]
                                      │
                                      ▼
                     [ Exportable JSON Report / Web UI ]
```

### Critical Security Distinctions
- **Byte-Level Integrity vs. Maliciousness:** A matching hash proves that a file is identical to a trusted reference byte-for-byte; it does **not** prove the file is bug-free or harmless. Conversely, a mismatch indicates alteration or divergence, not necessarily malware.
- **Digital Signatures vs. Signer Trust:** A valid Ed25519 signature mathematically verifies that the payload was signed by the private key corresponding to the public key. It does **not** prove who owns the key. Trust is an explicit local policy decision managed in the key registry.
- **Media Hashes vs. Real-World Authenticity:** A cryptographic hash of a photo or audio file proves the file has not been modified since that hash was recorded. It does **not** prove that a photograph depicts a real event or that an audio recording belongs to a particular person. AegisGate explicitly refrains from biometric face recognition or voice identification.
- **Provenance Data:** Absence of C2PA provenance metadata does not mean a media file is synthetic or forged; presence of metadata requires cryptographic validation against an external trust root.

---

## 7. AegisGate Verify API Endpoints

All endpoints require authentication (session cookie or `Authorization: Bearer <token>`). State-changing requests (`POST`, `PUT`) using ambient cookies enforce `X-CSRF-Token` validation.

### A. Verify Uploaded File
```powershell
# Authenticate
$loginBody = @{ username = "admin"; password = "YourStrongPassword123!" } | ConvertTo-Json
$session = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/auth/login" `
  -Method Post -ContentType "application/json" -Body $loginBody -SessionVariable aegisSession
$csrfToken = ($session.Cookies.GetCookies("http://127.0.0.1:8000") | Where-Object { $_.Name -eq "aegisgate_csrf" }).Value

# Upload file for integrity verification
$form = @{
    category = "file"
    file = Get-Item "C:\path\to\target_file.bin"
}
$headers = @{ "X-CSRF-Token" = $csrfToken }
$verifyResult = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/verify/file" `
  -Method Post -Form $form -Headers $headers -WebSession $aegisSession
$verifyResult | ConvertTo-Json -Depth 5
```

### B. Register Trusted Reference
```powershell
$refBody = @{
    label = "Production Model Weights v1.0.0"
    category = "model"
    digest = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    source_description = "Vendor release portal checksum"
} | ConvertTo-Json

$ref = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/verify/references" `
  -Method Post -ContentType "application/json" -Headers $headers -Body $refBody -WebSession $aegisSession
```

### C. Import Trusted Public Key
```powershell
$keyBody = @{
    signer_name = "Model Vendor Authority"
    public_key_hex = "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    algorithm = "ed25519"
} | ConvertTo-Json

$key = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/verify/keys" `
  -Method Post -ContentType "application/json" -Headers $headers -Body $keyBody -WebSession $aegisSession
```

### D. Export Verification Report
```powershell
$report = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/verify/records/$($verifyResult.verification_id)/report" `
  -WebSession $aegisSession
$report | ConvertTo-Json -Depth 5
```

---

## 8. Database Schema & Backups

The SQLite database (`data/aegisgate.db`) manages tables with automatic schema migration:
- `users`: User credentials and Argon2id password hashes.
- `sessions`: Cryptographic session tokens and CSRF secrets.
- `login_attempts`: Rate limiting and brute-force backoff tracking.
- `audit_events`: Tamper-evident SHA-256 hash chain of all system events.
- `analysis_records`: Text policy assessment summaries (raw prompt text is **never** stored).
- `trusted_references`: Authorized SHA-256 references, categories, and lifecycle status.
- `trusted_keys`: Ed25519 public keys, calculated fingerprints, and signer trust status.
- `verification_records`: Complete history of hash, signature, media, and manifest operations.

### Database Backup Command
```powershell
Copy-Item "data/aegisgate.db" "data/aegisgate_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

---

## 9. Known Limitations & Future Development

- **Local Trust Root:** AegisGate runs as an offline gateway without connecting to external Certificate Authorities (CAs) or cloud PKI. Trust roots must be explicitly configured by a local administrator.
- **C2PA Provenance:** The media adapter detects C2PA/JUMBF container structures in file headers; full cryptographic credential validation against X.509 certificate chains is designed as an extension point for future stages.
- **Local File Modification vs. Hardware WORM:** The SHA-256 audit chain detects database modifications and deletions. However, an attacker with physical or root operating system control can overwrite the database file and recompute hashes. Immutable external write-once storage (WORM) is required for hardware-grade non-repudiation.
- **Single-Turn Scope:** Input text analysis evaluates single submissions; multi-turn semantic smuggling across multiple conversational turns is planned for future conversational session state tracking.
