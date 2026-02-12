import api from './api';

export const login = async (email, password) => {
  return api.post('/auth/login', { email, password });
};

export const refreshToken = async (refreshToken) => {
  return api.post('/auth/refresh', { refreshToken });
};

export const logout = async () => {
  return api.post('/auth/logout');
};

export const verifyToken = async (token) => {
  return api.get('/auth/verify', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const register = async (userData) => {
  return api.post('/auth/register', userData);
};

export const resetPassword = async (email) => {
  return api.post('/auth/reset-password', { email });
};

export const resetPasswordWithToken = async (token, newPassword) => {
  return api.post('/auth/reset-password-confirm', { token, newPassword });
};

export const changePassword = async (currentPassword, newPassword) => {
  return api.post('/auth/change-password', { currentPassword, newPassword });
};

export const getTwoFactorMethods = async () => {
  return api.get('/auth/2fa/methods');
};

export const setupTwoFactor = async (method) => {
  return api.post('/auth/2fa/setup', { method });
};

export const confirmTwoFactor = async (code) => {
  return api.post('/auth/2fa/confirm', { code });
};

export const disableTwoFactor = async (password) => {
  return api.post('/auth/2fa/disable', { password });
};

export const validateTwoFactor = async (code) => {
  return api.post('/auth/2fa/validate', { code });
};

export const getCurrentUser = async () => {
  return api.get('/auth/me');
};

export const updateUserProfile = async (profileData) => {
  return api.put('/auth/me', profileData);
};

export const getUserSessions = async () => {
  return api.get('/auth/sessions');
};

export const revokeSession = async (sessionId) => {
  return api.delete(`/auth/sessions/${sessionId}`);
};

export const revokeAllSessions = async () => {
  return api.post('/auth/sessions/revoke-all');
};

export const getAuditLog = async (params = {}) => {
  return api.get('/auth/audit-log', { params });
};
