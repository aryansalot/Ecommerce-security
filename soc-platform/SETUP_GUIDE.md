# SOC Platform - SETUP GUIDE

## Quick Start (5 minutes)

### Prerequisites
- Python 3.12+
- Node.js LTS
- Git (optional)

### Step 1: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Run Flask server
python app.py
```

Backend runs at: http://localhost:5000

### Step 2: Frontend Setup (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React dev server
npm start
```

Frontend runs at: http://localhost:3000

### Step 3: Login

Access http://localhost:3000 and login with:
- **Username**: admin
- **Password**: admin123

## Project Structure

```
soc-platform/
├── backend/
│   ├── app/
│   │   ├── models/           # Database models
│   │   │   ├── user.py
│   │   │   ├── vulnerability.py
│   │   │   ├── incident.py
│   │   │   ├── threat.py
│   │   │   ├── alert.py
│   │   │   ├── compliance.py
│   │   │   ├── mitre.py
│   │   │   ├── asset.py
│   │   │   └── audit_log.py
│   │   ├── routes/           # API endpoints
│   │   │   ├── auth_routes.py
│   │   │   ├── dashboard_routes.py
│   │   │   ├── vulnerability_routes.py
│   │   │   ├── incident_routes.py
│   │   │   ├── threat_routes.py
│   │   │   ├── alert_routes.py
│   │   │   ├── compliance_routes.py
│   │   │   ├── mitre_routes.py
│   │   │   ├── asset_routes.py
│   │   │   └── risk_routes.py
│   │   ├── services/         # Business logic
│   │   │   └── risk_service.py
│   │   └── utils/            # Utilities
│   │       ├── auth.py
│   │       └── sample_data.py
│   ├── app.py                # Flask app entry
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
└── frontend/
    ├── src/
    │   ├── components/       # React components
    │   │   ├── Dashboard.jsx
    │   │   ├── Login.jsx
    │   │   ├── Vulnerabilities.jsx
    │   │   ├── Incidents.jsx
    │   │   ├── Threats.jsx
    │   │   ├── Alerts.jsx
    │   │   ├── Compliance.jsx
    │   │   ├── MITRE.jsx
    │   │   ├── Assets.jsx
    │   │   ├── RiskAnalysis.jsx
    │   │   ├── TopNavbar.jsx
    │   │   ├── Sidebar.jsx
    │   │   └── ProtectedRoute.jsx
    │   ├── services/         # API services
    │   │   └── api.js
    │   ├── context/          # State management
    │   │   └── store.js
    │   ├── styles/           # CSS
    │   │   └── theme.css
    │   ├── App.jsx
    │   └── index.js
    ├── public/
    │   └── index.html
    ├── package.json
    └── .gitignore
```

## Features Overview

### 1. Dashboard
- Real-time security KPIs
- Vulnerability count and severity
- Incident status overview
- Active threats tracking
- Compliance and risk scores

### 2. Vulnerability Management
- CVE tracking with CVSS scores
- Severity classification
- Status tracking (open, mitigated, resolved)
- Remediation tracking
- Asset impact analysis

### 3. Incident Management
- Full incident lifecycle
- Status tracking
- Root cause analysis
- Timeline tracking
- Response time metrics

### 4. Threat Intelligence
- IOC (Indicator of Compromise) tracking
- Threat type classification
- Confidence scoring
- Source tracking
- Multi-type IOC support (IP, domain, hash, email)

### 5. Alert Management
- Alert triage
- Severity classification
- Status tracking
- Batch acknowledge/resolve
- Auto-assignment

### 6. Compliance Dashboard
- Framework tracking (PCI-DSS, HIPAA, SOC2, CIS, OWASP)
- Requirement status
- Compliance scoring
- Remediation tracking

### 7. MITRE ATT&CK
- Attack technique tracking
- Tactic classification
- Detection statistics
- Matrix visualization

