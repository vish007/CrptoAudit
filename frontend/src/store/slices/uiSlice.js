import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  sidebarOpen: true,
  sidebarCollapsed: false,
  theme: localStorage.getItem('theme') || 'dark',
  notifications: [],
  modals: {},
  currentTenant: localStorage.getItem('currentTenant') || null,
  currentEngagementContext: localStorage.getItem('currentEngagementContext') || null,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action) => {
      state.sidebarOpen = action.payload;
    },
    toggleSidebarCollapse: (state) => {
      state.sidebarCollapsed = !state.sidebarCollapsed;
    },
    setSidebarCollapsed: (state, action) => {
      state.sidebarCollapsed = action.payload;
    },
    toggleTheme: (state) => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('theme', state.theme);
    },
    setTheme: (state, action) => {
      state.theme = action.payload;
      localStorage.setItem('theme', action.payload);
    },
    addNotification: (state, action) => {
      const notification = {
        id: Date.now(),
        ...action.payload,
      };
      state.notifications.push(notification);
    },
    removeNotification: (state, action) => {
      state.notifications = state.notifications.filter((n) => n.id !== action.payload);
    },
    clearNotifications: (state) => {
      state.notifications = [];
    },
    openModal: (state, action) => {
      const { modalId, data } = action.payload;
      state.modals[modalId] = { isOpen: true, data };
    },
    closeModal: (state, action) => {
      const { modalId } = action.payload;
      state.modals[modalId] = { isOpen: false, data: null };
    },
    setCurrentTenant: (state, action) => {
      state.currentTenant = action.payload;
      localStorage.setItem('currentTenant', action.payload);
    },
    setCurrentEngagementContext: (state, action) => {
      state.currentEngagementContext = action.payload;
      localStorage.setItem('currentEngagementContext', action.payload);
    },
  },
});

export const {
  toggleSidebar,
  setSidebarOpen,
  toggleSidebarCollapse,
  setSidebarCollapsed,
  toggleTheme,
  setTheme,
  addNotification,
  removeNotification,
  clearNotifications,
  openModal,
  closeModal,
  setCurrentTenant,
  setCurrentEngagementContext,
} = uiSlice.actions;

// Selectors
export const selectSidebarOpen = (state) => state.ui.sidebarOpen;
export const selectSidebarCollapsed = (state) => state.ui.sidebarCollapsed;
export const selectTheme = (state) => state.ui.theme;
export const selectNotifications = (state) => state.ui.notifications;
export const selectModals = (state) => state.ui.modals;
export const selectCurrentTenant = (state) => state.ui.currentTenant;
export const selectCurrentEngagementContext = (state) => state.ui.currentEngagementContext;

export default uiSlice.reducer;
