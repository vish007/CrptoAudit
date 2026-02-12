# SimplyFI PoR Platform - Frontend

A production-grade React frontend for the SimplyFI Proof of Reserves (PoR) Audit Platform - a banking-grade, multi-tenant SaaS for crypto asset audit and compliance management.

## Overview

The SimplyFI PoR Platform frontend is built with modern React technologies and follows enterprise-level architectural patterns. It supports multiple roles (SuperAdmin, Auditor, VASP Admin, VASP Finance, VASP Compliance, Customer, Regulator) with comprehensive permission-based access control.

## Tech Stack

- **React 18.2.0** - UI library
- **React Router 6.20.0** - Client-side routing
- **Redux Toolkit 2.0.0** - State management
- **Axios 1.6.0** - HTTP client with interceptors
- **Tailwind CSS 3.4.0** - Utility-first styling
- **Framer Motion 10.16.0** - Animation library
- **Recharts 2.10.0** - Charting library
- **Lucide React 0.263.1** - Icon library
- **React Hot Toast 2.4.0** - Toast notifications
- **Date-fns 3.0.0** - Date utilities

## Project Structure

```
src/
├── components/
│   ├── common/           # Reusable components
│   │   ├── Button.jsx
│   │   ├── Card.jsx
│   │   ├── DataTable.jsx
│   │   ├── Modal.jsx
│   │   ├── StatusBadge.jsx
│   │   ├── LoadingSpinner.jsx
│   │   ├── PermissionGate.jsx
│   │   └── StatCard.jsx
│   └── layout/           # Layout components
│       ├── Sidebar.jsx
│       ├── Header.jsx
│       └── Layout.jsx
├── pages/                # Page components organized by feature
│   ├── auth/
│   ├── dashboard/
│   ├── engagements/
│   ├── assets/
│   ├── merkle/
│   ├── blockchain/
│   ├── reports/
│   ├── admin/
│   └── settings/
├── store/                # Redux store configuration
│   ├── index.js
│   └── slices/           # Redux slices
│       ├── authSlice.js
│       ├── engagementSlice.js
│       ├── dashboardSlice.js
│       └── uiSlice.js
├── services/             # API service functions
│   ├── api.js            # Axios instance with interceptors
│   ├── authService.js
│   ├── engagementService.js
│   ├── assetService.js
│   ├── merkleService.js
│   ├── blockchainService.js
│   ├── reportService.js
│   ├── dashboardService.js
│   └── adminService.js
├── hooks/                # Custom React hooks
│   ├── useAuth.js        # Authentication hook
│   ├── usePermissions.js # Permission checking hook
│   ├── useEngagement.js  # Engagement data hook
│   └── useWebSocket.js   # WebSocket connection hook
├── types/                # JSDoc type definitions
│   └── index.js
├── utils/                # Utility functions
│   ├── constants.js      # App constants and enums
│   ├── formatters.js     # Data formatting utilities
│   └── validators.js     # Form validation utilities
├── App.jsx               # Main app component with routing
├── index.js              # App entry point
└── index.css             # Global styles and Tailwind imports
```

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

3. Configure environment variables:
```env
REACT_APP_API_URL=http://localhost:3001/api
REACT_APP_WS_URL=ws://localhost:3001
```

## Development

Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Key Features

### Authentication & Authorization
- JWT-based authentication with automatic token refresh
- Role-based access control (RBAC)
- Permission-based feature gates
- Session timeout with inactivity detection
- Multi-factor authentication support

### State Management
- Redux Toolkit for centralized state
- Async thunks for API calls
- Selectors for efficient state access
- Persistent storage for tokens and preferences

### API Integration
- Axios HTTP client with interceptors
- Automatic token injection in headers
- Token refresh on 401 responses
- Request/response logging
- Error handling with user-friendly messages

