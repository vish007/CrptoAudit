/**
 * @typedef {Object} User
 * @property {string} id - User ID (UUID)
 * @property {string} email - User email address
 * @property {string} firstName - First name
 * @property {string} lastName - Last name
 * @property {string} role - User role (ROLES constant)
 * @property {string} tenantId - Associated tenant ID
 * @property {string[]} permissions - Array of permission strings
 * @property {boolean} isActive - Account active status
 * @property {string} profileImage - Profile image URL
 * @property {Date} lastLogin - Last login timestamp
 * @property {Date} createdAt - Account creation timestamp
 * @property {Date} updatedAt - Last update timestamp
 */

/**
 * @typedef {Object} AuthState
 * @property {User|null} user - Current authenticated user
 * @property {string|null} token - JWT access token
 * @property {string|null} refreshToken - Refresh token
 * @property {boolean} isLoading - Loading state
 * @property {string|null} error - Error message
 * @property {boolean} isAuthenticated - Authentication status
 */

/**
 * @typedef {Object} Tenant
 * @property {string} id - Tenant ID (UUID)
 * @property {string} name - Tenant name
 * @property {string} type - Tenant type (vasp, regulator, auditor, etc)
 * @property {string} status - Tenant status (active, inactive, suspended)
 * @property {string} logoUrl - Logo URL
 * @property {string|null} description - Tenant description
 * @property {Object} settings - Tenant configuration settings
 * @property {number} maxEngagements - Maximum concurrent engagements
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Update timestamp
 */

/**
 * @typedef {Object} Engagement
 * @property {string} id - Engagement ID (UUID)
 * @property {string} tenantId - Associated tenant ID
 * @property {string} auditId - Associated audit ID
 * @property {string} status - Engagement status (ENGAGEMENT_STATUS)
 * @property {string} engagementType - Type of engagement (audit, review, assessment)
 * @property {Date} startDate - Engagement start date
 * @property {Date} endDate - Engagement end date (planned)
 * @property {Date} actualEndDate - Actual completion date
 * @property {Object} auditScope - Audit scope definition
 * @property {string[]} auditableAssets - List of assets to be audited
 * @property {string[]} assignedAuditors - Auditor IDs assigned
 * @property {string} engagementManager - Manager user ID
 * @property {Object} progress - Progress tracking
 * @property {number} completionPercentage - Overall completion percentage
 * @property {string|null} notes - Internal notes
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Update timestamp
 */

/**
 * @typedef {Object} Asset
 * @property {string} id - Asset ID (UUID)
 * @property {string} engagementId - Associated engagement ID
 * @property {string} name - Asset name/label
 * @property {string} assetType - Asset type (ASSET_TYPES)
 * @property {string} status - Asset status (ASSET_STATUS)
 * @property {string} symbol - Asset symbol (BTC, ETH, USD, etc)
 * @property {number} quantity - Asset quantity
 * @property {number} unitPrice - Unit price in USD
 * @property {number} totalValue - Total value in USD
 * @property {string} blockchain - Blockchain network (if crypto)
 * @property {string} address - Wallet/address (if applicable)
 * @property {string|null} txHash - Transaction hash for verification
 * @property {Date} assetDate - Asset date/snapshot date
 * @property {Object} metadata - Additional metadata
 * @property {string} submittedBy - User ID who submitted
 * @property {string|null} verifiedBy - Auditor ID who verified
 * @property {Date|null} verifiedAt - Verification timestamp
 * @property {string|null} verificationNotes - Verification notes
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Update timestamp
 */

/**
 * @typedef {Object} MerkleTree
 * @property {string} id - Merkle tree ID (UUID)
 * @property {string} engagementId - Associated engagement ID
 * @property {string} status - Tree status (pending, submitted, verified)
 * @property {string} merkleRoot - Root hash of the tree
 * @property {number} leafCount - Number of leaves in tree
 * @property {number} depth - Depth of the tree
 * @property {Object[]} leaves - Merkle tree leaves/data points
 * @property {Object} proofs - Merkle proofs for verification
 * @property {string} submittedBy - User ID who submitted
 * @property {string|null} verifiedBy - Auditor ID who verified
 * @property {Date|null} verifiedAt - Verification timestamp
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Update timestamp
 */

/**
 * @typedef {Object} BlockchainData
 * @property {string} id - Blockchain data ID (UUID)
 * @property {string} engagementId - Associated engagement ID
 * @property {string} network - Blockchain network
 * @property {string} address - Wallet address being verified
 * @property {string} status - Data status (pending, confirmed, verified)
 * @property {number} balance - Current balance
 * @property {number} blockNumber - Latest block number checked
 * @property {string} txHash - Transaction hash
 * @property {Object[]} transactions - Transaction history
 * @property {Object} chainData - On-chain verification data
 * @property {Date|null} verifiedAt - Verification timestamp
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Update timestamp
 */

