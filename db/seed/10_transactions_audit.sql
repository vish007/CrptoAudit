-- Seed audit log entries for various actions

INSERT INTO audit_logs (
  id, user_id, user_email, action, resource_type, resource_id, details, ip_address, user_agent, status, timestamp
) VALUES

-- User login events
(
  'k60e8400-e29b-41d4-a716-446655440001'::uuid,
  '650e8400-e29b-41d4-a716-446655440001'::uuid,
  'admin1@simplyfi.io',
  'read',
  'auth',
  '650e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('method', 'password', 'mfa_verified', true),
  '192.168.1.100',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
  'success',
  NOW() - interval '10 hours'
),

-- Engagement creation
(
  'k60e8400-e29b-41d4-a716-446655440002'::uuid,
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  'auditor1@big4.io',
  'create',
  'engagements',
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('audit_date', '2024-01-15', 'engagement_type', 'full_audit', 'scope_asset_count', 5),
  '203.0.113.42',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '9 days'
),

-- Engagement status update
(
  'k60e8400-e29b-41d4-a716-446655440003'::uuid,
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  'auditor1@big4.io',
  'update',
  'engagements',
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('from_status', 'planning', 'to_status', 'data_collection'),
  '203.0.113.42',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '8 days'
),

-- Asset verification
(
  'k60e8400-e29b-41d4-a716-446655440004'::uuid,
  '750e8400-e29b-41d4-a716-446655440011'::uuid,
  'auditor2@big4.io',
  'create',
  'blockchain_verification',
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('assets_verified', 5, 'total_balance_usd', 15234567.89),
  '203.0.113.43',
  'Mozilla/5.0 (X11; Linux x86_64)',
  'success',
  NOW() - interval '7 days'
),

-- Merkle tree generation
(
  'k60e8400-e29b-41d4-a716-446655440005'::uuid,
  '750e8400-e29b-41d4-a716-446655440011'::uuid,
  'auditor2@big4.io',
  'create',
  'merkle_trees',
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('leaf_count', 4250, 'tree_depth', 12),
  '203.0.113.43',
  'Mozilla/5.0 (X11; Linux x86_64)',
  'success',
  NOW() - interval '6 days'
),

-- Report generation
(
  'k60e8400-e29b-41d4-a716-446655440006'::uuid,
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  'auditor1@big4.io',
  'create',
  'reports',
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('report_type', 'por', 'pages', 45),
  '203.0.113.42',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '5 days'
),

-- Engagement completed
(
  'k60e8400-e29b-41d4-a716-446655440007'::uuid,
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  'auditor1@big4.io',
  'update',
  'engagements',
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('from_status', 'reporting', 'to_status', 'completed', 'reserve_ratio', 102.3),
  '203.0.113.42',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '4 days'
),

-- User role assignment
(
  'k60e8400-e29b-41d4-a716-446655440008'::uuid,
  '650e8400-e29b-41d4-a716-446655440001'::uuid,
  'admin1@simplyfi.io',
  'update',
  'user_roles',
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  jsonb_build_object('assigned_role', 'Audit Manager', 'role_id', '750e8400-e29b-41d4-a716-440655440010'::uuid),
  '192.168.1.100',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
  'success',
  NOW() - interval '8 days'
),

-- Tenant settings update
(
  'k60e8400-e29b-41d4-a716-446655440009'::uuid,
  '850e8400-e29b-41d4-a716-446655440001'::uuid,
  'compliance@kraken.io',
  'update',
  'tenants',
  '550e8400-e29b-41d4-a716-446655440010'::uuid,
  jsonb_build_object('setting', 'min_reserve_threshold', 'old_value', 95.0, 'new_value', 100.0),
  '198.51.100.23',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0)',
  'success',
  NOW() - interval '6 days'
),

-- Wallet address verification
(
  'k60e8400-e29b-41d4-a716-446655440010'::uuid,
  '750e8400-e29b-41d4-a716-446655440012'::uuid,
  'auditor3@big4.io',
  'create',
  'wallet_verification',
  'f60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('blockchain', 'bitcoin', 'address_hash', '1a1z7agoat2LRGH3EiJjP73yq6fsKSvxzu', 'balance_verified', true),
  '203.0.113.44',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '5 days'
),

