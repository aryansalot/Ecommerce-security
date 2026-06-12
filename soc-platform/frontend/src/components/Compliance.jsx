import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Spinner, ProgressBar } from 'react-bootstrap';
import { complianceService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';

export default function Compliance() {
  const [matrix, setMatrix] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCompliance();
  }, []);

  const fetchCompliance = async () => {
    try {
      const response = await complianceService.getMatrix();
      setMatrix(response.data);
    } catch (error) {
      console.error('Error fetching compliance:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <TopNavbar />
      <Sidebar />
      <div className="main-content">
        <Container fluid>
          <Row className="mb-4">
            <Col>
              <h1>Compliance Dashboard</h1>
              <p className="text-muted">Track framework compliance status</p>
            </Col>
          </Row>

          {loading ? (
            <Spinner animation="border" />
          ) : (
            <Row>
              {matrix && Object.entries(matrix).map(([framework, data]) => (
                <Col md={6} lg={4} key={framework} className="mb-4">
                  <Card>
                    <Card.Header>
                      <Card.Title className="mb-0">{framework}</Card.Title>
                    </Card.Header>
                    <Card.Body>
                      <Row className="mb-3">
                        <Col xs={6}>
                          <small className="text-muted">Compliant</small>
                          <div className="h5">{data.compliant}/{data.total}</div>
                        </Col>
                        <Col xs={6} className="text-end">
                          <small className="text-muted">Score</small>
                          <div className="h5">{Math.round(data.score)}%</div>
                        </Col>
                      </Row>
                      <ProgressBar 
                        now={data.score} 
                        label={`${Math.round(data.score)}%`}
                      />
                      <div className="mt-3 small">
                        <div>Non-compliant: {data.non_compliant}</div>
                        <div>In Progress: {data.in_progress}</div>
                      </div>
                    </Card.Body>
                  </Card>
                </Col>
              ))}
            </Row>
          )}
        </Container>
      </div>
    </>
  );
}