/**
 * @typedef {Object} Report
 * @property {string} id - Report ID (UUID)
 * @property {string} engagementId - Associated engagement ID
 * @property {string} reportType - Report type (REPORT_TYPE)
 * @property {string} status - Report status (REPORT_STATUS)
 * @property {string} title - Report title
 * @property {string} summary - Executive summary
 * @property {Object} findings - Audit findings
 * @property {Object} compliance - Compliance assessment results
 * @property {Object} financials - Financial data/summaries
 * @property {string} conclusion - Report conclusion
 * @property {string[]} attachments - Attachment file IDs
 * @property {string} preparedBy - Auditor/preparer user ID
 * @property {string|null} approvedBy - Approver user ID
 * @property {Date|null} approvedAt - Approval timestamp
 * @property {Date|null} publishedAt - Publication timestamp
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Update timestamp
 */

/**
 * @typedef {Object} Audit
 * @property {string} id - Audit ID (UUID)
 * @property {string} engagementId - Associated engagement ID
 * @property {string} status - Audit status (AUDIT_STATUS)
 * @property {string} auditType - Type of audit
 * @property {string[]} assignedAuditors - Auditor IDs
 * @property {Date} startDate - Audit start date
 * @property {Date|null} endDate - Audit end date
 * @property {Object} scope - Audit scope
 * @property {Object} findings - Audit findings
 * @property {Object[]} riskAssessments - Risk assessment data
 * @property {string} overallRiskRating - Overall risk rating
 * @property {string|null} notes - Audit notes
 * @property {Date} createdAt - Creation timestamp
 * @property {Date} updatedAt - Update timestamp
 */

/**
 * @typedef {Object} Notification
 * @property {string} id - Notification ID (UUID)
 * @property {string} userId - Target user ID
 * @property {string} type - Notification type (NOTIFICATION_TYPES)
 * @property {string} title - Notification title
 * @property {string} message - Notification message
 * @property {string|null} actionUrl - URL for action
 * @property {boolean} isRead - Read status
 * @property {Date} createdAt - Creation timestamp
 * @property {Date|null} readAt - Read timestamp
 */

/**
 * @typedef {Object} Permission
 * @property {string} id - Permission ID
 * @property {string} name - Permission name
 * @property {string} description - Permission description
 * @property {string} category - Permission category
 * @property {string[]} roles - Roles that have this permission
 */

/**
 * @typedef {Object} APIResponse
 * @property {boolean} success - Response success status
 * @property {*} data - Response data
 * @property {string|null} message - Response message
 * @property {Object|null} error - Error object
 * @property {number} statusCode - HTTP status code
 * @property {number|null} timestamp - Response timestamp
 */

/**
 * @typedef {Object} PaginatedResponse
 * @property {boolean} success - Response success status
 * @property {*[]} data - Array of data items
 * @property {Object} pagination - Pagination metadata
 * @property {number} pagination.total - Total items count
 * @property {number} pagination.page - Current page
 * @property {number} pagination.pageSize - Items per page
 * @property {number} pagination.totalPages - Total pages
 * @property {boolean} pagination.hasMore - Has more pages
 * @property {string|null} message - Response message
 */

/**
 * @typedef {Object} FormErrors
 * @property {string} [fieldName] - Error message for field
 */

/**
 * @typedef {Object} DashboardStats
 * @property {number} activeEngagements - Count of active engagements
 * @property {number} completedAudits - Count of completed audits
 * @property {number} totalAssetsUnderAudit - Total assets value
 * @property {number} complianceScore - Overall compliance score
 * @property {Object} assetBreakdown - Asset type breakdown
 * @property {Object} statusDistribution - Status distribution
 * @property {Object[]} recentActivity - Recent activity log
 */

/**
 * @typedef {Object} AIAgentTask
 * @property {string} id - Task ID (UUID)
 * @property {string} engagementId - Associated engagement ID
 * @property {string} taskType - Type of AI task
 * @property {string} status - Task status (pending, in_progress, completed, failed)
 * @property {Object} parameters - Task parameters
 * @property {*} result - Task result/output
 * @property {string|null} error - Error message if failed
 * @property {number} retries - Number of retries
 * @property {Date} createdAt - Creation timestamp
 * @property {Date|null} completedAt - Completion timestamp
 */

/**
 * @typedef {Object} AuditLog
 * @property {string} id - Log entry ID (UUID)
 * @property {string} userId - User who performed action
 * @property {string} action - Action performed
 * @property {string} resourceType - Type of resource affected
 * @property {string} resourceId - ID of affected resource
 * @property {Object|null} changes - Changes made
 * @property {string} ipAddress - IP address of requester
 * @property {string|null} userAgent - User agent string
 * @property {Date} createdAt - Timestamp of action
 */

export {};
