/**
 * Service API pour communiquer avec le backend FastAPI.
 */
import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Documents
export const documentsAPI = {
  list: () => api.get('/documents/'),
  get: (documentId) => api.get(`/documents/${documentId}`),
  index: () => api.post('/documents/index'),
  indexSingle: (filename) => api.post(`/documents/index/${filename}`),
  getSections: (documentId) => api.get(`/documents/${documentId}/sections`),
  getFigures: (documentId) => api.get(`/documents/${documentId}/figures`),
  getTables: (documentId) => api.get(`/documents/${documentId}/tables`),
};

// Recherche
export const searchAPI = {
  search: (query, limit = 20) => api.get('/search/', { params: { q: query, limit } }),
  suggestions: (query, limit = 5) => api.get('/search/suggestions', { params: { q: query, limit } }),
  reindex: () => api.post('/search/reindex'),
};

// Annotations
export const annotationsAPI = {
  create: (data) => api.post('/annotations/', data),
  list: (documentId, page = null) =>
    api.get(`/annotations/${documentId}`, { params: page ? { page } : {} }),
  get: (documentId, annotationId) =>
    api.get(`/annotations/${documentId}/${annotationId}`),
  update: (documentId, annotationId, data) =>
    api.put(`/annotations/${documentId}/${annotationId}`, data),
  delete: (documentId, annotationId) =>
    api.delete(`/annotations/${documentId}/${annotationId}`),
  export: (documentId) => api.get(`/annotations/${documentId}/export`),
};

// Modules interactifs
export const interactiveAPI = {
  getConcepts: (documentId) => api.get(`/interactive/${documentId}/concepts`),
  getQuiz: (documentId) => api.get(`/interactive/${documentId}/quiz`),
  getSummary: (documentId) => api.get(`/interactive/${documentId}/summary`),
  getStatistics: (documentId) => api.get(`/interactive/${documentId}/statistics`),
};

// Health check
export const healthCheck = () => api.get('/health');

export default api;
