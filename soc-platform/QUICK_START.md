# Enterprise Security Operations Center (SOC) Platform
## Quick Start Guide

### ⚡ 5-Minute Setup

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

Then open: http://localhost:3000

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 📊 Features at a Glance

### Dashboard
- Executive security metrics
- Real-time KPIs
- Risk scoring
- Compliance overview

### Vulnerability Management
- CVSS scoring
- Severity tracking
- Remediation workflows
- Asset correlation

### Incident Response
- Full incident lifecycle
- Timeline tracking
- Root cause analysis
- Metrics & analytics

### Threat Intelligence
- IOC tracking (IP, domain, hash, email)
- Threat source tracking
- Confidence scoring
- Multi-source feeds

### Alert Management
- Alert triage
- Severity classification
- Status tracking
- Bulk operations

### Compliance
- PCI-DSS tracking
- HIPAA compliance
- SOC2 requirements
- CIS Controls
- OWASP Top 10

### MITRE ATT&CK
- Attack technique mapping
- Tactic classification
- Detection stats
- Matrix visualization

### Asset Management
- Asset discovery
- Criticality levels
- Vulnerability tracking
- Owner management

### Risk Analysis
- AI risk scoring
- Risk heatmaps
- Security scorecard
- Recommendations

### Audit Logging
- User activity tracking
- Security event logs
- Change tracking
- Compliance reporting

---

## 🛠️ Technology Stack

**Frontend:**
- React 18
- React Router 6
- Bootstrap 5
- Chart.js
- Zustand
- Axios

**Backend:**
- Flask 3.0
- SQLAlchemy ORM
- Flask-JWT-Extended
- Flask-CORS
- SQLite

**Python Version:** 3.12+
**Node.js Version:** LTS (18+)

---

## 📁 Project Structure

```
soc-platform/
├── backend/                          # Flask REST API
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── models/                  # Database models (9 models)
│   │   ├── routes/                  # API endpoints (10 route files)
│   │   ├── services/                # Business logic
│   │   └── utils/                   # Helpers & auth
│   ├── app.py                       # Entry point
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Environment template
│
├── frontend/                         # React SPA
│   ├── src/
│   │   ├── components/              # React components (10+ components)
│   │   ├── services/                # API client
│   │   ├── context/                 # State management
│   │   ├── styles/                  # Dark theme CSS
│   │   ├── App.jsx
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   └── .env.example
│
├── README.md                         # Main documentation
├── SETUP_GUIDE.md                    # Operational guide
├── INSTALLATION_GUIDE.md             # Installation steps
├── ARCHITECTURE.md                   # System architecture
├── DEVELOPER_GUIDE.md                # Development guide
└── .gitignore
```

---

## 🔑 API Overview

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get profile
- `PUT /api/auth/profile` - Update profile

### Dashboard
- `GET /api/dashboard/overview` - Dashboard data
- `GET /api/dashboard/health` - Security health
- `GET /api/dashboard/metrics` - Metrics
- `GET /api/dashboard/timeline` - Event timeline

### Core Modules
- `GET /api/vulnerabilities` - List vulnerabilities
- `GET /api/incidents` - List incidents
- `GET /api/threats` - List threats
- `GET /api/alerts` - List alerts
- `GET /api/compliance` - List compliance items
- `GET /api/mitre/techniques` - MITRE techniques
- `GET /api/assets` - List assets
- `GET /api/risk/score` - Risk score

*Full API documentation in [README.md](README.md)*

---

## 👥 User Roles

| Role | Features |
|------|----------|
| **Admin** | Full access, user management, system settings |
| **Manager** | View all data, manage team, create reports |
| **Analyst** | View data, create tickets, acknowledge alerts |

---

## 📈 Sample Data Included

- 3 demo users (admin, manager, analyst)
- 5 production assets
- 8 sample vulnerabilities
- 5 sample incidents
- 5 active threats
- 10 security alerts
- 11 compliance requirements
- 6 MITRE ATT&CK techniques

---

## 🚀 Production Deployment

### Pre-Production Checklist
- [ ] Change SECRET_KEY and JWT_SECRET_KEY
- [ ] Update database to PostgreSQL
- [ ] Configure environment variables
- [ ] Enable HTTPS/TLS
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Security audit

### Deployment Options
- **Docker**: Use provided Dockerfiles
- **Traditional**: Gunicorn + Nginx + PostgreSQL
- **Cloud**: AWS, Azure, GCP (with modifications)

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Feature overview & API docs |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Operational procedures |
| [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) | Installation steps |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Development guidelines |

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.12+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend won't start
```bash
# Clear cache and reinstall
npm cache clean --force
npm install
```

### Port conflicts
```bash
# Find process using port
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

---

## ✨ Key Features

✅ **Enterprise-Grade UI**
- Dark theme optimized for SOC
- Responsive design
- Professional dashboards
- Real-time data

✅ **Complete Security Platform**
- Vulnerability management
- Incident response
- Threat intelligence
- Alert triage
- Compliance tracking

✅ **AI Risk Intelligence**
- Automated risk scoring
- Risk prioritization
- Security recommendations
- Compliance analytics

✅ **Production-Ready**
- JWT authentication
- Role-based access
- Audit logging
- Error handling

---

## 📞 Support

- Review documentation files
- Check browser console for errors
- Review backend terminal for API errors
- Verify both servers are running
- Clear browser cache if needed

---

## 🎯 Next Steps

1. **First-Time Users:**
   - Follow [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
   - Run the quick 5-minute setup above
   - Explore the dashboard

2. **Customization:**
   - Review [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
   - Add custom integrations
   - Modify sample data
   - Customize workflows

3. **Deployment:**
   - Read [ARCHITECTURE.md](ARCHITECTURE.md)
   - Set up production database
   - Configure security settings
   - Deploy to your environment

---

## 🏆 Enterprise-Ready Features

- ✅ Multi-tenant ready architecture
- ✅ Comprehensive audit logging
- ✅ Role-based access control
- ✅ RESTful API design
- ✅ Real-time data processing
- ✅ Scalable database schema
- ✅ Professional UI/UX
- ✅ Production-grade error handling

---

**Built for enterprise security teams. Runs completely in VS Code.** 🛡️

Last Updated: 2024
