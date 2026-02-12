import api from './api';

export const getAssets = async (params = {}) => {
  return api.get('/assets', { params });
};

export const getAssetById = async (id) => {
  return api.get(`/assets/${id}`);
};

export const createAsset = async (assetData) => {
  return api.post('/assets', assetData);
};

export const updateAsset = async (id, assetData) => {
  return api.put(`/assets/${id}`, assetData);
};

export const deleteAsset = async (id) => {
  return api.delete(`/assets/${id}`);
};

export const verifyAsset = async (id, verificationData) => {
  return api.post(`/assets/${id}/verify`, verificationData);
};

export const rejectAsset = async (id, reason) => {
  return api.post(`/assets/${id}/reject`, { reason });
};

export const getAssetVerificationHistory = async (id) => {
  return api.get(`/assets/${id}/verification-history`);
};

export const getAssetTransactions = async (id, params = {}) => {
  return api.get(`/assets/${id}/transactions`, { params });
};

export const getAssetBlockchainData = async (id) => {
  return api.get(`/assets/${id}/blockchain-data`);
};

export const getAssetValuation = async (id) => {
  return api.get(`/assets/${id}/valuation`);
};

export const getAssetRiskAssessment = async (id) => {
  return api.get(`/assets/${id}/risk-assessment`);
};

export const bulkVerifyAssets = async (assetIds, verificationData) => {
  return api.post('/assets/bulk-verify', { assetIds, verificationData });
};

export const bulkRejectAssets = async (assetIds, reason) => {
  return api.post('/assets/bulk-reject', { assetIds, reason });
};

export const exportAssets = async (params = {}) => {
  return api.get('/assets/export', { params, responseType: 'blob' });
};

export const importAssets = async (file, engagementId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('engagementId', engagementId);
  return api.post('/assets/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getAssetTypes = async () => {
  return api.get('/assets/types');
};

export const getAssetStatuses = async () => {
  return api.get('/assets/statuses');
};

export const getAssetSummary = async (params = {}) => {
  return api.get('/assets/summary', { params });
};

export const getAssetBreakdown = async (params = {}) => {
  return api.get('/assets/breakdown', { params });
};

export const reconcileAssets = async (engagementId, reconciliationData) => {
  return api.post(`/assets/reconcile/${engagementId}`, reconciliationData);
};

export const getReconciliationReport = async (engagementId) => {
  return api.get(`/assets/reconciliation-report/${engagementId}`);
};
