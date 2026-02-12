# SimplyFI PoR Platform - Architecture & Design

## Project Overview

This is a production-grade React frontend for the SimplyFI Proof of Reserves (PoR) Audit Platform - a banking-grade, multi-tenant SaaS application for managing crypto asset audits and compliance verification.

**Base Directory**: `/sessions/great-ecstatic-ptolemy/mnt/POR/simplyfi-por-platform/frontend/`

## Architecture Principles

1. **Component-Driven Architecture**: Modular, reusable components with single responsibilities
2. **State Management**: Centralized Redux store with async thunks for API calls
3. **Service Layer**: Abstracted API calls in service modules
4. **Custom Hooks**: Encapsulated business logic in reusable hooks
5. **Type Safety**: JSDoc type definitions for all entities
6. **Security First**: Role-based access control, permission gates, secure token handling
7. **Responsive Design**: Mobile-first approach with Tailwind CSS
8. **Performance**: Lazy loading, code splitting, optimized selectors

## Directory Structure

```
frontend/
├── public/                      # Static assets
│   ├── index.html              # Main HTML file
│   └── manifest.json           # PWA manifest
│
├── src/
│   ├── components/             # React components
│   │   ├── common/             # Reusable UI components
│   │   │   ├── Button.jsx      # Button component with variants
│   │   │   ├── Card.jsx        # Card container component
│   │   │   ├── DataTable.jsx   # Searchable, sortable, paginated table
│   │   │   ├── Modal.jsx       # Modal dialog with animations
│   │   │   ├── StatusBadge.jsx # Status indicator badges
│   │   │   ├── LoadingSpinner.jsx  # Loading indicators
│   │   │   ├── PermissionGate.jsx  # Permission-based rendering
│   │   │   └── StatCard.jsx    # Dashboard stat cards
│   │   │
│   │   └── layout/             # Layout components
│   │       ├── Sidebar.jsx     # Collapsible navigation sidebar
│   │       ├── Header.jsx      # Top header with user menu
│   │       └── Layout.jsx      # Main layout wrapper
│   │
│   ├── pages/                  # Page-level components (feature routes)
│   │   ├── auth/
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   └── ForgotPasswordPage.jsx
│   │   ├── dashboard/
│   │   │   └── DashboardPage.jsx    # Main dashboard with metrics
│   │   ├── engagements/
│   │   │   ├── EngagementsPage.jsx      # List view
│   │   │   ├── EngagementDetailPage.jsx # Detail view
│   │   │   └── CreateEngagementPage.jsx # Creation form
│   │   ├── assets/
│   │   │   ├── AssetsPage.jsx
│   │   │   └── AssetDetailPage.jsx
│   │   ├── merkle/
│   │   │   ├── MerkleTreesPage.jsx
│   │   │   └── MerkleDetailPage.jsx
│   │   ├── blockchain/
│   │   │   └── BlockchainPage.jsx
│   │   ├── reports/
│   │   │   ├── ReportsPage.jsx
│   │   │   └── ReportDetailPage.jsx
│   │   ├── admin/
│   │   │   ├── AdminUsersPage.jsx
│   │   │   ├── AdminTenantsPage.jsx
│   │   │   ├── AdminSettingsPage.jsx
│   │   │   └── AdminAuditLogsPage.jsx
│   │   ├── settings/
│   │   │   ├── ProfileSettingsPage.jsx
│   │   │   └── SecuritySettingsPage.jsx
│   │   └── NotFoundPage.jsx
│   │
│   ├── store/                  # Redux store
│   │   ├── index.js            # Store configuration
│   │   └── slices/
│   │       ├── authSlice.js         # Auth state & thunks
│   │       ├── engagementSlice.js   # Engagement state
│   │       ├── dashboardSlice.js    # Dashboard state
│   │       └── uiSlice.js           # UI state (sidebar, theme, modals)
│   │
│   ├── services/               # API service layer
│   │   ├── api.js              # Axios instance with interceptors
│   │   ├── authService.js      # Auth endpoints
│   │   ├── engagementService.js    # Engagement endpoints
│   │   ├── assetService.js     # Asset endpoints
│   │   ├── merkleService.js    # Merkle tree endpoints
│   │   ├── blockchainService.js    # Blockchain endpoints
│   │   ├── reportService.js    # Report endpoints
│   │   ├── dashboardService.js # Dashboard endpoints
│   │   └── adminService.js     # Admin endpoints
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAuth.js          # Authentication hook
│   │   ├── usePermissions.js   # Permission checking hook
│   │   ├── useEngagement.js    # Engagement data hook
│   │   └── useWebSocket.js     # WebSocket connection hook
│   │
│   ├── types/                  # JSDoc type definitions
│   │   └── index.js            # All TypeScript-style JSDoc types
│   │
│   ├── utils/                  # Utility functions
│   │   ├── constants.js        # Enums, constants, role definitions
│   │   ├── formatters.js       # Data formatting utilities
│   │   └── validators.js       # Form validation utilities
│   │
│   ├── App.jsx                 # Main app component with routing
│   ├── index.js                # React app entry point
│   └── index.css               # Global styles
│
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── package.json                # Dependencies & scripts
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
├── ARCHITECTURE.md             # This file
└── README.md                   # Project documentation
```

