import React from 'react';
import { Nav } from 'react-bootstrap';
import { Link, useLocation } from 'react-router-dom';
import { 
  FaChartBar, FaShieldAlt, FaBug, FaExclamationTriangle, 
  FaNetworkWired, FaBell, FaClipboardList, FaMap, FaBoxes
} from 'react-icons/fa';

export default function Sidebar() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="sidebar">
      <Nav className="flex-column">
        <Nav.Link 
          as={Link} 
          to="/" 
          className={`sidebar-item ${isActive('/') ? 'active' : ''}`}
        >
          <FaChartBar className="me-2" /> Dashboard
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/vulnerabilities" 
          className={`sidebar-item ${isActive('/vulnerabilities') ? 'active' : ''}`}
        >
          <FaBug className="me-2" /> Vulnerabilities
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/incidents" 
          className={`sidebar-item ${isActive('/incidents') ? 'active' : ''}`}
        >
          <FaExclamationTriangle className="me-2" /> Incidents
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/threats" 
          className={`sidebar-item ${isActive('/threats') ? 'active' : ''}`}
        >
          <FaNetworkWired className="me-2" /> Threats
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/alerts" 
          className={`sidebar-item ${isActive('/alerts') ? 'active' : ''}`}
        >
          <FaBell className="me-2" /> Alerts
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/compliance" 
          className={`sidebar-item ${isActive('/compliance') ? 'active' : ''}`}
        >
          <FaClipboardList className="me-2" /> Compliance
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/mitre" 
          className={`sidebar-item ${isActive('/mitre') ? 'active' : ''}`}
        >
          <FaMap className="me-2" /> MITRE ATT&CK
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/assets" 
          className={`sidebar-item ${isActive('/assets') ? 'active' : ''}`}
        >
          <FaBoxes className="me-2" /> Assets
        </Nav.Link>
        
        <Nav.Link 
          as={Link} 
          to="/risk" 
          className={`sidebar-item ${isActive('/risk') ? 'active' : ''}`}
        >
          <FaShieldAlt className="me-2" /> Risk Analysis
        </Nav.Link>
      </Nav>
    </div>
  );
}
