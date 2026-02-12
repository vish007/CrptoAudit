import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as engagementService from '../../services/engagementService';

const initialState = {
  engagements: [],
  currentEngagement: null,
  isLoading: false,
  error: null,
  filters: {
    status: null,
    type: null,
    searchTerm: '',
    sortBy: 'createdAt',
    sortDirection: 'desc',
  },
  pagination: {
    page: 1,
    pageSize: 10,
    total: 0,
    totalPages: 0,
    hasMore: false,
  },
};

export const fetchEngagements = createAsyncThunk(
  'engagement/fetchEngagements',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await engagementService.getEngagements(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch engagements');
    }
  }
);

export const fetchEngagementById = createAsyncThunk(
  'engagement/fetchEngagementById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await engagementService.getEngagementById(id);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch engagement');
    }
  }
);

export const createEngagement = createAsyncThunk(
  'engagement/createEngagement',
  async (engagementData, { rejectWithValue }) => {
    try {
      const response = await engagementService.createEngagement(engagementData);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to create engagement');
    }
  }
);

export const updateEngagement = createAsyncThunk(
  'engagement/updateEngagement',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await engagementService.updateEngagement(id, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to update engagement');
    }
  }
);

export const deleteEngagement = createAsyncThunk(
  'engagement/deleteEngagement',
  async (id, { rejectWithValue }) => {
    try {
      await engagementService.deleteEngagement(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to delete engagement');
    }
  }
);

const engagementSlice = createSlice({
  name: 'engagement',
  initialState,
  reducers: {
    setCurrentEngagement: (state, action) => {
      state.currentEngagement = action.payload;
    },
    clearCurrentEngagement: (state) => {
      state.currentEngagement = null;
    },
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = {
        status: null,
        type: null,
        searchTerm: '',
        sortBy: 'createdAt',
        sortDirection: 'desc',
      };
    },
    setPagination: (state, action) => {
      state.pagination = { ...state.pagination, ...action.payload };
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch Engagements
    builder
      .addCase(fetchEngagements.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchEngagements.fulfilled, (state, action) => {
        state.isLoading = false;
        state.engagements = action.payload.data;
        state.pagination = action.payload.pagination;
        state.error = null;
      })
      .addCase(fetchEngagements.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });

    // Fetch Engagement by ID
    builder
      .addCase(fetchEngagementById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchEngagementById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentEngagement = action.payload;
        state.error = null;
      })
      .addCase(fetchEngagementById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });

    // Create Engagement
    builder
      .addCase(createEngagement.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createEngagement.fulfilled, (state, action) => {
        state.isLoading = false;
        state.engagements.unshift(action.payload);
        state.currentEngagement = action.payload;
        state.error = null;
      })
      .addCase(createEngagement.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });

    // Update Engagement
    builder
      .addCase(updateEngagement.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateEngagement.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.engagements.findIndex((e) => e.id === action.payload.id);
        if (index > -1) {
          state.engagements[index] = action.payload;
        }
        if (state.currentEngagement?.id === action.payload.id) {
          state.currentEngagement = action.payload;
        }
        state.error = null;
      })
      .addCase(updateEngagement.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });

    // Delete Engagement
    builder
      .addCase(deleteEngagement.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteEngagement.fulfilled, (state, action) => {
        state.isLoading = false;
        state.engagements = state.engagements.filter((e) => e.id !== action.payload);
        if (state.currentEngagement?.id === action.payload) {
          state.currentEngagement = null;
        }
        state.error = null;
      })
      .addCase(deleteEngagement.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const {
  setCurrentEngagement,
  clearCurrentEngagement,
  setFilters,
  clearFilters,
  setPagination,
  clearError,
} = engagementSlice.actions;

// Selectors
export const selectEngagements = (state) => state.engagement.engagements;
export const selectCurrentEngagement = (state) => state.engagement.currentEngagement;
export const selectEngagementIsLoading = (state) => state.engagement.isLoading;
export const selectEngagementError = (state) => state.engagement.error;
export const selectEngagementFilters = (state) => state.engagement.filters;
export const selectEngagementPagination = (state) => state.engagement.pagination;

export default engagementSlice.reducer;
