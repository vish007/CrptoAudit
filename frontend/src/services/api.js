import axios from 'axios';
import { API_BASE_URL, HTTP_STATUS, SESSION_TIMEOUT, TOKEN_REFRESH_THRESHOLD } from '../utils/constants';
import store from '../store';
import { refreshToken, logout } from '../store/slices/authSlice';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

// Request interceptor to add authorization token
api.interceptors.request.use(
  (config) => {
    const state = store.getState();
    const token = state.auth.token;

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Add request timestamp for debugging
    config.metadata = { startTime: Date.now() };

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh and errors
api.interceptors.response.use(
  (response) => {
    // Log response time
    const duration = Date.now() - response.config.metadata.startTime;
    console.debug(`[API] ${response.config.method.toUpperCase()} ${response.config.url} - ${duration}ms`);

    return response;
  },
  async (error) => {
    const { config } = error;
    const state = store.getState();
    const token = state.auth.token;

    if (!config) {
      return Promise.reject(error);
    }

    // Handle token expiration
    if (error.response?.status === HTTP_STATUS.UNAUTHORIZED) {
      if (!isRefreshing && token) {
        isRefreshing = true;

        try {
          await store.dispatch(refreshToken());
          const newState = store.getState();
          const newToken = newState.auth.token;

          if (newToken) {
            config.headers.Authorization = `Bearer ${newToken}`;
            processQueue(null, newToken);
            return api(config);
          } else {
            processQueue(error, null);
            store.dispatch(logout());
            window.location.href = '/auth/login';
            return Promise.reject(error);
          }
        } catch (err) {
          processQueue(err, null);
          store.dispatch(logout());
          window.location.href = '/auth/login';
          return Promise.reject(err);
        } finally {
          isRefreshing = false;
        }
      } else if (isRefreshing && token) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((newToken) => {
            config.headers.Authorization = `Bearer ${newToken}`;
            return api(config);
          })
          .catch((err) => {
            return Promise.reject(err);
          });
      }
    }

    // Handle other status codes
    if (error.response?.status === HTTP_STATUS.FORBIDDEN) {
      console.warn('[API] Access forbidden - insufficient permissions');
    }

    if (error.response?.status === HTTP_STATUS.NOT_FOUND) {
      console.warn('[API] Resource not found');
    }

    if (error.response?.status >= HTTP_STATUS.INTERNAL_SERVER_ERROR) {
      console.error('[API] Server error:', error.response?.status);
    }

    return Promise.reject(error);
  }
);

export default api;
