import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';
import { riskService } from '../services/api';
import Sidebar from './Sidebar';
import TopNavbar from './TopNavbar';

export default function RiskAnalysis() {
  const [data, setData] = useState(null);
  const [scorecard, setScorecard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRiskData();
  }, []);

  const fetchRiskData = async () => {
    try {
      const [riskResponse, scorecardResponse] = await Promise.all([
        riskService.getRiskScore(),
        riskService.getScorecard()
      ]);
      setData(riskResponse.data);
      setScorecard(scorecardResponse.data);
    } catch (error) {
      console.error('Error fetching risk data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 80) return '#e94560';
    if (score >= 60) return '#ff6b6b';
    if (score >= 40) return '#ffa502';
    return '#51cf66';
  };

  if (loading) {
    return (
      <>
        <TopNavbar />
        <Sidebar />
        <div className="main-content">
          <Spinner animation="border" />
        </div>
      </>
    );
  }

  return (
    <>
      <TopNavbar />
      <Sidebar />
      <div className="main-content">
        <Container fluid>
          <Row className="mb-4">
            <Col>
              <h1>Risk Analysis & Scoring</h1>
              <p className="text-muted">AI-powered organizational risk assessment</p>
            </Col>
          </Row>

          <Row className="mb-4">
            <Col md={6}>
              <Card>
                <Card.Header>
                  <Card.Title className="mb-0">Overall Risk Score</Card.Title>
                </Card.Header>
                <Card.Body>
                  <div style={{textAlign: 'center', padding: '20px'}}>
                    <div style={{
                      fontSize: '64px',
                      fontWeight: 'bold',
                      color: getRiskColor(data?.risk_score),
                      marginBottom: '10px'
                    }}>
                      {Math.round(data?.risk_score)}%
                    </div>
                    <Alert variant={data?.risk_level === 'Critical' ? 'danger' : 'warning'} className="mb-0">
                      <strong>Risk Level: {data?.risk_level}</strong>
                    </Alert>
                  </div>
                </Card.Body>
              </Card>
            </Col>

            <Col md={6}>
              <Card>
                <Card.Header>
                  <Card.Title className="mb-0">Security Scorecard</Card.Title>
                </Card.Header>
                <Card.Body>
                  {scorecard && (
                    <div>
                      <div className="mb-3">
                        <small className="text-muted">Overall Score</small>
                        <div className="h5">{Math.round(scorecard.overall_score)}%</div>
                      </div>
                      <div className="mb-3">
                        <small className="text-muted">Security Maturity</small>
                        <div className="h5">{Math.round(scorecard.security_maturity)}%</div>
                      </div>
                      <div className="mb-3">
                        <small className="text-muted">Compliance Readiness</small>
                        <div className="h5">{Math.round(scorecard.compliance_readiness)}%</div>
                      </div>
                      <div>
                        <small className="text-muted">Asset Health</small>
                        <div className="h5">{Math.round(scorecard.asset_health)}%</div>
                      </div>
                    </div>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>

          {data?.recommendations && (
            <Card>
              <Card.Header>
                <Card.Title className="mb-0">Recommendations</Card.Title>
              </Card.Header>
              <Card.Body>
                <ul>
                  {data.recommendations.map((rec, idx) => (
                    <li key={idx} className="mb-2">{rec}</li>
                  ))}
                </ul>
              </Card.Body>
            </Card>
          )}
        </Container>
      </div>
    </>
  );
}
