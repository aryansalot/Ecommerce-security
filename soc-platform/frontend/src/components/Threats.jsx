import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Spinner } from 'react-bootstrap';
import { threatService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';

export default function Threats() {
  const [threats, setThreats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchThreats();
  }, []);

  const fetchThreats = async () => {
    try {
      const response = await threatService.getThreats({});
      setThreats(response.data.threats);
    } catch (error) {
      console.error('Error fetching threats:', error);
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
              <h1>Threat Intelligence</h1>
              <p className="text-muted">Monitor threats and IOCs</p>
            </Col>
          </Row>

          {loading ? (
            <Spinner animation="border" />
          ) : (
            <Card>
              <Card.Header>
                <Card.Title className="mb-0">Active Threats ({threats.length})</Card.Title>
              </Card.Header>
              <Card.Body className="p-0">
                <Table hover className="mb-0">
                  <thead>
                    <tr>
                      <th>Threat Name</th>
                      <th>Type</th>
                      <th>IOC</th>
                      <th>Severity</th>
                      <th>Confidence</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {threats.map(threat => (
                      <tr key={threat.id}>
                        <td>{threat.threat_name}</td>
                        <td>{threat.threat_type}</td>
                        <td><code>{threat.ioc_value}</code></td>
                        <td>
                          <Badge className={getSeverityBadgeClass(threat.severity)}>
                            {threat.severity}
                          </Badge>
                        </td>
                        <td>{threat.confidence}%</td>
                        <td>
                          <Badge bg={threat.status === 'active' ? 'danger' : 'success'}>
                            {threat.status}
                          </Badge>
                        </td>
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