### UI Components
- Fully customizable with SimplyFI brand colors
- Dark navy (#001f3f) primary color
- Gold (#d4af37) accent color
- Emerald green (#10b981) for positive states
- Responsive design for mobile/tablet/desktop
- Smooth animations with Framer Motion

### Features by Role

#### SuperAdmin
- User and tenant management
- System configuration
- Audit log access
- AI agent management
- Role and permission management

#### Auditor
- View assigned engagements
- Perform audits
- Verify assets and blockchain data
- Generate audit reports
- Manage Merkle trees

#### VASP Admin
- Manage engagement lifecycle
- Manage team members
- Oversee asset and compliance submissions
- View compliance status

#### VASP Finance
- Submit financial assets
- View engagement status
- Access reports and analytics

#### VASP Compliance
- Submit compliance data
- Manage Merkle tree submissions
- Manage blockchain submissions

#### Customer
- View own engagements
- Download reports
- Limited data access

#### Regulator
- View all engagements
- View all reports
- Access compliance data
- Audit log access

## Routes

### Authentication
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/auth/forgot-password` - Password reset

### Main Application
- `/dashboard` - Dashboard with key metrics
- `/engagements` - Engagement list and management
- `/engagements/create` - Create new engagement
- `/engagements/:id` - Engagement details
- `/assets` - Asset management
- `/assets/:id` - Asset details
- `/merkle` - Merkle tree management
- `/merkle/:id` - Merkle tree details
- `/blockchain` - Blockchain verification
- `/reports` - Report management
- `/reports/:id` - Report details
- `/admin/users` - User management
- `/admin/tenants` - Tenant management
- `/admin/settings` - System settings
- `/admin/audit-logs` - Audit logs
- `/settings/profile` - Profile settings
- `/settings/security` - Security settings

## Custom Hooks

### useAuth()
Authentication state and methods:
```javascript
const { user, token, isAuthenticated, login, logout, refreshToken } = useAuth();
```

### usePermissions()
Permission checking:
```javascript
const { hasPermission, hasRole, isAdmin, canEdit, canApprove } = usePermissions();
```

### useEngagement()
Engagement data management:
```javascript
const { engagements, currentEngagement, getEngagements, createNewEngagement } = useEngagement();
```

### useWebSocket()
Real-time WebSocket connections:
```javascript
const { isConnected, send, on, subscribe } = useWebSocket();
```

## Utilities

### Formatters
- `formatDate()` - Format dates
- `formatCurrency()` - Format currency values
- `formatCrypto()` - Format crypto values
- `formatPercentage()` - Format percentages
- `formatCryptoAddress()` - Format wallet addresses
- `formatBytes()` - Format file sizes

### Validators
- `validateEmail()` - Email validation
- `validatePassword()` - Password validation
- `validateCryptoAddress()` - Crypto address validation
- `validateJSON()` - JSON validation
- `validateNumber()` - Number validation
- `createValidator()` - Create custom validators

### Constants
- `ROLES` - Role definitions
- `ROLE_PERMISSIONS` - Role to permission mapping
- `ENGAGEMENT_STATUS` - Engagement status enums
- `ASSET_STATUS` - Asset status enums
- `BLOCKCHAIN_NETWORKS` - Supported blockchain networks
- `PAGE_SIZES` - Pagination options

## Styling

The application uses Tailwind CSS with custom SimplyFI theme:

```javascript
// Custom colors
simplyfi-dark-navy: #001f3f
simplyfi-navy: #003d7a
simplyfi-light-navy: #1a5fa0
simplyfi-gold: #d4af37
simplyfi-light-gold: #f0d67d
simplyfi-emerald: #10b981
simplyfi-red-warning: #ef4444
```

## Error Handling

The application includes comprehensive error handling:
- API error interceptors
- Token refresh on expiration
- User-friendly error messages via toast notifications
- Form validation with detailed error messages
- Permission checks with graceful fallbacks

## Security

Key security features:
- JWT token-based authentication
- Secure token storage in localStorage
- Automatic session timeout
- CSRF protection ready (configure on backend)
- XSS prevention with React's built-in escaping
- Secure password validation requirements
- Permission-based access control

## Performance

- Lazy loading of page components
- Code splitting with React.lazy()
- Optimized Redux selectors
- Memoized components with React.memo
- Efficient state updates with Redux Toolkit
- Network request optimization with axios

## WebSocket Real-time Updates

For real-time features, the app includes WebSocket support:

```javascript
const { send, on, subscribe } = useWebSocket();

// Subscribe to engagement updates
subscribe('engagement:123');

// Listen for messages
on('engagement:updated', (data) => {
  console.log('Engagement updated:', data);
});
```

## Testing

(Configure your testing setup here)

```bash
npm test
```

## Deployment

The frontend can be deployed to any static hosting:

```bash
npm run build
# Upload the 'build' directory to your hosting provider
```

## Environment Configuration

Create `.env` files for different environments:

- `.env` - Local development
- `.env.development` - Development environment
- `.env.production` - Production environment

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

Copyright (c) 2024 SimplyFI. All rights reserved.

## Support

For issues and questions, contact support@simplyfi.com
