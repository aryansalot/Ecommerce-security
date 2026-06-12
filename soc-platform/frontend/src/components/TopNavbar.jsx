import React from 'react';
import { Container, Row, Col, Navbar, Nav } from 'react-bootstrap';
import { FaSignOutAlt, FaUser } from 'react-icons/fa';
import { useAuthStore } from '../context/store';
import { useNavigate } from 'react-router-dom';

export default function TopNavbar() {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Navbar bg="dark" expand="lg" className="navbar-dark fixed-top">
      <Container fluid>
        <Navbar.Brand href="/" className="fw-bold">
          🛡️ SOC Platform
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link className="d-flex align-items-center gap-2">
              <FaUser /> {user?.username}
            </Nav.Link>
            <Nav.Link onClick={handleLogout} className="d-flex align-items-center gap-2">
              <FaSignOutAlt /> Logout
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
