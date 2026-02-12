import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as authService from '../../services/authService';

const initialState = {
  user: null,
  token: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  isLoading: false,
  isRefreshing: false,
  error: null,
  isAuthenticated: !!localStorage.getItem('accessToken'),
};

export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const response = await authService.login(email, password);
      localStorage.setItem('accessToken', response.data.token);
      localStorage.setItem('refreshToken', response.data.refreshToken);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Login failed');
    }
  }
);

export const refreshToken = createAsyncThunk(
  'auth/refreshToken',
  async (_, { rejectWithValue }) => {
    try {
      const refreshTokenValue = localStorage.getItem('refreshToken');
      if (!refreshTokenValue) {
        throw new Error('No refresh token');
      }

      const response = await authService.refreshToken(refreshTokenValue);
      localStorage.setItem('accessToken', response.data.token);
      if (response.data.refreshToken) {
        localStorage.setItem('refreshToken', response.data.refreshToken);
      }
      return response.data;
    } catch (error) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      return rejectWithValue('Token refresh failed');
    }
  }
);

export const logout = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    }
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    return null;
  }
);

export const verifyToken = createAsyncThunk(
  'auth/verifyToken',
  async (token, { rejectWithValue }) => {
    try {
      const response = await authService.verifyToken(token);
      return response.data;
    } catch (error) {
      return rejectWithValue('Token verification failed');
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    updateUserProfile: (state, action) => {
      if (state.user) {
        state.user = { ...state.user, ...action.payload };
        localStorage.setItem('user', JSON.stringify(state.user));
      }
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.token = action.payload.token;
        state.refreshToken = action.payload.refreshToken;
        state.isAuthenticated = true;
        state.error = null;
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.error = action.payload;
        state.user = null;
        state.token = null;
        state.refreshToken = null;
      });

    // Refresh Token
    builder
      .addCase(refreshToken.pending, (state) => {
        state.isRefreshing = true;
        state.error = null;
      })
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.isRefreshing = false;
        state.token = action.payload.token;
        if (action.payload.refreshToken) {
          state.refreshToken = action.payload.refreshToken;
        }
        state.isAuthenticated = true;
        state.error = null;
      })
      .addCase(refreshToken.rejected, (state, action) => {
        state.isRefreshing = false;
        state.isAuthenticated = false;
        state.error = action.payload;
        state.user = null;
        state.token = null;
        state.refreshToken = null;
      });

    // Logout
    builder
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
        state.token = null;
        state.refreshToken = null;
        state.isAuthenticated = false;
        state.error = null;
        state.isLoading = false;
      });

    // Verify Token
    builder
      .addCase(verifyToken.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(verifyToken.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.error = null;
      })
      .addCase(verifyToken.rejected, (state) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
        state.refreshToken = null;
      });
  },
});

export const { setUser, clearError, updateUserProfile } = authSlice.actions;

// Selectors
export const selectUser = (state) => state.auth.user;
export const selectToken = (state) => state.auth.token;
export const selectIsAuthenticated = (state) => state.auth.isAuthenticated;
export const selectIsLoading = (state) => state.auth.isLoading;
export const selectError = (state) => state.auth.error;
export const selectUserRole = (state) => state.auth.user?.role;
export const selectUserPermissions = (state) => state.auth.user?.permissions || [];
export const selectTenantId = (state) => state.auth.user?.tenantId;

export default authSlice.reducer;
