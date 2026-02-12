import api from './api';

export const getDashboardStats = async (params = {}) => {
  return api.get('/dashboard/stats', { params });
};

export const getDashboardData = async (params = {}) => {
  return api.get('/dashboard', { params });
};

export const getRecentActivity = async (params = {}) => {
  return api.get('/dashboard/activity', { params });
};

export const getAssetBreakdown = async (params = {}) => {
  return api.get('/dashboard/assets/breakdown', { params });
};

export const getStatusDistribution = async (params = {}) => {
  return api.get('/dashboard/status/distribution', { params });
};

export const getRiskSummary = async (params = {}) => {
  return api.get('/dashboard/risk/summary', { params });
};

export const getTopRisks = async (params = {}) => {
  return api.get('/dashboard/risk/top', { params });
};

export const getComplianceScore = async (params = {}) => {
  return api.get('/dashboard/compliance/score', { params });
};

export const getEngagementMetrics = async (params = {}) => {
  return api.get('/dashboard/engagements/metrics', { params });
};

export const getAuditMetrics = async (params = {}) => {
  return api.get('/dashboard/audits/metrics', { params });
};

export const getAssetMetrics = async (params = {}) => {
  return api.get('/dashboard/assets/metrics', { params });
};

export const getTimelineData = async (params = {}) => {
  return api.get('/dashboard/timeline', { params });
};

export const getNotifications = async (params = {}) => {
  return api.get('/dashboard/notifications', { params });
};

export const markNotificationAsRead = async (notificationId) => {
  return api.put(`/dashboard/notifications/${notificationId}/read`);
};

export const markAllNotificationsAsRead = async () => {
  return api.post('/dashboard/notifications/mark-all-read');
};

export const dismissNotification = async (notificationId) => {
  return api.delete(`/dashboard/notifications/${notificationId}`);
};

export const getAlerts = async (params = {}) => {
  return api.get('/dashboard/alerts', { params });
};

export const acknowledgeAlert = async (alertId) => {
  return api.post(`/dashboard/alerts/${alertId}/acknowledge`);
};

export const getFavorites = async () => {
  return api.get('/dashboard/favorites');
};

export const addFavorite = async (itemId, itemType) => {
  return api.post('/dashboard/favorites', { itemId, itemType });
};

export const removeFavorite = async (itemId) => {
  return api.delete(`/dashboard/favorites/${itemId}`);
};

export const getCustomDashboard = async (dashboardId) => {
  return api.get(`/dashboard/custom/${dashboardId}`);
};

export const createCustomDashboard = async (dashboardData) => {
  return api.post('/dashboard/custom', dashboardData);
};

export const updateCustomDashboard = async (dashboardId, dashboardData) => {
  return api.put(`/dashboard/custom/${dashboardId}`, dashboardData);
};

export const deleteCustomDashboard = async (dashboardId) => {
  return api.delete(`/dashboard/custom/${dashboardId}`);
};

export const getPerformanceMetrics = async (params = {}) => {
  return api.get('/dashboard/performance', { params });
};

export const getSystemHealth = async () => {
  return api.get('/dashboard/system-health');
};

export const getWorkloadDistribution = async (params = {}) => {
  return api.get('/dashboard/workload', { params });
};

export const getAuditProgress = async (params = {}) => {
  return api.get('/dashboard/audit-progress', { params });
};

export const getKeyMetrics = async (params = {}) => {
  return api.get('/dashboard/key-metrics', { params });
};
