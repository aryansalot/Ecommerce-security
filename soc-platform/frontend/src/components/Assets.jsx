import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Spinner, ProgressBar } from 'react-bootstrap';
import { assetService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';

export default function Assets() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAssets();
  }, []);

  const fetchAssets = async () => {
    try {
      const response = await assetService.getAssets({});
      setAssets(response.data.assets);
    } catch (error) {
      console.error('Error fetching assets:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCriticalityBadgeClass = (criticality) => {
    const classes = {
      'Critical': 'badge-critical',
      'High': 'badge-high',
      'Medium': 'badge-medium',
      'Low': 'badge-low'
    };
    return classes[criticality] || 'badge-secondary';
  };

  return (
    <>
      <TopNavbar />
      <Sidebar />
      <div className="main-content">
        <Container fluid>
          <Row className="mb-4">
            <Col>
              <h1>Asset Inventory</h1>
              <p className="text-muted">Track and manage organizational assets</p>
            </Col>
          </Row>

          {loading ? (
            <Spinner animation="border" />
          ) : (
            <Card>
              <Card.Header>
                <Card.Title className="mb-0">Assets ({assets.length})</Card.Title>
              </Card.Header>
              <Card.Body className="p-0">
                <Table hover className="mb-0">
                  <thead>
                    <tr>
                      <th>Asset Name</th>
                      <th>Type</th>
                      <th>IP Address</th>
                      <th>OS</th>
                      <th>Criticality</th>
                      <th>Vulnerabilities</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {assets.map(asset => (
                      <tr key={asset.id}>
                        <td>{asset.asset_name}</td>
                        <td>{asset.asset_type}</td>
                        <td><code>{asset.ip_address}</code></td>
                        <td>{asset.os}</td>
                        <td>
                          <Badge className={getCriticalityBadgeClass(asset.criticality)}>
                            {asset.criticality}
                          </Badge>
                        </td>
                        <td>
                          <Badge bg={asset.vulnerabilities > 0 ? 'warning' : 'success'}>
                            {asset.vulnerabilities}
                          </Badge>
                        </td>
                        <td>
                          <Badge bg={asset.status === 'active' ? 'success' : 'secondary'}>
                            {asset.status}
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
