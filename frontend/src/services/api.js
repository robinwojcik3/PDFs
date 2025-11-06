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

// Analyse avancée
export const advancedAPI = {
  getBibliography: (documentId) => api.get(`/advanced/${documentId}/bibliography`),
  exportBibliography: (documentId, format = 'bibtex') =>
    api.get(`/advanced/${documentId}/bibliography/export`, { params: { format } }),
  getEquations: (documentId) => api.get(`/advanced/${documentId}/equations`),
  getMethodology: (documentId) => api.get(`/advanced/${documentId}/methodology`),
  compareDocuments: (documentIds) => api.post('/advanced/compare', documentIds),
  getRecommendations: (documentId, limit = 5) =>
    api.get(`/advanced/${documentId}/recommendations`, { params: { limit } }),
  recommendByTopic: (keywords, limit = 5) =>
    api.get('/advanced/recommendations/by-topic', { params: { keywords, limit } }),
  getTrendingTopics: (limit = 10) =>
    api.get('/advanced/recommendations/trending-topics', { params: { limit } }),
  getAuthorNetwork: () => api.get('/advanced/network/authors'),
  exportDocument: (documentId, format = 'markdown', includeAnnotations = true) =>
    api.get(`/advanced/${documentId}/export`, { params: { format, include_annotations: includeAnnotations } }),
  getGlobalStatistics: () => api.get('/advanced/statistics/global'),
};

// Organisation (tags, collections, favoris, historique)
export const organizationAPI = {
  // Tags
  addTag: (documentId, tag, color = null) =>
    api.post(`/organization/tags/${documentId}`, { tag, color }),
  removeTag: (documentId, tag) =>
    api.delete(`/organization/tags/${documentId}/${tag}`),
  getTags: (documentId) => api.get(`/organization/tags/${documentId}`),
  getAllTags: () => api.get('/organization/tags'),
  searchByTags: (tags, matchAll = false) =>
    api.get('/organization/tags/search', { params: { tags, match_all: matchAll } }),
  suggestTags: (documentId) => api.get(`/organization/tags/suggestions/${documentId}`),

  // Catégories
  setCategory: (documentId, categoryType, categoryValue) =>
    api.post(`/organization/categories/${documentId}`, { category_type: categoryType, category_value: categoryValue }),
  getCategories: (documentId) => api.get(`/organization/categories/${documentId}`),
  getPredefinedCategories: () => api.get('/organization/categories/predefined'),
  searchByCategory: (categoryType, categoryValue) =>
    api.get(`/organization/categories/search/${categoryType}/${categoryValue}`),

  // Collections
  createCollection: (name, description = '', color = '#3b82f6', icon = 'folder') =>
    api.post('/organization/collections', { name, description, color, icon }),
  getCollections: () => api.get('/organization/collections'),
  getCollection: (collectionId) => api.get(`/organization/collections/${collectionId}`),
  updateCollection: (collectionId, data) =>
    api.put(`/organization/collections/${collectionId}`, data),
  deleteCollection: (collectionId) =>
    api.delete(`/organization/collections/${collectionId}`),
  addToCollection: (collectionId, documentId) =>
    api.post(`/organization/collections/${collectionId}/documents/${documentId}`),
  removeFromCollection: (collectionId, documentId) =>
    api.delete(`/organization/collections/${collectionId}/documents/${documentId}`),
  getDocumentCollections: (documentId) =>
    api.get(`/organization/collections/document/${documentId}`),

  // Favoris
  addFavorite: (documentId, priority = 3, notes = '') =>
    api.post(`/organization/favorites/${documentId}`, { priority, notes }),
  removeFavorite: (documentId) =>
    api.delete(`/organization/favorites/${documentId}`),
  updateFavorite: (documentId, priority = null, notes = null) =>
    api.put(`/organization/favorites/${documentId}`, { priority, notes }),
  getFavorites: (sortBy = 'priority') =>
    api.get('/organization/favorites', { params: { sort_by: sortBy } }),
  getFavorite: (documentId) => api.get(`/organization/favorites/${documentId}`),
  isFavorite: (documentId) => api.get(`/organization/favorites/${documentId}/check`),

  // Historique
  recordReading: (documentId, page = null, durationSeconds = null) =>
    api.post(`/organization/history/${documentId}`, { page, duration_seconds: durationSeconds }),
  updateProgress: (documentId, currentPage, totalPages) =>
    api.put(`/organization/history/${documentId}/progress`, null, { params: { current_page: currentPage, total_pages: totalPages } }),
  getHistory: (documentId) => api.get(`/organization/history/${documentId}`),
  getAllHistory: (sortBy = 'last_view', limit = null) =>
    api.get('/organization/history', { params: { sort_by: sortBy, limit } }),
  getRecentDocuments: (days = 7, limit = 10) =>
    api.get('/organization/history/recent', { params: { days, limit } }),
  getReadingStatistics: () => api.get('/organization/history/statistics'),
  getReadingByPeriod: (period = 'week') =>
    api.get('/organization/history/statistics/period', { params: { period } }),
  clearHistory: (documentId = null) =>
    documentId ? api.delete(`/organization/history/${documentId}`) : api.delete('/organization/history'),

  // Statistiques
  getStatistics: () => api.get('/organization/statistics'),
};

// Applications pédagogiques interactives
export const learningAPI = {
  getAllInteractions: (documentId, includeMethodology = true) =>
    api.get(`/learning/${documentId}/interactions`, { params: { include_methodology: includeMethodology } }),
  getVisualizations: (documentId) => api.get(`/learning/${documentId}/interactions/visualizations`),
  getSimulations: (documentId) => api.get(`/learning/${documentId}/interactions/simulations`),
  getDiagrams: (documentId) => api.get(`/learning/${documentId}/interactions/diagrams`),
  getExercises: (documentId, difficulty = null) =>
    api.get(`/learning/${documentId}/interactions/exercises`, { params: difficulty ? { difficulty } : {} }),
  getCalculators: (documentId) => api.get(`/learning/${documentId}/interactions/calculators`),
  getTimeline: (documentId) => api.get(`/learning/${documentId}/interactions/timeline`),
  getGraphExplorers: (documentId) => api.get(`/learning/${documentId}/interactions/graph-explorers`),
  getComparisons: (documentId) => api.get(`/learning/${documentId}/interactions/comparisons`),
  getInteractionTypes: () => api.get('/learning/types'),
  createCustomInteraction: (documentId, interactionType, config) =>
    api.post(`/learning/${documentId}/interactions/custom`, null, { params: { interaction_type: interactionType, config } }),
};

// Health check
export const healthCheck = () => api.get('/health');

export default api;
