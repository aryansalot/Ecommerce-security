# Enterprise SOC Platform - Installation Guide

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.12 or higher
- **Node.js**: LTS version (18+)
- **RAM**: Minimum 4GB
- **Disk Space**: 2GB free

## Full Installation Steps

### 1. Python Installation

#### Windows
1. Download Python 3.12 from python.org
2. Run installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

#### macOS
```bash
# Using Homebrew
brew install python@3.12
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv python3-pip
```

### 2. Node.js Installation

#### Windows & macOS
Download from nodejs.org and run installer

#### Linux
```bash
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 3. Clone/Extract Project

```bash
# Navigate to your projects directory
cd d:/e-commerce-devops

# Project already at:
# d:/e-commerce-devops/soc-platform
```

### 4. Backend Installation

```bash
cd soc-platform/backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Verify activation (should show (.venv) prefix)

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env
# Or on macOS/Linux:
cp .env.example .env

# Edit .env if needed (optional)
# notepad .env  # Windows
# nano .env     # macOS/Linux
```

### 5. Frontend Installation

```bash
cd ../frontend

# Install Node dependencies
npm install

# This may take 2-3 minutes
```

### 6. Running the Application

#### Terminal 1 - Backend

```bash
cd soc-platform/backend

# Activate virtual environment (if not already active)
.venv\Scripts\activate

# Start Flask server
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

#### Terminal 2 - Frontend

```bash
cd soc-platform/frontend

# Start React dev server
npm start
```

Expected output:
```
webpack compiled successfully
You can now view soc-platform-frontend in the browser.

Local:            http://localhost:3000
```

### 7. Access Application

Open your browser and go to:
```
http://localhost:3000
```

### 8. Login

Use the default credentials:
- **Email/Username**: admin
- **Password**: admin123

## Verification Checklist

- [ ] Python 3.12+ installed (`python --version`)
- [ ] Node.js LTS installed (`node --version`)
- [ ] Backend dependencies installed (`pip list` shows Flask, SQLAlchemy, etc.)
- [ ] Frontend dependencies installed (`npm ls --depth=0`)
- [ ] Backend running on http://localhost:5000
- [ ] Frontend running on http://localhost:3000
- [ ] Can login with admin credentials
- [ ] Dashboard loads successfully

## Common Installation Issues

### Issue: Python not found
**Solution**: Add Python to PATH
- Windows: Reinstall Python and check "Add Python to PATH"
- macOS: `export PATH="/usr/local/opt/python@3.12/bin:$PATH"`

### Issue: pip not found
**Solution**:
```bash
python -m pip --version
python -m pip install --upgrade pip
```

### Issue: Port 5000 already in use
**Solution**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # macOS/Linux

# Kill process (get PID from above)
taskkill /PID <PID> /F  # Windows
kill -9 <PID>  # macOS/Linux
```

### Issue: Port 3000 already in use
**Solution**:
```bash
PORT=3001 npm start
```

### Issue: npm ERR! 
**Solution**:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Issue: CORS errors in console
**Solution**: Ensure both servers are running

### Issue: Database errors
**Solution**:
```bash
# Delete and recreate database
rm soc_platform.db
python app.py
```

## Development Workflow

1. Start backend in Terminal 1
2. Start frontend in Terminal 2
3. Access http://localhost:3000
4. Make code changes (hot reload enabled)
5. Check browser console for errors
6. Check backend terminal for API errors

## Production Deployment

For production use:

1. **Install production dependencies**:
```bash
pip install gunicorn
npm install -g serve
```

2. **Build frontend**:
```bash
npm run build
```

3. **Run production backend**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. **Serve frontend**:
```bash
serve -s build -l 3000
```

## Docker Setup (Optional)

If you want to use Docker:

**Dockerfile** (backend):
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Dockerfile** (frontend):
```dockerfile
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

## Next Steps

1. Review [README.md](README.md) for feature documentation
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for operational details
3. Explore the UI and dashboards
4. Check sample data and customize
5. Review API endpoints
6. Plan integration with your security tools

## Support

For issues:
1. Check browser console (F12)
2. Check backend terminal for errors
3. Review error messages carefully
4. Check Common Installation Issues above

## Additional Resources

- [Python Documentation](https://docs.python.org/3.12/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

**Installation Complete!** 🎉

The enterprise SOC platform is now running and ready to use.
