import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import engagementReducer from './slices/engagementSlice';
import dashboardReducer from './slices/dashboardSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    engagement: engagementReducer,
    dashboard: dashboardReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['auth/login/fulfilled', 'auth/refreshToken/fulfilled'],
        ignoredPaths: ['auth.user'],
      },
    }),
});

export default store;
