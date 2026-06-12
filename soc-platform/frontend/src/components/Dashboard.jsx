import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Spinner, Alert } from 'react-bootstrap';
import { dashboardService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';
import '../styles/theme.css';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await dashboardService.getOverview();
        setData(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger" role="alert">
        Error: {error}
      </Alert>
    );
  }

  const getSeverityBadgeClass = (severity) => {
    switch (severity) {
      case 'Critical': return 'badge-critical';
      case 'High': return 'badge-high';
      case 'Medium': return 'badge-medium';
      case 'Low': return 'badge-low';
      default: return 'badge-secondary';
    }
  };

  const getRiskColor = (score) => {
    if (score >= 80) return '#e94560';
    if (score >= 60) return '#ff6b6b';
    if (score >= 40) return '#ffa502';
    return '#51cf66';
  };

  return (
    <>
      <TopNavbar />
      <Sidebar />
      
      <div className="main-content">
        <Container fluid>
          <Row className="mb-4">
            <Col>
              <h1 className="display-4">Executive Dashboard</h1>
              <p className="text-muted">Real-time security operations overview</p>
            </Col>
          </Row>

          {/* KPI Cards */}
          <Row className="dashboard-grid">
            <Col md={3}>
              <div className="kpi-card">
                <div className="kpi-label">Total Vulnerabilities</div>
                <div className="kpi-value">{data?.vulnerabilities?.total || 0}</div>
                <div className="kpi-label">Critical: {data?.vulnerabilities?.critical || 0}</div>
              </div>
            </Col>
            <Col md={3}>
              <div className="kpi-card">
                <div className="kpi-label">Open Incidents</div>
                <div className="kpi-value" style={{color: '#ff6b6b'}}>{data?.incidents?.open || 0}</div>
                <div className="kpi-label">Total: {data?.incidents?.total || 0}</div>
              </div>
            </Col>
            <Col md={3}>
              <div className="kpi-card">
                <div className="kpi-label">Active Threats</div>
                <div className="kpi-value" style={{color: '#ffa502'}}>{data?.threats?.active || 0}</div>
                <div className="kpi-label">Total: {data?.threats?.total || 0}</div>
              </div>
            </Col>
            <Col md={3}>
              <div className="kpi-card">
                <div className="kpi-label">New Alerts</div>
                <div className="kpi-value" style={{color: '#ff8787'}}>{data?.alerts?.new || 0}</div>
                <div className="kpi-label">Total: {data?.alerts?.total || 0}</div>
              </div>
            </Col>
          </Row>

          {/* Risk and Compliance Scores */}
          <Row className="mb-4">
            <Col md={6}>
              <Card>
                <Card.Header>
                  <Card.Title className="mb-0">Organizational Risk Score</Card.Title>
                </Card.Header>
                <Card.Body>
                  <div className="risk-meter">
                    <div 
                      className="risk-meter-fill" 
                      style={{width: `${data?.risk_score || 0}%`}}
                    >
                      {Math.round(data?.risk_score || 0)}%
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Col>
            <Col md={6}>
              <Card>
                <Card.Header>
                  <Card.Title className="mb-0">Compliance Status</Card.Title>
                </Card.Header>
                <Card.Body>
                  <div className="risk-meter">
                    <div 
                      className="risk-meter-fill" 
                      style={{width: `${data?.compliance_score || 0}%`}}
                    >
                      {Math.round(data?.compliance_score || 0)}%
                    </div>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          </Row>

          {/* Recent Events */}
          <Row>
            <Col lg={4}>
              <Card className="mb-4">
                <Card.Header>
                  <Card.Title className="mb-0">Recent Vulnerabilities</Card.Title>
                </Card.Header>
                <Card.Body className="p-0">
                  <Table hover className="mb-0">
                    <tbody>
                      {data?.recent?.vulnerabilities?.slice(0, 5).map(vuln => (
                        <tr key={vuln.id}>
                          <td>
                            <small>
                              <span className={`badge ${getSeverityBadgeClass(vuln.severity)}`}>
                                {vuln.severity}
                              </span>
                            </small>
                            <br />
                            <small>{vuln.title}</small>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </Card.Body>
              </Card>
            </Col>

            <Col lg={4}>
              <Card className="mb-4">
                <Card.Header>
                  <Card.Title className="mb-0">Recent Incidents</Card.Title>
                </Card.Header>
                <Card.Body className="p-0">
                  <Table hover className="mb-0">
                    <tbody>
                      {data?.recent?.incidents?.slice(0, 5).map(incident => (
                        <tr key={incident.id}>
                          <td>
                            <small>
                              <span className={`badge ${getSeverityBadgeClass(incident.severity)}`}>
                                {incident.severity}
                              </span>
                            </small>
                            <br />
                            <small>{incident.title}</small>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </Card.Body>
              </Card>
            </Col>

            <Col lg={4}>
              <Card className="mb-4">
                <Card.Header>
                  <Card.Title className="mb-0">Recent Alerts</Card.Title>
                </Card.Header>
                <Card.Body className="p-0">
                  <Table hover className="mb-0">
                    <tbody>
                      {data?.recent?.alerts?.slice(0, 5).map(alert => (
                        <tr key={alert.id}>
                          <td>
                            <small>
                              <span className={`badge ${getSeverityBadgeClass(alert.severity)}`}>
                                {alert.severity}
                              </span>
                            </small>
                            <br />
                            <small>{alert.title}</small>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}
