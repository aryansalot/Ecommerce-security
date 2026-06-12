# SOC Platform - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser (User)                        │
│                    http://localhost:3000                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   React Frontend (Port 3000)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React Router                                        │   │
│  │  - Dashboard                                         │   │
│  │  - Vulnerabilities                                   │   │
│  │  - Incidents                                         │   │
│  │  - Threats                                           │   │
│  │  - Alerts                                            │   │
│  │  - Compliance                                        │   │
│  │  - MITRE ATT&CK                                      │   │
│  │  - Assets                                            │   │
│  │  - Risk Analysis                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Zustand State Management                            │   │
│  │  - Authentication State                              │   │
│  │  - Dashboard Data Cache                              │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Axios API Client                                    │   │
│  │  - JWT Token Interceptor                             │   │
│  │  - Error Handling                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              │ JWT Authentication
                              │ CORS Enabled
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Flask Backend (Port 5000)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Authentication Layer                                │   │
│  │  - JWT Token Generation                              │   │
│  │  - Password Hashing                                  │   │
│  │  - Role-Based Access Control                         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Routes (Blueprints)                             │   │
│  │  - Auth Routes                                       │   │
│  │  - Dashboard Routes                                  │   │
│  │  - Vulnerability Routes                              │   │
│  │  - Incident Routes                                   │   │
│  │  - Threat Routes                                     │   │
│  │  - Alert Routes                                      │   │
│  │  - Compliance Routes                                 │   │
│  │  - MITRE Routes                                      │   │
│  │  - Asset Routes                                      │   │
│  │  - Risk Routes                                       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Business Logic Services                             │   │
│  │  - Risk Scoring Engine                               │   │
│  │  - Compliance Calculator                             │   │
│  │  - Audit Logging                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Data Models (SQLAlchemy ORM)                        │   │
│  │  - User                                              │   │
│  │  - Vulnerability                                     │   │
│  │  - Incident                                          │   │
│  │  - Threat                                            │   │
│  │  - Alert                                             │   │
│  │  - Compliance                                        │   │
│  │  - MITRE                                             │   │
│  │  - Asset                                             │   │
│  │  - AuditLog                                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  SQLite Database                             │
│                 (soc_platform.db)                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tables:                                             │   │
│  │  - users                                             │   │
│  │  - vulnerabilities                                   │   │
│  │  - incidents                                         │   │
│  │  - threats                                           │   │
│  │  - alerts                                            │   │
│  │  - compliance_status                                 │   │
│  │  - mitre_attacks                                     │   │
│  │  - assets                                            │   │
│  │  - audit_logs                                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

### Frontend

```
App
├── Router
│   ├── Login
│   ├── ProtectedRoute
│   │   ├── TopNavbar
│   │   │   └── User Profile / Logout
│   │   ├── Sidebar
│   │   │   ├── Dashboard Link
│   │   │   ├── Vulnerabilities Link
│   │   │   ├── Incidents Link
│   │   │   ├── Threats Link
│   │   │   ├── Alerts Link
│   │   │   ├── Compliance Link
│   │   │   ├── MITRE ATT&CK Link
│   │   │   ├── Assets Link
│   │   │   └── Risk Analysis Link
│   │   └── Main Content Area
│   │       ├── Dashboard
│   │       │   ├── KPI Cards
│   │       │   ├── Risk Meter
│   │       │   └── Data Tables
│   │       ├── Vulnerabilities
│   │       │   ├── Filter Controls
│   │       │   └── Vulnerability Table
│   │       ├── Incidents
│   │       ├── Threats
│   │       ├── Alerts
│   │       ├── Compliance
│   │       ├── MITRE
│   │       ├── Assets
│   │       └── RiskAnalysis
```

### Backend

```
Flask App
├── Blueprints (API Routes)
│   ├── Auth Routes (/api/auth)
│   ├── Dashboard Routes (/api/dashboard)
│   ├── Vulnerability Routes (/api/vulnerabilities)
│   ├── Incident Routes (/api/incidents)
│   ├── Threat Routes (/api/threats)
│   ├── Alert Routes (/api/alerts)
│   ├── Compliance Routes (/api/compliance)
│   ├── MITRE Routes (/api/mitre)
│   ├── Asset Routes (/api/assets)
│   └── Risk Routes (/api/risk)
├── Models (SQLAlchemy)
│   ├── User
│   ├── Vulnerability
│   ├── Incident
│   ├── Threat
│   ├── Alert
│   ├── ComplianceStatus
│   ├── MitreAttack
│   ├── Asset
│   └── AuditLog
├── Services
│   ├── RiskScoringEngine
│   └── ComplianceCalculator
└── Utils
    ├── Authentication & Authorization
    ├── Audit Logging
    └── Sample Data Initialization
```

