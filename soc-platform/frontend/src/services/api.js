import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const getToken = () => {
  if (typeof window === 'undefined') {
    return null;
  }
  return localStorage.getItem('token');
};

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

apiClient.interceptors.request.use((config) => {
  const token = getToken();
  config.headers = config.headers || {};
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: (username, password) =>
    apiClient.post('/auth/login', { username, password }),
  register: (data) =>
    apiClient.post('/auth/register', data),
  getProfile: () =>
    apiClient.get('/auth/profile'),
  getUsers: () =>
    apiClient.get('/auth/users')
};

export const dashboardService = {
  getOverview: () =>
    apiClient.get('/dashboard/overview'),
  getHealth: () =>
    apiClient.get('/dashboard/health'),
  getMetrics: () =>
    apiClient.get('/dashboard/metrics'),
  getTimeline: () =>
    apiClient.get('/dashboard/timeline')
};

export const vulnerabilityService = {
  getVulnerabilities: (params) =>
    apiClient.get('/vulnerabilities', { params }),
  getVulnerability: (id) =>
    apiClient.get(`/vulnerabilities/${id}`),
  createVulnerability: (data) =>
    apiClient.post('/vulnerabilities', data),
  updateVulnerability: (id, data) =>
    apiClient.put(`/vulnerabilities/${id}`, data),
  deleteVulnerability: (id) =>
    apiClient.delete(`/vulnerabilities/${id}`),
  getStatistics: () =>
    apiClient.get('/vulnerabilities/statistics')
};

export const incidentService = {
  getIncidents: (params) =>
    apiClient.get('/incidents', { params }),
  getIncident: (id) =>
    apiClient.get(`/incidents/${id}`),
  createIncident: (data) =>
    apiClient.post('/incidents', data),
  updateIncident: (id, data) =>
    apiClient.put(`/incidents/${id}`, data),
  getStatistics: () =>
    apiClient.get('/incidents/statistics')
};

export const threatService = {
  getThreats: (params) =>
    apiClient.get('/threats', { params }),
  getThreat: (id) =>
    apiClient.get(`/threats/${id}`),
  createThreat: (data) =>
    apiClient.post('/threats', data),
  updateThreat: (id, data) =>
    apiClient.put(`/threats/${id}`, data),
  getIOCs: () =>
    apiClient.get('/threats/iocs'),
  getStatistics: () =>
    apiClient.get('/threats/statistics')
};

export const alertService = {
  getAlerts: (params) =>
    apiClient.get('/alerts', { params }),
  getAlert: (id) =>
    apiClient.get(`/alerts/${id}`),
  acknowledgeAlert: (id) =>
    apiClient.put(`/alerts/${id}/acknowledge`),
  resolveAlert: (id) =>
    apiClient.put(`/alerts/${id}/resolve`),
  getStatistics: () =>
    apiClient.get('/alerts/statistics')
};

export const complianceService = {
  getCompliance: (params) =>
    apiClient.get('/compliance', { params }),
  getFrameworks: () =>
    apiClient.get('/compliance/frameworks'),
  getOverall: () =>
    apiClient.get('/compliance/overall'),
  getMatrix: () =>
    apiClient.get('/compliance/matrix')
};

export const mitreService = {
  getTechniques: (params) =>
    apiClient.get('/mitre/techniques', { params }),
  getTactics: () =>
    apiClient.get('/mitre/tactics'),
  getMatrix: () =>
    apiClient.get('/mitre/matrix'),
  getDetections: () =>
    apiClient.get('/mitre/detections')
};

export const assetService = {
  getAssets: (params) =>
    apiClient.get('/assets', { params }),
  getAsset: (id) =>
    apiClient.get(`/assets/${id}`),
  createAsset: (data) =>
    apiClient.post('/assets', data),
  updateAsset: (id, data) =>
    apiClient.put(`/assets/${id}`, data),
  getStatistics: () =>
    apiClient.get('/assets/statistics')
};

export const riskService = {
  getRiskScore: () =>
    apiClient.get('/risk/score'),
  getHeatmap: () =>
    apiClient.get('/risk/heatmap'),
  getScorecard: () =>
    apiClient.get('/risk/scorecard'),
  getAssetRisk: (id) =>
    apiClient.get(`/risk/asset/${id}`)
};

export default apiClient;