-- Export request
(
  'k60e8400-e29b-41d4-a716-446655440011'::uuid,
  '850e8400-e29b-41d4-a716-446655440004'::uuid,
  'compliance@coinbase.io',
  'export',
  'engagements',
  'e60e8400-e29b-41d4-a716-446655440002'::uuid,
  jsonb_build_object('format', 'csv', 'records_exported', 250),
  '198.51.100.24',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
  'success',
  NOW() - interval '3 days'
),

-- AI analysis execution
(
  'k60e8400-e29b-41d4-a716-446655440012'::uuid,
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  'auditor1@big4.io',
  'create',
  'ai_analysis',
  'e60e8400-e29b-41d4-a716-446655440002'::uuid,
  jsonb_build_object('analysis_type', 'anomaly_detection', 'anomalies_found', 3),
  '203.0.113.42',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '2 days'
),

-- Failed login attempt
(
  'k60e8400-e29b-41d4-a716-446655440013'::uuid,
  '750e8400-e29b-41d4-a716-446655440001'::uuid,
  'auditor1@big4.io',
  'read',
  'auth',
  '750e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('reason', 'invalid_password', 'attempt_number', 1),
  '192.0.2.42',
  'Mozilla/5.0 (Android 12; Mobile)',
  'failure',
  NOW() - interval '1 day'
),

-- Data import
(
  'k60e8400-e29b-41d4-a716-446655440014'::uuid,
  '850e8400-e29b-41d4-a716-446655440002'::uuid,
  'audit@kraken.io',
  'create',
  'onboarding_import',
  '550e8400-e29b-41d4-a716-446655440010'::uuid,
  jsonb_build_object('import_type', 'wallets', 'records_imported', 32, 'records_failed', 0),
  '198.51.100.25',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '7 days'
),

-- User account deactivation
(
  'k60e8400-e29b-41d4-a716-446655440015'::uuid,
  '650e8400-e29b-41d4-a716-446655440001'::uuid,
  'admin1@simplyfi.io',
  'update',
  'users',
  '750e8400-e29b-41d4-a716-446655440005'::uuid,
  jsonb_build_object('from_status', 'active', 'to_status', 'inactive', 'reason', 'Employee termination'),
  '192.168.1.100',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
  'success',
  NOW() - interval '5 days'
),

-- Permission check
(
  'k60e8400-e29b-41d4-a716-446655440016'::uuid,
  '750e8400-e29b-41d4-a716-446655440030'::uuid,
  'supervisor1@fca.gov.uk',
  'read',
  'admin_dashboard',
  '550e8400-e29b-41d4-a716-446655440020'::uuid,
  jsonb_build_object('permission_check', 'admin_dashboard', 'approved', true),
  '203.0.113.100',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '2 days'
),

-- Compliance check execution
(
  'k60e8400-e29b-41d4-a716-446655440017'::uuid,
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  'auditor1@big4.io',
  'create',
  'compliance_check',
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('compliance_framework', 'VARA', 'compliant', true),
  '203.0.113.42',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '3 days'
),

-- Bulk asset import
(
  'k60e8400-e29b-41d4-a716-446655440018'::uuid,
  '650e8400-e29b-41d4-a716-446655440002'::uuid,
  'admin2@simplyfi.io',
  'create',
  'assets',
  NULL,
  jsonb_build_object('assets_imported', 153, 'import_source', 'seed_data'),
  '192.168.1.101',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
  'success',
  NOW() - interval '14 days'
),

-- Report download
(
  'k60e8400-e29b-41d4-a716-446655440019'::uuid,
  '850e8400-e29b-41d4-a716-446655440001'::uuid,
  'compliance@kraken.io',
  'export',
  'reports',
  NULL,
  jsonb_build_object('report_type', 'por', 'file_size_mb', 2.5),
  '198.51.100.26',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
  'success',
  NOW() - interval '1 day'
),

-- AI narrative generation
(
  'k60e8400-e29b-41d4-a716-446655440020'::uuid,
  '750e8400-e29b-41d4-a716-446655440010'::uuid,
  'auditor1@big4.io',
  'create',
  'ai_narrative',
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  jsonb_build_object('section', 'executive_summary', 'word_count', 450),
  '203.0.113.42',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'success',
  NOW() - interval '4 days'
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource_type ON audit_logs(resource_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_status ON audit_logs(status);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
