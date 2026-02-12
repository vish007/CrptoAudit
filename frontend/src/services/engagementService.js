import api from './api';

export const getEngagements = async (params = {}) => {
  return api.get('/engagements', { params });
};

export const getEngagementById = async (id) => {
  return api.get(`/engagements/${id}`);
};

export const createEngagement = async (engagementData) => {
  return api.post('/engagements', engagementData);
};

export const updateEngagement = async (id, engagementData) => {
  return api.put(`/engagements/${id}`, engagementData);
};

export const deleteEngagement = async (id) => {
  return api.delete(`/engagements/${id}`);
};

export const getEngagementStatus = async (id) => {
  return api.get(`/engagements/${id}/status`);
};

export const updateEngagementStatus = async (id, status) => {
  return api.patch(`/engagements/${id}/status`, { status });
};

export const getEngagementProgress = async (id) => {
  return api.get(`/engagements/${id}/progress`);
};

export const getEngagementAssets = async (id, params = {}) => {
  return api.get(`/engagements/${id}/assets`, { params });
};

export const submitEngagementAsset = async (id, assetData) => {
  return api.post(`/engagements/${id}/assets`, assetData);
};

export const getEngagementAudit = async (id) => {
  return api.get(`/engagements/${id}/audit`);
};

export const startEngagementAudit = async (id) => {
  return api.post(`/engagements/${id}/audit/start`);
};

export const getEngagementMerkleTree = async (id) => {
  return api.get(`/engagements/${id}/merkle-tree`);
};

export const submitEngagementMerkleTree = async (id, merkleData) => {
  return api.post(`/engagements/${id}/merkle-tree`, merkleData);
};

export const getEngagementBlockchainData = async (id) => {
  return api.get(`/engagements/${id}/blockchain`);
};

export const submitBlockchainVerification = async (id, blockchainData) => {
  return api.post(`/engagements/${id}/blockchain`, blockchainData);
};

export const getEngagementReports = async (id, params = {}) => {
  return api.get(`/engagements/${id}/reports`, { params });
};

export const getEngagementComments = async (id, params = {}) => {
  return api.get(`/engagements/${id}/comments`, { params });
};

export const addEngagementComment = async (id, commentData) => {
  return api.post(`/engagements/${id}/comments`, commentData);
};

export const getEngagementTeam = async (id) => {
  return api.get(`/engagements/${id}/team`);
};

export const addEngagementTeamMember = async (id, userId, role) => {
  return api.post(`/engagements/${id}/team`, { userId, role });
};

export const removeEngagementTeamMember = async (id, userId) => {
  return api.delete(`/engagements/${id}/team/${userId}`);
};

export const getEngagementTimeline = async (id) => {
  return api.get(`/engagements/${id}/timeline`);
};

export const getEngagementRiskAssessment = async (id) => {
  return api.get(`/engagements/${id}/risk-assessment`);
};

export const updateEngagementRiskAssessment = async (id, riskData) => {
  return api.put(`/engagements/${id}/risk-assessment`, riskData);
};

export const getEngagementDocuments = async (id, params = {}) => {
  return api.get(`/engagements/${id}/documents`, { params });
};

export const uploadEngagementDocument = async (id, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/engagements/${id}/documents`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteEngagementDocument = async (id, documentId) => {
  return api.delete(`/engagements/${id}/documents/${documentId}`);
};
