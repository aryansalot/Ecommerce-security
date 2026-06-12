import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Spinner } from 'react-bootstrap';
import { mitreService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';

export default function MITRE() {
  const [matrix, setMatrix] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMatrix();
  }, []);

  const fetchMatrix = async () => {
    try {
      const response = await mitreService.getMatrix();
      setMatrix(response.data);
    } catch (error) {
      console.error('Error fetching MITRE matrix:', error);
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
              <h1>MITRE ATT&CK Framework</h1>
              <p className="text-muted">Attack techniques and tactics mapping</p>
            </Col>
          </Row>

          {loading ? (
            <Spinner animation="border" />
          ) : (
            <Row>
              {matrix && Object.entries(matrix).map(([tactic, data]) => (
                <Col md={6} lg={4} key={tactic} className="mb-4">
                  <Card>
                    <Card.Header>
                      <Card.Title className="mb-0">{tactic}</Card.Title>
                    </Card.Header>
                    <Card.Body>
                      <div className="mb-3">
                        <div><strong>Total Techniques:</strong> {data.count}</div>
                        <div><strong>Detected:</strong> {data.detected}</div>
                      </div>
                      <Table size="sm" className="mb-0">
                        <tbody>
                          {data.techniques.slice(0, 3).map(tech => (
                            <tr key={tech.id}>
                              <td>
                                <small>{tech.technique_id}</small>
                              </td>
                              <td>
                                <small>{tech.technique}</small>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </Table>
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