### 8. Asset Inventory
- Asset discovery
- Type classification
- Criticality levels
- Vulnerability association
- Owner tracking

### 9. Risk Analysis
- AI risk scoring
- Heatmap visualization
- Security scorecard
- Recommendations engine

### 10. User Management
- Multi-role support (admin, manager, analyst)
- Department tracking
- Activity logging
- Access control

## Demo Users

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| manager | manager123 | Manager |
| analyst | analyst123 | Analyst |

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Register user
- `GET /api/auth/profile` - Get profile

### Dashboard  
- `GET /api/dashboard/overview` - Dashboard data
- `GET /api/dashboard/health` - Security health
- `GET /api/dashboard/metrics` - Key metrics
- `GET /api/dashboard/timeline` - Event timeline

### Vulnerabilities
- `GET /api/vulnerabilities` - List vulnerabilities
- `POST /api/vulnerabilities` - Create vulnerability
- `GET /api/vulnerabilities/<id>` - Get vulnerability
- `PUT /api/vulnerabilities/<id>` - Update vulnerability
- `DELETE /api/vulnerabilities/<id>` - Delete vulnerability

### Incidents
- `GET /api/incidents` - List incidents
- `POST /api/incidents` - Create incident
- `GET /api/incidents/<id>` - Get incident
- `PUT /api/incidents/<id>` - Update incident

### Threats
- `GET /api/threats` - List threats
- `POST /api/threats` - Create threat
- `GET /api/threats/<id>` - Get threat
- `PUT /api/threats/<id>` - Update threat

### Alerts
- `GET /api/alerts` - List alerts
- `PUT /api/alerts/<id>/acknowledge` - Acknowledge alert
- `PUT /api/alerts/<id>/resolve` - Resolve alert

### Compliance
- `GET /api/compliance` - List compliance items
- `GET /api/compliance/frameworks` - Framework scores
- `GET /api/compliance/overall` - Overall score
- `GET /api/compliance/matrix` - Compliance matrix

### MITRE
- `GET /api/mitre/techniques` - List techniques
- `GET /api/mitre/matrix` - Attack matrix
- `GET /api/mitre/detections` - Detection stats

### Assets
- `GET /api/assets` - List assets
- `POST /api/assets` - Create asset
- `GET /api/assets/<id>` - Get asset
- `PUT /api/assets/<id>` - Update asset

### Risk
- `GET /api/risk/score` - Org risk score
- `GET /api/risk/heatmap` - Risk heatmap
- `GET /api/risk/scorecard` - Security scorecard
- `GET /api/risk/asset/<id>` - Asset risk score

## Database

SQLite database automatically created at:
- `backend/soc_platform.db`

Sample data automatically initialized on first run.

## Troubleshooting

### Backend won't start
```bash
# Check Python version (3.12+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend won't start
```bash
# Clear npm cache
npm cache clean --force

# Reinstall packages
rm -rf node_modules package-lock.json
npm install
```

### CORS errors
Ensure backend is running on http://localhost:5000

### Port already in use
```bash
# Backend
python app.py --port 5001

# Frontend
PORT=3001 npm start
```

## Performance Tips

1. **Database**: SQLite is suitable for up to 100K records
2. **Caching**: Frontend caches API responses
3. **Pagination**: APIs support pagination for large datasets
4. **Indexing**: Database indexes on frequently filtered fields

## Security Features

- JWT token-based authentication
- Password hashing with Werkzeug
- CORS protection
- Role-based access control
- SQL injection prevention
- Comprehensive audit logging
- Secure password reset capability

## Deployment Considerations

### For Production:
1. Replace SQLite with PostgreSQL
2. Add Redis for caching
3. Use HTTPS/TLS
4. Implement rate limiting
5. Add WAF (Web Application Firewall)
6. Set up monitoring and alerting
7. Implement backup strategy
8. Use environment-specific configs

## Support & Documentation

See README.md for comprehensive documentation.

---

**Built for Enterprise Security Teams** 🛡️
