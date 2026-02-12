import api from './api';

export const getReports = async (params = {}) => {
  return api.get('/reports', { params });
};

export const getReportById = async (id) => {
  return api.get(`/reports/${id}`);
};

export const createReport = async (reportData) => {
  return api.post('/reports', reportData);
};

export const updateReport = async (id, reportData) => {
  return api.put(`/reports/${id}`, reportData);
};

export const deleteReport = async (id) => {
  return api.delete(`/reports/${id}`);
};

export const publishReport = async (id) => {
  return api.post(`/reports/${id}/publish`);
};

export const approveReport = async (id, approvalData) => {
  return api.post(`/reports/${id}/approve`, approvalData);
};

export const rejectReport = async (id, rejectionData) => {
  return api.post(`/reports/${id}/reject`, rejectionData);
};

export const archiveReport = async (id) => {
  return api.post(`/reports/${id}/archive`);
};

export const generateReport = async (engagementId, reportType, params = {}) => {
  return api.post(`/reports/generate`, { engagementId, reportType, ...params });
};

export const getReportTemplate = async (reportType) => {
  return api.get(`/reports/templates/${reportType}`);
};

export const getReportTemplates = async () => {
  return api.get('/reports/templates');
};

export const getReportContent = async (id) => {
  return api.get(`/reports/${id}/content`);
};

export const updateReportContent = async (id, content) => {
  return api.put(`/reports/${id}/content`, { content });
};

export const getReportAttachments = async (id) => {
  return api.get(`/reports/${id}/attachments`);
};

export const uploadReportAttachment = async (id, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/reports/${id}/attachments`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const deleteReportAttachment = async (id, attachmentId) => {
  return api.delete(`/reports/${id}/attachments/${attachmentId}`);
};

export const downloadReport = async (id, format = 'pdf') => {
  return api.get(`/reports/${id}/download`, { params: { format }, responseType: 'blob' });
};

export const exportReport = async (id, format = 'pdf') => {
  return api.get(`/reports/${id}/export`, { params: { format }, responseType: 'blob' });
};

export const getReportComments = async (id, params = {}) => {
  return api.get(`/reports/${id}/comments`, { params });
};

export const addReportComment = async (id, commentData) => {
  return api.post(`/reports/${id}/comments`, commentData);
};

export const updateReportComment = async (id, commentId, commentData) => {
  return api.put(`/reports/${id}/comments/${commentId}`, commentData);
};

export const deleteReportComment = async (id, commentId) => {
  return api.delete(`/reports/${id}/comments/${commentId}`);
};

export const getReportHistory = async (id, params = {}) => {
  return api.get(`/reports/${id}/history`, { params });
};

export const getReportStatus = async (id) => {
  return api.get(`/reports/${id}/status`);
};

export const scheduleReportGeneration = async (engagementId, reportType, schedule) => {
  return api.post('/reports/schedule', { engagementId, reportType, schedule });
};

export const getScheduledReports = async (params = {}) => {
  return api.get('/reports/scheduled', { params });
};

export const cancelScheduledReport = async (scheduleId) => {
  return api.delete(`/reports/scheduled/${scheduleId}`);
};

export const sendReportViaEmail = async (id, recipients) => {
  return api.post(`/reports/${id}/send-email`, { recipients });
};

export const shareReport = async (id, sharedWith, permissions = []) => {
  return api.post(`/reports/${id}/share`, { sharedWith, permissions });
};

export const getReportShares = async (id) => {
  return api.get(`/reports/${id}/shares`);
};

export const revokeReportShare = async (id, shareId) => {
  return api.delete(`/reports/${id}/shares/${shareId}`);
};
