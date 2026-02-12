import api from './api';

// User Management
export const getUsers = async (params = {}) => {
  return api.get('/admin/users', { params });
};

export const getUserById = async (id) => {
  return api.get(`/admin/users/${id}`);
};

export const createUser = async (userData) => {
  return api.post('/admin/users', userData);
};

export const updateUser = async (id, userData) => {
  return api.put(`/admin/users/${id}`, userData);
};

export const deleteUser = async (id) => {
  return api.delete(`/admin/users/${id}`);
};

export const activateUser = async (id) => {
  return api.post(`/admin/users/${id}/activate`);
};

export const deactivateUser = async (id) => {
  return api.post(`/admin/users/${id}/deactivate`);
};

export const resetUserPassword = async (id) => {
  return api.post(`/admin/users/${id}/reset-password`);
};

export const assignUserRole = async (id, role) => {
  return api.post(`/admin/users/${id}/assign-role`, { role });
};

export const revokeUserRole = async (id, role) => {
  return api.post(`/admin/users/${id}/revoke-role`, { role });
};

// Tenant Management
export const getTenants = async (params = {}) => {
  return api.get('/admin/tenants', { params });
};

export const getTenantById = async (id) => {
  return api.get(`/admin/tenants/${id}`);
};

export const createTenant = async (tenantData) => {
  return api.post('/admin/tenants', tenantData);
};

export const updateTenant = async (id, tenantData) => {
  return api.put(`/admin/tenants/${id}`, tenantData);
};

export const deleteTenant = async (id) => {
  return api.delete(`/admin/tenants/${id}`);
};

export const activateTenant = async (id) => {
  return api.post(`/admin/tenants/${id}/activate`);
};

export const deactivateTenant = async (id) => {
  return api.post(`/admin/tenants/${id}/deactivate`);
};

export const getTenantUsers = async (id, params = {}) => {
  return api.get(`/admin/tenants/${id}/users`, { params });
};

export const getTenantSettings = async (id) => {
  return api.get(`/admin/tenants/${id}/settings`);
};

export const updateTenantSettings = async (id, settings) => {
  return api.put(`/admin/tenants/${id}/settings`, settings);
};

// Audit Logs
export const getAuditLogs = async (params = {}) => {
  return api.get('/admin/audit-logs', { params });
};

export const getAuditLogById = async (id) => {
  return api.get(`/admin/audit-logs/${id}`);
};

export const exportAuditLogs = async (params = {}) => {
  return api.get('/admin/audit-logs/export', { params, responseType: 'blob' });
};

// System Settings
export const getSystemSettings = async () => {
  return api.get('/admin/settings');
};

export const updateSystemSettings = async (settings) => {
  return api.put('/admin/settings', settings);
};

export const getEmailSettings = async () => {
  return api.get('/admin/settings/email');
};

export const updateEmailSettings = async (emailSettings) => {
  return api.put('/admin/settings/email', emailSettings);
};

export const getSecuritySettings = async () => {
  return api.get('/admin/settings/security');
};

export const updateSecuritySettings = async (securitySettings) => {
  return api.put('/admin/settings/security', securitySettings);
};

// Roles and Permissions
export const getRoles = async () => {
  return api.get('/admin/roles');
};

export const getRoleById = async (id) => {
  return api.get(`/admin/roles/${id}`);
};

export const createRole = async (roleData) => {
  return api.post('/admin/roles', roleData);
};

export const updateRole = async (id, roleData) => {
  return api.put(`/admin/roles/${id}`, roleData);
};

export const deleteRole = async (id) => {
  return api.delete(`/admin/roles/${id}`);
};

export const getPermissions = async () => {
  return api.get('/admin/permissions');
};

export const assignPermissionToRole = async (roleId, permissionId) => {
  return api.post(`/admin/roles/${roleId}/permissions/${permissionId}`);
};

export const revokePermissionFromRole = async (roleId, permissionId) => {
  return api.delete(`/admin/roles/${roleId}/permissions/${permissionId}`);
};

// System Health
export const getSystemHealth = async () => {
  return api.get('/admin/system-health');
};

export const getDatabaseHealth = async () => {
  return api.get('/admin/health/database');
};

export const getServiceHealth = async () => {
  return api.get('/admin/health/services');
};

// Backups
export const getBackups = async (params = {}) => {
  return api.get('/admin/backups', { params });
};

export const createBackup = async () => {
  return api.post('/admin/backups');
};

export const restoreBackup = async (backupId) => {
  return api.post(`/admin/backups/${backupId}/restore`);
};

export const deleteBackup = async (backupId) => {
  return api.delete(`/admin/backups/${backupId}`);
};

// Integration Management
export const getIntegrations = async (params = {}) => {
  return api.get('/admin/integrations', { params });
};

export const getIntegrationById = async (id) => {
  return api.get(`/admin/integrations/${id}`);
};

export const createIntegration = async (integrationData) => {
  return api.post('/admin/integrations', integrationData);
};

export const updateIntegration = async (id, integrationData) => {
  return api.put(`/admin/integrations/${id}`, integrationData);
};

export const deleteIntegration = async (id) => {
  return api.delete(`/admin/integrations/${id}`);
};

export const testIntegration = async (id) => {
  return api.post(`/admin/integrations/${id}/test`);
};

// Analytics
export const getAnalytics = async (params = {}) => {
  return api.get('/admin/analytics', { params });
};

export const getUserAnalytics = async (params = {}) => {
  return api.get('/admin/analytics/users', { params });
};

export const getEngagementAnalytics = async (params = {}) => {
  return api.get('/admin/analytics/engagements', { params });
};
