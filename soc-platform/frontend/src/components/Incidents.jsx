import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Button, Spinner } from 'react-bootstrap';
import { incidentService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';

export default function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ severity: '', status: '' });

  useEffect(() => {
    fetchIncidents();
  }, [filter]);

  const fetchIncidents = async () => {
    try {
      const response = await incidentService.getIncidents(filter);
      setIncidents(response.data.incidents);
    } catch (error) {
      console.error('Error fetching incidents:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityBadgeClass = (severity) => {
    const classes = {
      'Critical': 'badge-critical',
      'High': 'badge-high',
      'Medium': 'badge-medium',
      'Low': 'badge-low'
    };
    return classes[severity] || 'badge-secondary';
  };

  return (
    <>
      <TopNavbar />
      <Sidebar />
      <div className="main-content">
        <Container fluid>
          <Row className="mb-4">
            <Col>
              <h1>Incident Management</h1>
              <p className="text-muted">Track and manage security incidents</p>
            </Col>
          </Row>

          {loading ? (
            <Spinner animation="border" />
          ) : (
            <Card>
              <Card.Header>
                <Card.Title className="mb-0">Incidents ({incidents.length})</Card.Title>
              </Card.Header>
              <Card.Body className="p-0">
                <Table hover className="mb-0">
                  <thead>
                    <tr>
                      <th>Incident ID</th>
                      <th>Title</th>
                      <th>Severity</th>
                      <th>Status</th>
                      <th>Affected Systems</th>
                      <th>Assigned To</th>
                    </tr>
                  </thead>
                  <tbody>
                    {incidents.map(incident => (
                      <tr key={incident.id}>
                        <td><code>{incident.incident_id}</code></td>
                        <td>{incident.title}</td>
                        <td>
                          <Badge className={getSeverityBadgeClass(incident.severity)}>
                            {incident.severity}
                          </Badge>
                        </td>
                        <td>
                          <Badge bg={incident.status === 'open' ? 'danger' : 'success'}>
                            {incident.status}
                          </Badge>
                        </td>
                        <td>{incident.affected_systems}</td>
                        <td>{incident.assigned_to}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          )}
        </Container>
      </div>
    </>
  );
}