## Data Flow

### Authentication Flow

```
User Login
    ↓
Frontend: POST /api/auth/login
    ↓
Backend: Verify Credentials
    ↓
Backend: Generate JWT Token
    ↓
Frontend: Store Token & User Info
    ↓
Frontend: Redirect to Dashboard
    ↓
All Subsequent Requests: Include JWT in Header
```

### Dashboard Data Flow

```
User Navigates to Dashboard
    ↓
Frontend: GET /api/dashboard/overview
    ↓
Backend: Query Multiple Tables
    ├── Count Vulnerabilities
    ├── Count Incidents
    ├── Count Threats
    ├── Count Alerts
    ├── Calculate Risk Score
    ├── Calculate Compliance Score
    └── Fetch Recent Events
    ↓
Backend: Return Aggregated Data
    ↓
Frontend: Store in Zustand
    ↓
Frontend: Render Dashboard
```

### Vulnerability Management Flow

```
Analyst Views Vulnerabilities
    ↓
Frontend: GET /api/vulnerabilities?severity=High&status=open
    ↓
Backend: Query Vulnerabilities Table with Filters
    ↓
Backend: Return Paginated Results
    ↓
Frontend: Display in Table
    ↓
Analyst Updates Vulnerability Status
    ↓
Frontend: PUT /api/vulnerabilities/{id}
    ↓
Backend: Update Database
    ↓
Backend: Create Audit Log Entry
    ↓
Backend: Return Updated Record
    ↓
Frontend: Refresh Display
```

## Security Architecture

### Authentication & Authorization

```
Login Request
    ↓
Password Verification (bcrypt)
    ↓
JWT Token Generation (24 hour expiry)
    ↓
Token Stored in Browser localStorage
    ↓
All API Requests Include Token
    ↓
Backend: Verify JWT Signature
    ↓
Backend: Check User Role
    ↓
Backend: Check Permissions
    ↓
Allow/Deny Request
```

### Data Protection

- **Passwords**: Hashed with Werkzeug (bcrypt)
- **Tokens**: JWT with HS256 signature
- **API**: CORS protection
- **Database**: SQLite with parameterized queries
- **Audit**: All modifications logged with timestamp, user, and action

## Scalability Considerations

### Current Limitations (SQLite)
- Max ~100K records
- Single-threaded
- No concurrent write optimization
- File-based storage

### For Production Scale-up

1. **Replace SQLite with PostgreSQL**
   - Multi-user concurrency
   - Advanced indexing
   - Built-in replication

2. **Add Redis Caching**
   - Session storage
   - Query result caching
   - Real-time data feeds

3. **Implement Horizontal Scaling**
   - Load balancer (nginx)
   - Multiple Flask instances
   - Database connection pooling

4. **Add Message Queue**
   - Celery for async tasks
   - Real-time updates via WebSocket
   - Bulk data import processing

5. **Monitoring & Observability**
   - Prometheus metrics
   - ELK Stack for logging
   - APM (Datadog, New Relic)

## API Documentation

### Request/Response Format

```json
Request Header:
{
  "Authorization": "Bearer eyJhbGc...",
  "Content-Type": "application/json"
}

Success Response (200):
{
  "data": { ... },
  "message": "Success",
  "status": 200
}

Error Response (4xx/5xx):
{
  "error": "Error description",
  "status": 400
}
```

### Rate Limiting (Future)
- 1000 requests per minute per user
- 100 requests per second per API
- 30-second timeout for long operations

## Performance Metrics

### Current Performance
- Dashboard load: <500ms
- Vulnerability list: <300ms
- Search/filter: <200ms
- Compliance matrix: <400ms

### Target Performance (Production)
- Dashboard load: <200ms
- List views: <100ms
- Search: <50ms
- Complex queries: <1s

---

**Architecture designed for enterprise security operations at scale**
