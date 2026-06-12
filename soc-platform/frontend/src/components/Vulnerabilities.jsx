import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Table, Badge, Button, Modal, Form, Spinner, Alert } from 'react-bootstrap';
import { vulnerabilityService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';
import '../styles/theme.css';

export default function Vulnerabilities() {
  const [vulnerabilities, setVulnerabilities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ severity: '', status: '' });
  const [showModal, setShowModal] = useState(false);
  const [selectedVulnerability, setSelectedVulnerability] = useState(null);
  const [formData, setFormData] = useState({
    cve_id: '',
    title: '',
    cvss_score: '',
    severity: 'Medium',
    status: 'open',
    affected_asset: ''
  });
  const [formErrors, setFormErrors] = useState({});
  const [submitLoading, setSubmitLoading] = useState(false);
  const [submitError, setSubmitError] = useState('');

  useEffect(() => {
    fetchVulnerabilities();
  }, [filter]);

  const resetForm = () => {
    setFormData({
      cve_id: '',
      title: '',
      cvss_score: '',
      severity: 'Medium',
      status: 'open',
      affected_asset: ''
    });
    setFormErrors({});
    setSubmitError('');
  };

  const handleClose = () => {
    setShowModal(false);
    resetForm();
  };

  const handleCloseView = () => {
    setSelectedVulnerability(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.cve_id.trim()) errors.cve_id = 'CVE ID is required';
    if (!formData.title.trim()) errors.title = 'Title is required';
    if (!formData.cvss_score.toString().trim()) {
      errors.cvss_score = 'CVSS score is required';
    } else if (isNaN(Number(formData.cvss_score)) || Number(formData.cvss_score) < 0 || Number(formData.cvss_score) > 10) {
      errors.cvss_score = 'CVSS score must be a number between 0 and 10';
    }
    if (!formData.affected_asset.trim()) errors.affected_asset = 'Affected asset is required';
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const fetchVulnerabilities = async () => {
    try {
      const response = await vulnerabilityService.getVulnerabilities(filter);
      setVulnerabilities(response.data.vulnerabilities);
    } catch (error) {
      console.error('Error fetching vulnerabilities:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateVulnerability = async (e) => {
    e.preventDefault();
    setSubmitError('');

    if (!validateForm()) {
      return;
    }

    setSubmitLoading(true);
    try {
      await vulnerabilityService.createVulnerability({
        cve_id: formData.cve_id,
        title: formData.title,
        cvss_score: Number(formData.cvss_score),
        severity: formData.severity,
        status: formData.status,
        affected_asset: formData.affected_asset,
        description: '',
        remediation: '',
        priority: 5
      });
      handleClose();
      fetchVulnerabilities();
    } catch (error) {
      setSubmitError(error.response?.data?.error || error.message || 'Failed to create vulnerability');
      console.error('Error creating vulnerability:', error);
    } finally {
      setSubmitLoading(false);
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
              <h1>Vulnerability Management</h1>
              <p className="text-muted">Track and manage security vulnerabilities</p>
            </Col>
            <Col md={2} className="text-end">
              <Button variant="primary" onClick={() => setShowModal(true)}>
                Add Vulnerability
              </Button>
            </Col>
          </Row>

          <Row className="mb-4">
            <Col md={3}>
              <Form.Group>
                <Form.Label>Severity</Form.Label>
                <Form.Select 
                  value={filter.severity}
                  onChange={(e) => setFilter({...filter, severity: e.target.value})}
                >
                  <option value="">All</option>
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group>
                <Form.Label>Status</Form.Label>
                <Form.Select 
                  value={filter.status}
                  onChange={(e) => setFilter({...filter, status: e.target.value})}
                >
                  <option value="">All</option>
                  <option value="open">Open</option>
                  <option value="mitigated">Mitigated</option>
                  <option value="resolved">Resolved</option>
                </Form.Select>
              </Form.Group>
            </Col>
          </Row>

          <Modal show={showModal} onHide={handleClose} centered>
            <Modal.Header closeButton>
              <Modal.Title>Add Vulnerability</Modal.Title>
            </Modal.Header>
            <Form onSubmit={handleCreateVulnerability}>
              <Modal.Body>
                {submitError && (
                  <Alert variant="danger">{submitError}</Alert>
                )}
                <Form.Group className="mb-3" controlId="cveId">
                  <Form.Label>CVE ID</Form.Label>
                  <Form.Control
                    name="cve_id"
                    type="text"
                    value={formData.cve_id}
                    onChange={handleChange}
                    isInvalid={!!formErrors.cve_id}
                    placeholder="CVE-2025-12345"
                  />
                  <Form.Control.Feedback type="invalid">
                    {formErrors.cve_id}
                  </Form.Control.Feedback>
                </Form.Group>

                <Form.Group className="mb-3" controlId="title">
                  <Form.Label>Title</Form.Label>
                  <Form.Control
                    name="title"
                    type="text"
                    value={formData.title}
                    onChange={handleChange}
                    isInvalid={!!formErrors.title}
                    placeholder="Vulnerability title"
                  />
                  <Form.Control.Feedback type="invalid">
                    {formErrors.title}
                  </Form.Control.Feedback>
                </Form.Group>

                <Row className="g-3">
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="cvssScore">
                      <Form.Label>CVSS Score</Form.Label>
                      <Form.Control
                        name="cvss_score"
                        type="number"
                        min="0"
                        max="10"
                        step="0.1"
                        value={formData.cvss_score}
                        onChange={handleChange}
                        isInvalid={!!formErrors.cvss_score}
                        placeholder="7.5"
                      />
                      <Form.Control.Feedback type="invalid">
                        {formErrors.cvss_score}
                      </Form.Control.Feedback>
                    </Form.Group>
                  </Col>

                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="affectedAsset">
                      <Form.Label>Affected Asset</Form.Label>
                      <Form.Control
                        name="affected_asset"
                        type="text"
                        value={formData.affected_asset}
                        onChange={handleChange}
                        isInvalid={!!formErrors.affected_asset}
                        placeholder="Asset name or identifier"
                      />
                      <Form.Control.Feedback type="invalid">
                        {formErrors.affected_asset}
                      </Form.Control.Feedback>
                    </Form.Group>
                  </Col>
                </Row>

                <Row className="g-3">
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="severity">
                      <Form.Label>Severity</Form.Label>
                      <Form.Select
                        name="severity"
                        value={formData.severity}
                        onChange={handleChange}
                      >
                        <option value="Critical">Critical</option>
                        <option value="High">High</option>
                        <option value="Medium">Medium</option>
                        <option value="Low">Low</option>
                      </Form.Select>
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3" controlId="status">
                      <Form.Label>Status</Form.Label>
                      <Form.Select
                        name="status"
                        value={formData.status}
                        onChange={handleChange}
                      >
                        <option value="open">Open</option>
                        <option value="mitigated">Mitigated</option>
                        <option value="resolved">Resolved</option>
                      </Form.Select>
                    </Form.Group>
                  </Col>
                </Row>
              </Modal.Body>
              <Modal.Footer>
                <Button variant="secondary" onClick={handleClose} disabled={submitLoading}>
                  Cancel
                </Button>
                <Button type="submit" variant="primary" disabled={submitLoading}>
                  {submitLoading ? 'Creating...' : 'Create Vulnerability'}
                </Button>
              </Modal.Footer>
            </Form>
          </Modal>

          <Modal show={!!selectedVulnerability} onHide={handleCloseView} centered>
            <Modal.Header closeButton>
              <Modal.Title>Vulnerability Details</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              {selectedVulnerability && (
                <div>
                  <p><strong>CVE ID:</strong> {selectedVulnerability.cve_id}</p>
                  <p><strong>Title:</strong> {selectedVulnerability.title}</p>
                  <p><strong>CVSS Score:</strong> {selectedVulnerability.cvss_score}</p>
                  <p><strong>Severity:</strong> {selectedVulnerability.severity}</p>
                  <p><strong>Status:</strong> {selectedVulnerability.status}</p>
                  <p><strong>Affected Asset:</strong> {selectedVulnerability.affected_asset}</p>
                </div>
              )}
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={handleCloseView}>
                Close
              </Button>
            </Modal.Footer>
          </Modal>

          {loading ? (
            <div className="text-center">
              <Spinner animation="border" />
            </div>
          ) : (
            <Card>
              <Card.Header>
                <Card.Title className="mb-0">Vulnerabilities ({vulnerabilities.length})</Card.Title>
              </Card.Header>
              <Card.Body className="p-0">
                <Table hover className="mb-0">
                  <thead>
                    <tr>
                      <th>CVE ID</th>
                      <th>Title</th>
                      <th>CVSS</th>
                      <th>Severity</th>
                      <th>Status</th>
                      <th>Asset</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {vulnerabilities.map(vuln => (
                      <tr key={vuln.id}>
                        <td><code>{vuln.cve_id}</code></td>
                        <td>{vuln.title}</td>
                        <td><strong>{vuln.cvss_score}</strong></td>
                        <td>
                          <Badge className={getSeverityBadgeClass(vuln.severity)}>
                            {vuln.severity}
                          </Badge>
                        </td>
                        <td>
                          <Badge bg={vuln.status === 'open' ? 'danger' : 'success'}>
                            {vuln.status}
                          </Badge>
                        </td>
                        <td>{vuln.affected_asset}</td>
                        <td>
                          <Button variant="outline-primary" size="sm" onClick={() => setSelectedVulnerability(vuln)}>
                            View
                          </Button>
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
