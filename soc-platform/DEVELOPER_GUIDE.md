# SOC Platform - Developer Guide

## Project Setup for Development

### Prerequisites
- Visual Studio Code
- Python 3.12+ with venv
- Node.js LTS (18+)
- Git

### VS Code Extensions (Recommended)
- Python
- Pylint
- Prettier
- ES7+ React/Redux/React-Native snippets
- SQLite
- REST Client

### Initial Setup

```bash
# Clone project
cd d:/e-commerce-devops/soc-platform

# Backend development
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov pylint black  # Dev tools

# Frontend development
cd ../frontend
npm install
npm install --save-dev eslint prettier  # Dev tools
```

## Code Structure

### Backend Code Style

```python
# app/models/user.py
from app import db
from datetime import datetime

class User(db.Model):
    """User model with authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # ... additional fields
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            # ... additional fields
        }
```

### Frontend Code Style

```jsx
// components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { dashboardService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    try {
      // Implementation
    } catch (error) {
      // Error handling
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <>
      <TopNavbar />
      <Sidebar />
      <div className="main-content">
        {/* Content */}
      </div>
    </>
  );
}
```

## Common Development Tasks

### Adding a New Page

1. **Create React Component**
   ```bash
   # components/NewFeature.jsx
   ```

2. **Add Route to App.jsx**
   ```javascript
   <Route path="/new-feature" element={<ProtectedRoute><NewFeature /></ProtectedRoute>} />
   ```

3. **Add Sidebar Navigation**
   ```javascript
   // components/Sidebar.jsx
   <Nav.Link as={Link} to="/new-feature">
     <FaIcon /> New Feature
   </Nav.Link>
   ```

4. **Add API Service**
   ```javascript
   // services/api.js
   export const newFeatureService = {
     getItems: (params) => apiClient.get('/new-feature', { params }),
     createItem: (data) => apiClient.post('/new-feature', data),
   };
   ```

### Adding a New API Endpoint

1. **Create Backend Routes**
   ```python
   # app/routes/new_feature_routes.py
   from flask import Blueprint
   
   bp = Blueprint('new_feature', __name__, url_prefix='/api/new-feature')
   
   @bp.route('', methods=['GET'])
   @jwt_required()
   def get_items():
       # Implementation
       return jsonify(...), 200
   ```

2. **Register Blueprint in app/__init__.py**
   ```python
   from app.routes import new_feature_routes
   app.register_blueprint(new_feature_routes.bp)
   ```

3. **Add Model if needed**
   ```python
   # app/models/new_feature.py
   class NewFeature(db.Model):
       __tablename__ = 'new_features'
       # Implementation
   ```

### Adding New Database Migration

```bash
# Create model
# app/models/new_model.py

# In app/__init__.py
with app.app_context():
    db.create_all()
```

## Testing

### Backend Testing

```bash
# Unit tests
pytest app/tests/ -v

# Coverage report
pytest --cov=app --cov-report=html

# Specific test
pytest app/tests/test_auth.py::test_login
```

### Frontend Testing

```bash
# Run tests
npm test

# Coverage
npm test -- --coverage

# Specific test
npm test -- Dashboard.test.jsx
```

## Debugging

### Backend Debugging

```python
# Use Python debugger
import pdb
pdb.set_trace()

# Or use Flask debug mode (already enabled in development)
# Breakpoints in VS Code
```

### Frontend Debugging

```javascript
// Browser DevTools
console.log('Debug:', variable);
debugger;  // Adds breakpoint

// VS Code debugging
// Add .vscode/launch.json:
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

## Database Queries

### Common ORM Patterns

```python
# Find by ID
user = User.query.get(user_id)

# Filter by condition
vulnerabilities = Vulnerability.query.filter_by(status='open').all()

# Complex filters
incidents = Incident.query.filter(
    (Incident.severity == 'Critical') & 
    (Incident.status == 'open')
).order_by(Incident.created_date.desc()).all()

# Pagination
page = Vulnerability.query.paginate(page=1, per_page=20)

# Aggregation
count = db.session.query(db.func.count(Vulnerability.id)).scalar()
avg_cvss = db.session.query(db.func.avg(Vulnerability.cvss_score)).scalar()

# Join queries
results = db.session.query(User, AuditLog).join(
    AuditLog, User.id == AuditLog.user_id
).filter(User.role == 'admin').all()
```

## Performance Optimization

### Backend
```python
# Use select() for specific columns
from sqlalchemy import select

# Lazy load relations
vulnerabilities = Vulnerability.query.options(
    db.joinedload(Vulnerability.asset)
).all()

# Index frequently queried columns
class Vulnerability(db.Model):
    __table_args__ = (
        db.Index('ix_vuln_status', 'status'),
        db.Index('ix_vuln_severity', 'severity'),
    )
```

### Frontend
```javascript
// Memoize expensive components
const MemoizedDashboard = React.memo(Dashboard);

// Use useCallback for event handlers
const handleClick = useCallback(() => {
  // Handler logic
}, [dependencies]);

// Lazy load routes
const Vulnerabilities = React.lazy(() => import('./components/Vulnerabilities'));
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "feat: add new feature"

# Push to origin
git push origin feature/new-feature

# Create Pull Request
# Review and merge
```

## Commit Message Convention

```
feat: add new feature
fix: fix bug in vulnerabilities
docs: update README
style: format code
refactor: restructure models
test: add unit tests
perf: optimize dashboard query
```

## Environment Variables

### Backend (.env)
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-key-change-in-production
JWT_SECRET_KEY=jwt-dev-key-change-in-production
DATABASE_URL=sqlite:///soc_platform.db
```

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_DEBUG=true
```

## Production Checklist

- [ ] Update SECRET_KEY and JWT_SECRET_KEY
- [ ] Set FLASK_ENV=production
- [ ] Disable Flask debug mode
- [ ] Use production database (PostgreSQL)
- [ ] Set up HTTPS/TLS
- [ ] Configure CORS for specific origins
- [ ] Enable rate limiting
- [ ] Set up monitoring/logging
- [ ] Implement backup strategy
- [ ] Security audit completed

## Useful Commands

```bash
# Backend
python app.py --port 5001          # Run on different port
pip freeze > requirements.txt      # Export dependencies
pytest --cov                        # Run tests with coverage
python -m black app/                # Format code

# Frontend
npm start --port 3001               # Run on different port
npm run build                       # Production build
npm test -- --coverage             # Test with coverage
npx eslint src/                    # Lint code
npx prettier --write src/           # Format code
```

## Troubleshooting Development

### Port conflicts
```bash
# Find process on port
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### Database issues
```bash
# Reset database
rm backend/soc_platform.db
python backend/app.py
```

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
npm install
```

---

**Happy coding!** 🚀