## Core Concepts

### 1. State Management (Redux)

**Store Structure**:
```javascript
{
  auth: {
    user,           // User object
    token,          // JWT access token
    refreshToken,   // Refresh token
    isLoading,      // Loading state
    error,          // Error messages
    isAuthenticated // Auth status
  },
  engagement: {
    engagements,    // Array of engagements
    currentEngagement,
    isLoading,
    error,
    filters,
    pagination
  },
  dashboard: {
    stats,          // Dashboard statistics
    recentActivity,
    assetBreakdown,
    topRisks,
    isLoading,
    error
  },
  ui: {
    sidebarOpen,    // Sidebar state
    theme,          // Light/dark theme
    notifications,  // Toast notifications
    modals,         // Modal states
    currentTenant,  // Selected tenant
    currentEngagementContext
  }
}
```

### 2. API Integration

**Axios Interceptors**:
- Request: Adds Authorization header with JWT token
- Response: Handles 401 errors by refreshing token
- Auto-retry failed requests after token refresh
- Comprehensive error logging

**Service Layer**:
Each service module (`authService.js`, `engagementService.js`, etc.) exports functions that wrap API calls.

### 3. Authentication Flow

```
Login → JWT Token → Store Token → Auto Refresh → Session Timeout → Logout
                  ↓
          Intercept 401 → Refresh Token → Retry Request
```

### 4. Permission-Based Access Control

**Role Definitions**:
```javascript
ROLES = {
  SUPER_ADMIN: 'SuperAdmin',
  AUDITOR: 'Auditor',
  VASP_ADMIN: 'VASP_Admin',
  VASP_FINANCE: 'VASP_Finance',
  VASP_COMPLIANCE: 'VASP_Compliance',
  CUSTOMER: 'Customer',
  REGULATOR: 'Regulator'
}
```

**Permission Mapping**:
Each role has an array of permissions. Features are gated by:
1. `PermissionGate` component - Conditional rendering
2. `usePermissions()` hook - Programmatic checks
3. Protected routes - Navigation protection

### 5. Component Hierarchy

```
App (Router)
├── ProtectedRoute / PublicRoute
├── Layout
│   ├── Sidebar
│   ├── Header
│   └── Main Content
│       └── Page Component
│           └── Common Components (Card, Button, DataTable, etc.)
```

### 6. Data Flow

```
Page Component
    ↓
useAuth() / useEngagement() hooks
    ↓
Dispatch Redux Action
    ↓
Redux Thunk (async)
    ↓
Service Layer (API call)
    ↓
Axios (with interceptors)
    ↓
Backend API
    ↓
Reducer updates state
    ↓
Component re-renders
```

## Key Technologies

### Frontend Framework
- **React 18.2.0**: Latest hooks, concurrent features, strict mode
- **React Router 6.20.0**: Nested routing, lazy code splitting, protected routes

