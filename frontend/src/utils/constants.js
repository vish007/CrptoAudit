export const ROLES = {
  SUPER_ADMIN: 'SuperAdmin',
  AUDITOR: 'Auditor',
  VASP_ADMIN: 'VASP_Admin',
  VASP_FINANCE: 'VASP_Finance',
  VASP_COMPLIANCE: 'VASP_Compliance',
  CUSTOMER: 'Customer',
  REGULATOR: 'Regulator',
};

export const ROLE_PERMISSIONS = {
  [ROLES.SUPER_ADMIN]: [
    'view_all_engagements',
    'manage_users',
    'manage_auditors',
    'manage_vasp',
    'manage_assets',
    'manage_merkle',
    'manage_blockchain',
    'generate_reports',
    'manage_system_settings',
    'view_audit_logs',
    'manage_ai_agents',
    'approve_assets',
    'approve_reports',
  ],
  [ROLES.AUDITOR]: [
    'view_assignments',
    'perform_audit',
    'verify_assets',
    'generate_audit_reports',
    'manage_merkle_trees',
    'view_blockchain_data',
    'communicate_with_vasp',
    'view_compliance_status',
  ],
  [ROLES.VASP_ADMIN]: [
    'manage_engagement',
    'view_reports',
    'manage_finance_team',
    'manage_compliance_team',
    'view_assets',
    'initiate_audit',
    'manage_merkle_submission',
    'view_blockchain_data',
  ],
  [ROLES.VASP_FINANCE]: [
    'view_engagement',
    'submit_financial_assets',
    'view_reports',
    'manage_asset_data',
    'view_blockchain_data',
  ],
  [ROLES.VASP_COMPLIANCE]: [
    'view_engagement',
    'submit_compliance_data',
    'view_reports',
    'manage_merkle_submission',
    'manage_blockchain_submission',
  ],
  [ROLES.CUSTOMER]: [
    'view_own_engagement',
    'view_own_reports',
    'download_reports',
  ],
  [ROLES.REGULATOR]: [
    'view_all_engagements',
    'view_all_reports',
    'view_compliance_status',
    'view_audit_logs',
  ],
};

export const ENGAGEMENT_STATUS = {
  PENDING: 'pending',
  IN_PROGRESS: 'in_progress',
  UNDER_REVIEW: 'under_review',
  COMPLETED: 'completed',
  FAILED: 'failed',
  APPROVED: 'approved',
  REJECTED: 'rejected',
};

export const ASSET_STATUS = {
  PENDING: 'pending',
  SUBMITTED: 'submitted',
  VERIFIED: 'verified',
  REJECTED: 'rejected',
  IN_REVIEW: 'in_review',
};

export const AUDIT_STATUS = {
  NOT_STARTED: 'not_started',
  IN_PROGRESS: 'in_progress',
  AWAITING_DOCUMENTATION: 'awaiting_documentation',
  UNDER_REVIEW: 'under_review',
  COMPLETED: 'completed',
  FAILED: 'failed',
};

export const BLOCKCHAIN_NETWORKS = {
  ETHEREUM: 'ethereum',
  BITCOIN: 'bitcoin',
  POLYGON: 'polygon',
  ARBITRUM: 'arbitrum',
  OPTIMISM: 'optimism',
  SOLANA: 'solana',
  CARDANO: 'cardano',
};

export const ASSET_TYPES = {
  CRYPTO: 'crypto',
  FIAT: 'fiat',
  DERIVATIVE: 'derivative',
  COMMODITY: 'commodity',
};

export const REPORT_STATUS = {
  DRAFT: 'draft',
  PENDING_APPROVAL: 'pending_approval',
  APPROVED: 'approved',
  PUBLISHED: 'published',
  ARCHIVED: 'archived',
};

export const REPORT_TYPE = {
  AUDIT_REPORT: 'audit_report',
  COMPLIANCE_REPORT: 'compliance_report',
  FINANCIAL_REPORT: 'financial_report',
  TECHNICAL_REPORT: 'technical_report',
  EXECUTIVE_SUMMARY: 'executive_summary',
};

export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';
export const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:3001';

export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
};

export const PAGE_SIZES = [10, 25, 50, 100];

export const DATETIME_FORMAT = 'yyyy-MM-dd HH:mm:ss';
export const DATE_FORMAT = 'yyyy-MM-dd';
export const TIME_FORMAT = 'HH:mm:ss';

export const CRYPTO_PRECISION = 8;
export const FIAT_PRECISION = 2;

export const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB
export const ALLOWED_FILE_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-excel',
  'application/json',
  'text/csv',
];

export const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes
export const TOKEN_REFRESH_THRESHOLD = 5 * 60 * 1000; // 5 minutes

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
};

export const STATUS_COLOR_MAP = {
  [ENGAGEMENT_STATUS.PENDING]: 'info',
  [ENGAGEMENT_STATUS.IN_PROGRESS]: 'warning',
  [ENGAGEMENT_STATUS.UNDER_REVIEW]: 'warning',
  [ENGAGEMENT_STATUS.COMPLETED]: 'success',
  [ENGAGEMENT_STATUS.APPROVED]: 'success',
  [ENGAGEMENT_STATUS.FAILED]: 'error',
  [ENGAGEMENT_STATUS.REJECTED]: 'error',
  [ASSET_STATUS.PENDING]: 'info',
  [ASSET_STATUS.SUBMITTED]: 'warning',
  [ASSET_STATUS.VERIFIED]: 'success',
  [ASSET_STATUS.REJECTED]: 'error',
  [ASSET_STATUS.IN_REVIEW]: 'warning',
};

export const SIDEBAR_WIDTH = {
  COLLAPSED: '80px',
  EXPANDED: '280px',
};
