# Enterprise Security Operations Center (SOC) Platform

A complete, enterprise-grade cybersecurity platform built with modern web technologies.

## 🛡️ Features

### Core Modules
- **Authentication System** - JWT-based authentication with role-based access control
- **Executive Dashboard** - Real-time security KPIs and metrics
- **Vulnerability Management** - CVSS-based vulnerability tracking
- **Incident Management** - Full incident lifecycle management
- **Threat Intelligence** - IOC tracking and threat monitoring
- **Alert Management** - Centralized alert aggregation
- **Compliance Dashboard** - PCI-DSS, HIPAA, SOC2, CIS, OWASP tracking
- **MITRE ATT&CK Mapping** - Threat technique tracking
- **Asset Inventory** - Complete asset management system
- **Risk Analysis** - AI-powered risk scoring engine

### Advanced Features
- Dark-themed enterprise UI
- Real-time data visualization
- Risk scoring algorithms
- Compliance calculators
- Incident timeline tracking
- Audit logging system

## 🏗️ Architecture

### Backend
- **Python 3.12** with Flask REST API
- **SQLite** database
- JWT authentication
- Role-based access control
- AI risk scoring engine

### Frontend
- **React 18** with React Router
- **Bootstrap 5** for responsive design
- **Chart.js** for data visualization
- **Zustand** for state management
- Dark theme with professional styling

## 📋 Prerequisites

- Python 3.12+
- Node.js LTS
- pip (Python package manager)
- npm (Node package manager)

## 🚀 Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Run server
python app.py
```

The backend will start at `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will start at `http://localhost:3000`

## 🔐 Default Credentials

- **Username**: admin
- **Password**: admin123

Other demo users:
- **manager/manager123** (Manager role)
- **analyst/analyst123** (Analyst role)

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Dashboard
- `GET /api/dashboard/overview` - Dashboard overview
- `GET /api/dashboard/health` - Security health
- `GET /api/dashboard/metrics` - Key metrics
- `GET /api/dashboard/timeline` - Events timeline

### Vulnerabilities
- `GET /api/vulnerabilities` - List vulnerabilities
- `POST /api/vulnerabilities` - Create vulnerability
- `GET /api/vulnerabilities/<id>` - Get vulnerability
- `PUT /api/vulnerabilities/<id>` - Update vulnerability
- `DELETE /api/vulnerabilities/<id>` - Delete vulnerability
- `GET /api/vulnerabilities/statistics` - Vulnerability stats

### Incidents
- `GET /api/incidents` - List incidents
- `POST /api/incidents` - Create incident
- `GET /api/incidents/<id>` - Get incident
- `PUT /api/incidents/<id>` - Update incident
- `GET /api/incidents/statistics` - Incident stats

### Threats
- `GET /api/threats` - List threats
- `POST /api/threats` - Create threat
- `GET /api/threats/<id>` - Get threat
- `PUT /api/threats/<id>` - Update threat
- `GET /api/threats/iocs` - IOC statistics
- `GET /api/threats/statistics` - Threat stats

### Alerts
- `GET /api/alerts` - List alerts
- `GET /api/alerts/<id>` - Get alert
- `PUT /api/alerts/<id>/acknowledge` - Acknowledge alert
- `PUT /api/alerts/<id>/resolve` - Resolve alert
- `GET /api/alerts/statistics` - Alert stats

### Compliance
- `GET /api/compliance` - List compliance statuses
- `GET /api/compliance/frameworks` - Framework scores
- `GET /api/compliance/overall` - Overall compliance
- `GET /api/compliance/matrix` - Compliance matrix

### MITRE ATT&CK
- `GET /api/mitre/techniques` - List techniques
- `GET /api/mitre/tactics` - List tactics
- `GET /api/mitre/matrix` - Attack matrix
- `GET /api/mitre/detections` - Detection statistics

### Assets
- `GET /api/assets` - List assets
- `POST /api/assets` - Create asset
- `GET /api/assets/<id>` - Get asset
- `PUT /api/assets/<id>` - Update asset
- `GET /api/assets/statistics` - Asset stats

### Risk
- `GET /api/risk/score` - Organizational risk score
- `GET /api/risk/heatmap` - Risk heatmap
- `GET /api/risk/scorecard` - Security scorecard
- `GET /api/risk/asset/<id>` - Asset risk score

## 🎨 UI Features

- **Dark Theme**: Enterprise-grade dark mode UI
- **Responsive Design**: Works on desktop and tablets
- **Real-time Updates**: Live data visualization
- **KPI Cards**: Executive-level metrics
- **Data Tables**: Sortable and filterable tables
- **Status Badges**: Color-coded severity levels
- **Charts**: Risk metrics and trends
- **Navigation**: Intuitive sidebar navigation

## 🔄 Workflow

1. **User Authentication** → Login with credentials
2. **Dashboard Overview** → View security metrics
3. **Vulnerability Tracking** → Manage CVEs and patches
4. **Incident Response** → Track and respond to incidents
5. **Threat Intelligence** → Monitor threats and IOCs
6. **Alert Management** → Triage and respond to alerts
7. **Compliance Monitoring** → Track framework compliance
8. **Risk Analysis** → Review organizational risk

## 📈 Sample Data

The system initializes with realistic sample data including:
- Multiple user accounts
- 8+ sample vulnerabilities
- 5 sample incidents
- 5 active threats
- 10 security alerts
- 11 compliance requirements
- 6 MITRE techniques
- 5 assets

## 🛠️ Development

### Project Structure

```
soc-platform/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── app.py
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   ├── styles/
    │   └── context/
    ├── public/
    └── package.json
```

## 📝 Documentation

### Running the Complete Stack

1. **Terminal 1 - Backend**:
```bash
cd backend
.venv\Scripts\activate
python app.py
```

2. **Terminal 2 - Frontend**:
```bash
cd frontend
npm start
```

3. **Access Application**:
Open http://localhost:3000 in your browser

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Werkzeug
- Role-based access control (RBAC)
- CORS protection
- Audit logging system
- SQL injection prevention
- Secure API endpoints

## 📊 Risk Scoring Algorithm

The AI risk scoring engine considers:
- Vulnerability CVSS scores
- Incident severity and count
- Active threat count
- Asset criticality
- Vulnerability remediation status

## 🎯 Use Cases

- **SOC Analysts**: Track and respond to alerts
- **Security Managers**: Monitor compliance and risk
- **CISOs**: Executive-level security overview
- **Compliance Teams**: Track framework requirements
- **Threat Intel Teams**: Monitor IOCs and threats

## 🚨 Enterprise Ready

- Production-grade code structure
- Error handling and logging
- Scalable database design
- RESTful API architecture
- Professional UI/UX
- Role-based permissions

## 📞 Support

For issues, questions, or contributions, please refer to the documentation or contact your security team.

---

**Built with ❤️ for Enterprise Security Teams**
