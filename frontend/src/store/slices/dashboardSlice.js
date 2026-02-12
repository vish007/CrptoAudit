import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as dashboardService from '../../services/dashboardService';

const initialState = {
  stats: null,
  recentActivity: [],
  assetBreakdown: null,
  statusDistribution: null,
  topRisks: [],
  isLoading: false,
  error: null,
  lastUpdated: null,
};

export const fetchDashboardStats = createAsyncThunk(
  'dashboard/fetchStats',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await dashboardService.getDashboardStats(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch dashboard stats');
    }
  }
);

export const fetchDashboardData = createAsyncThunk(
  'dashboard/fetchDashboardData',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await dashboardService.getDashboardData(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch dashboard data');
    }
  }
);

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    resetDashboard: () => initialState,
  },
  extraReducers: (builder) => {
    // Fetch Stats
    builder
      .addCase(fetchDashboardStats.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDashboardStats.fulfilled, (state, action) => {
        state.isLoading = false;
        state.stats = action.payload.stats;
        state.assetBreakdown = action.payload.assetBreakdown;
        state.statusDistribution = action.payload.statusDistribution;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchDashboardStats.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });

    // Fetch Dashboard Data
    builder
      .addCase(fetchDashboardData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.isLoading = false;
        state.recentActivity = action.payload.recentActivity || [];
        state.topRisks = action.payload.topRisks || [];
        state.stats = action.payload.stats || state.stats;
        state.lastUpdated = new Date().toISOString();
        state.error = null;
      })
      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, resetDashboard } = dashboardSlice.actions;

// Selectors
export const selectDashboardStats = (state) => state.dashboard.stats;
export const selectRecentActivity = (state) => state.dashboard.recentActivity;
export const selectAssetBreakdown = (state) => state.dashboard.assetBreakdown;
export const selectStatusDistribution = (state) => state.dashboard.statusDistribution;
export const selectTopRisks = (state) => state.dashboard.topRisks;
export const selectDashboardIsLoading = (state) => state.dashboard.isLoading;
export const selectDashboardError = (state) => state.dashboard.error;
export const selectLastUpdated = (state) => state.dashboard.lastUpdated;

export default dashboardSlice.reducer;
