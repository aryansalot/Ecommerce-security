import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Vulnerabilities from './components/Vulnerabilities';
import Incidents from './components/Incidents';
import Threats from './components/Threats';
import Alerts from './components/Alerts';
import Compliance from './components/Compliance';
import MITRE from './components/MITRE';
import Assets from './components/Assets';
import RiskAnalysis from './components/RiskAnalysis';
import ProtectedRoute from './components/ProtectedRoute';
import './styles/theme.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/vulnerabilities"
          element={
            <ProtectedRoute>
              <Vulnerabilities />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/incidents"
          element={
            <ProtectedRoute>
              <Incidents />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/threats"
          element={
            <ProtectedRoute>
              <Threats />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/alerts"
          element={
            <ProtectedRoute>
              <Alerts />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/compliance"
          element={
            <ProtectedRoute>
              <Compliance />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/mitre"
          element={
            <ProtectedRoute>
              <MITRE />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/assets"
          element={
            <ProtectedRoute>
              <Assets />
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/risk"
          element={
            <ProtectedRoute>
              <RiskAnalysis />
            </ProtectedRoute>
          }
        />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