### State & Side Effects
- **Redux Toolkit 2.0.0**: Simplified Redux with createSlice, createAsyncThunk
- **React-Redux 9.0.0**: Hooks API (useSelector, useDispatch)

### UI & Styling
- **Tailwind CSS 3.4.0**: Utility-first CSS framework
- **Lucide React 0.263.1**: Modern icon library
- **Framer Motion 10.16.0**: Animation library
- **clsx 2.0.0**: Conditional classname utility

### HTTP & APIs
- **Axios 1.6.0**: Promise-based HTTP client
- **Custom Interceptors**: Token management, error handling

### Forms & Validation
- **React Hot Toast 2.4.0**: Toast notifications
- **Custom Validators**: Email, password, crypto addresses, etc.

### Utilities
- **Date-fns 3.0.0**: Date manipulation (format, parse, etc.)
- **Recharts 2.10.0**: React charting library

## Color Scheme (SimplyFI Brand)

```css
Dark Navy:       #001f3f (Primary)
Navy:            #003d7a
Light Navy:      #1a5fa0
Gold:            #d4af37 (Accent)
Light Gold:      #f0d67d
Emerald:         #10b981 (Success)
Red Warning:     #ef4444 (Error)
Orange Warning:  #f97316 (Warning)
Neutral BG:      #f8f9fa
Border Light:    #e5e7eb
Text Dark:       #1f2937
Text Muted:      #6b7280
```

## Security Features

1. **Authentication**
   - JWT token storage in localStorage
   - Automatic token refresh 5 minutes before expiration
   - Session timeout after 30 minutes of inactivity

2. **Authorization**
   - Role-based access control
   - Permission-based feature gates
   - Protected routes with auth checks

3. **API Security**
   - Authorization header injection
   - HTTPS-ready configuration
   - CORS-compatible

4. **Data Validation**
   - Form validators for all inputs
   - Type checking with JSDoc
   - Crypto address validation

## Performance Optimizations

1. **Code Splitting**
   - Lazy loading page components with React.lazy()
   - Route-based code splitting

2. **State Management**
   - Selector memoization with Redux
   - Efficient state shape design

3. **Rendering**
   - Component memoization where needed
   - Conditional rendering to avoid unnecessary renders

4. **Network**
   - Request debouncing/throttling ready
   - Batch API requests capability
   - Response caching possible

## File Size Breakdown

- **Components**: ~45KB (UI library)
- **Pages**: ~55KB (Feature pages)
- **Store**: ~25KB (Redux setup)
- **Services**: ~35KB (API layer)
- **Hooks**: ~15KB (Custom hooks)
- **Utils**: ~20KB (Helpers)
- **Total**: ~195KB (development, ~65KB gzipped production)

## Running the Application

### Development
```bash
npm install
npm start
# Runs on http://localhost:3000
```

### Production Build
```bash
npm run build
# Creates optimized build in /build directory
# ~120KB gzipped including all dependencies
```

### Environment Setup
```env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_WS_URL=ws://localhost:3001
REACT_APP_ENV=development
```

## Integration Points

### Backend API
- RESTful endpoints at `/api/*`
- WebSocket at `ws://localhost:3001`
- JWT authentication
- Role-based response filtering

### External Services
- Ready for analytics integration
- Email provider ready (via backend)
- Blockchain RPC nodes (via backend)
- File storage (via backend)

## Future Enhancements

1. **Offline Support**: Service workers, offline data sync
2. **Advanced Caching**: Request caching, stale-while-revalidate
3. **Real-time Collaboration**: WebSocket-based live updates
4. **Advanced Analytics**: User behavior tracking, performance monitoring
5. **Accessibility**: WCAG 2.1 AA compliance
6. **Internationalization**: Multi-language support
7. **Dark Mode**: Full dark theme implementation
8. **Progressive Web App**: Installable web app

## Deployment Checklist

- [ ] Environment variables configured
- [ ] API URL points to production
- [ ] Build optimized (npm run build)
- [ ] Assets minified and compressed
- [ ] Analytics configured
- [ ] Error tracking enabled
- [ ] Performance monitoring active
- [ ] Security headers configured
- [ ] HTTPS enforced
- [ ] Cache headers set appropriately
