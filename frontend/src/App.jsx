import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { selectIsAuthenticated, selectUser } from './store/slices/authSlice';
import Layout from './components/layout/Layout';
import LoadingSpinner from './components/common/LoadingSpinner';
import Toaster from 'react-hot-toast';
import useAuth from './hooks/useAuth';

// Page imports - Auth
const LoginPage = React.lazy(() => import('./pages/auth/LoginPage'));
const RegisterPage = React.lazy(() => import('./pages/auth/RegisterPage'));
const ForgotPasswordPage = React.lazy(() => import('./pages/auth/ForgotPasswordPage'));

// Page imports - Dashboard
const DashboardPage = React.lazy(() => import('./pages/dashboard/DashboardPage'));

// Page imports - Engagements
const EngagementsPage = React.lazy(() => import('./pages/engagements/EngagementsPage'));
const EngagementDetailPage = React.lazy(() => import('./pages/engagements/EngagementDetailPage'));
const CreateEngagementPage = React.lazy(() => import('./pages/engagements/CreateEngagementPage'));

// Page imports - Assets
const AssetsPage = React.lazy(() => import('./pages/assets/AssetsPage'));
const AssetDetailPage = React.lazy(() => import('./pages/assets/AssetDetailPage'));

// Page imports - Merkle
const MerkleTreesPage = React.lazy(() => import('./pages/merkle/MerkleTreesPage'));
const MerkleDetailPage = React.lazy(() => import('./pages/merkle/MerkleDetailPage'));

// Page imports - Blockchain
const BlockchainPage = React.lazy(() => import('./pages/blockchain/BlockchainPage'));

// Page imports - Reports
const ReportsPage = React.lazy(() => import('./pages/reports/ReportsPage'));
const ReportDetailPage = React.lazy(() => import('./pages/reports/ReportDetailPage'));

// Page imports - Admin
const AdminUsersPage = React.lazy(() => import('./pages/admin/AdminUsersPage'));
const AdminTenantsPage = React.lazy(() => import('./pages/admin/AdminTenantsPage'));
const AdminSettingsPage = React.lazy(() => import('./pages/admin/AdminSettingsPage'));
const AdminAuditLogsPage = React.lazy(() => import('./pages/admin/AdminAuditLogsPage'));

// Page imports - Settings
const ProfileSettingsPage = React.lazy(() => import('./pages/settings/ProfileSettingsPage'));
const SecuritySettingsPage = React.lazy(() => import('./pages/settings/SecuritySettingsPage'));

// Page imports - 404
const NotFoundPage = React.lazy(() => import('./pages/NotFoundPage'));

/**
 * Protected Route Wrapper
 * Checks authentication and redirects to login if not authenticated
 */
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = useSelector(selectIsAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }

  return children;
};

/**
 * Public Route Wrapper
 * Redirects to dashboard if already authenticated
 */
const PublicRoute = ({ children }) => {
  const isAuthenticated = useSelector(selectIsAuthenticated);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

/**
 * Lazy Load Boundary
 * Shows loading spinner while component loads
 */
const LazyBoundary = ({ children }) => {
  return (
    <React.Suspense fallback={<LoadingSpinner fullScreen message="Loading..." />}>
      {children}
    </React.Suspense>
  );
};

/**
 * Main App Component
 */
function App() {
  const { isAuthenticated } = useAuth();
  const user = useSelector(selectUser);

  // Verify token on app load
  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token && !isAuthenticated) {
      // Token exists but user not authenticated - could be on first load
      // Component will handle verification through auth slice
    }
  }, [isAuthenticated]);

  return (
    <Router>
      <div className="min-h-screen bg-simplyfi-neutral-bg">
        <Routes>
          {/* Auth Routes */}
          <Route
            path="/auth/login"
            element={
              <LazyBoundary>
                <PublicRoute>
                  <LoginPage />
                </PublicRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/auth/register"
            element={
              <LazyBoundary>
                <PublicRoute>
                  <RegisterPage />
                </PublicRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/auth/forgot-password"
            element={
              <LazyBoundary>
                <PublicRoute>
                  <ForgotPasswordPage />
                </PublicRoute>
              </LazyBoundary>
            }
          />

          {/* Dashboard Route */}
          <Route
            path="/dashboard"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Dashboard">
                    <DashboardPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* Engagement Routes */}
          <Route
            path="/engagements"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Engagements" breadcrumbs={['Engagements']}>
                    <EngagementsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/engagements/create"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Create Engagement" breadcrumbs={['Engagements', 'Create']}>
                    <CreateEngagementPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/engagements/:id"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Engagement Details" breadcrumbs={['Engagements', 'Details']}>
                    <EngagementDetailPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* Asset Routes */}
          <Route
            path="/assets"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Assets" breadcrumbs={['Assets']}>
                    <AssetsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/assets/:id"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Asset Details" breadcrumbs={['Assets', 'Details']}>
                    <AssetDetailPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* Merkle Routes */}
          <Route
            path="/merkle"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Merkle Trees" breadcrumbs={['Merkle Trees']}>
                    <MerkleTreesPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/merkle/:id"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Merkle Tree Details" breadcrumbs={['Merkle Trees', 'Details']}>
                    <MerkleDetailPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* Blockchain Routes */}
          <Route
            path="/blockchain"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Blockchain Data" breadcrumbs={['Blockchain']}>
                    <BlockchainPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* Report Routes */}
          <Route
            path="/reports"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Reports" breadcrumbs={['Reports']}>
                    <ReportsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/reports/:id"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Report Details" breadcrumbs={['Reports', 'Details']}>
                    <ReportDetailPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* Admin Routes */}
          <Route
            path="/admin/users"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="User Management" breadcrumbs={['Admin', 'Users']}>
                    <AdminUsersPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/admin/tenants"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Tenant Management" breadcrumbs={['Admin', 'Tenants']}>
                    <AdminTenantsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/admin/settings"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="System Settings" breadcrumbs={['Admin', 'Settings']}>
                    <AdminSettingsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/admin/audit-logs"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Audit Logs" breadcrumbs={['Admin', 'Audit Logs']}>
                    <AdminAuditLogsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* Settings Routes */}
          <Route
            path="/settings/profile"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Profile Settings" breadcrumbs={['Settings', 'Profile']}>
                    <ProfileSettingsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />
          <Route
            path="/settings/security"
            element={
              <LazyBoundary>
                <ProtectedRoute>
                  <Layout title="Security Settings" breadcrumbs={['Settings', 'Security']}>
                    <SecuritySettingsPage />
                  </Layout>
                </ProtectedRoute>
              </LazyBoundary>
            }
          />

          {/* 404 Route */}
          <Route
            path="*"
            element={
              <LazyBoundary>
                <NotFoundPage />
              </LazyBoundary>
            }
          />

          {/* Default Route */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>

        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          reverseOrder={false}
          gutter={8}
          toastOptions={{
            duration: 4000,
            style: {
              background: '#fff',
              color: '#1f2937',
            },
          }}
        />
      </div>
    </Router>
  );
}

export default App;
