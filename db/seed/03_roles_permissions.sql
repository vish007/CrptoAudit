-- Seed system roles and permissions

-- Insert permissions first
INSERT INTO permissions (
  id, name, resource, action, description, created_at
) VALUES
-- User permissions
('550e8400-e29b-41d4-a716-440655440001'::uuid, 'view_users', 'users', 'read', 'View user accounts', NOW()),
('550e8400-e29b-41d4-a716-440655440002'::uuid, 'create_users', 'users', 'create', 'Create new user accounts', NOW()),
('550e8400-e29b-41d4-a716-440655440003'::uuid, 'edit_users', 'users', 'update', 'Edit user information', NOW()),
('550e8400-e29b-41d4-a716-440655440004'::uuid, 'delete_users', 'users', 'delete', 'Deactivate user accounts', NOW()),

-- Tenant permissions
('550e8400-e29b-41d4-a716-440655440010'::uuid, 'view_tenants', 'tenants', 'read', 'View tenant information', NOW()),
('550e8400-e29b-41d4-a716-440655440011'::uuid, 'create_tenants', 'tenants', 'create', 'Create new tenants', NOW()),
('550e8400-e29b-41d4-a716-440655440012'::uuid, 'edit_tenants', 'tenants', 'update', 'Edit tenant settings', NOW()),
('550e8400-e29b-41d4-a716-440655440013'::uuid, 'manage_tenant_members', 'tenants', 'update', 'Manage tenant membership', NOW()),

-- Engagement permissions
('550e8400-e29b-41d4-a716-440655440020'::uuid, 'view_engagements', 'engagements', 'read', 'View engagement details', NOW()),
('550e8400-e29b-41d4-a716-440655440021'::uuid, 'create_engagements', 'engagements', 'create', 'Create audit engagements', NOW()),
('550e8400-e29b-41d4-a716-440655440022'::uuid, 'edit_engagements', 'engagements', 'update', 'Edit engagement settings', NOW()),
('550e8400-e29b-41d4-a716-440655440023'::uuid, 'delete_engagements', 'engagements', 'delete', 'Delete engagements', NOW()),
('550e8400-e29b-41d4-a716-440655440024'::uuid, 'update_engagement_status', 'engagements', 'update', 'Update engagement status', NOW()),

-- Asset permissions
('550e8400-e29b-41d4-a716-440655440030'::uuid, 'view_assets', 'assets', 'read', 'View crypto assets', NOW()),
('550e8400-e29b-41d4-a716-440655440031'::uuid, 'create_assets', 'assets', 'create', 'Create crypto assets', NOW()),
('550e8400-e29b-41d4-a716-440655440032'::uuid, 'edit_assets', 'assets', 'update', 'Edit asset information', NOW()),
('550e8400-e29b-41d4-a716-440655440033'::uuid, 'import_assets', 'assets', 'create', 'Bulk import assets', NOW()),

-- Reserve permissions
('550e8400-e29b-41d4-a716-440655440040'::uuid, 'view_reserves', 'reserves', 'read', 'View reserve ratios and summaries', NOW()),
('550e8400-e29b-41d4-a716-440655440041'::uuid, 'calculate_reserves', 'reserves', 'create', 'Calculate reserve ratios', NOW()),
('550e8400-e29b-41d4-a716-440655440042'::uuid, 'verify_segregation', 'reserves', 'create', 'Verify fund segregation', NOW()),

-- Merkle permissions
('550e8400-e29b-41d4-a716-440655440050'::uuid, 'view_merkle', 'merkle', 'read', 'View Merkle tree data', NOW()),
('550e8400-e29b-41d4-a716-440655440051'::uuid, 'generate_merkle', 'merkle', 'create', 'Generate Merkle trees', NOW()),
('550e8400-e29b-41d4-a716-440655440052'::uuid, 'verify_merkle', 'merkle', 'create', 'Verify Merkle proofs', NOW()),

-- Blockchain permissions
('550e8400-e29b-41d4-a716-440655440060'::uuid, 'view_blockchain', 'blockchain', 'read', 'View blockchain verification data', NOW()),
('550e8400-e29b-41d4-a716-440655440061'::uuid, 'verify_balances', 'blockchain', 'create', 'Verify on-chain balances', NOW()),
('550e8400-e29b-41d4-a716-440655440062'::uuid, 'verify_addresses', 'blockchain', 'create', 'Verify wallet addresses', NOW()),

-- Report permissions
('550e8400-e29b-41d4-a716-440655440070'::uuid, 'view_reports', 'reports', 'read', 'View audit reports', NOW()),
('550e8400-e29b-41d4-a716-440655440071'::uuid, 'generate_reports', 'reports', 'create', 'Generate reports', NOW()),
('550e8400-e29b-41d4-a716-440655440072'::uuid, 'export_reports', 'reports', 'export', 'Export report data', NOW()),

-- AI permissions
('550e8400-e29b-41d4-a716-440655440080'::uuid, 'use_ai_analysis', 'ai', 'create', 'Use AI anomaly analysis', NOW()),
('550e8400-e29b-41d4-a716-440655440081'::uuid, 'generate_narratives', 'ai', 'create', 'Generate AI narratives', NOW()),
('550e8400-e29b-41d4-a716-440655440082'::uuid, 'ai_chat', 'ai', 'create', 'Use AI chat assistant', NOW()),

-- Admin permissions
('550e8400-e29b-41d4-a716-440655440090'::uuid, 'view_audit_log', 'admin', 'read', 'View system audit logs', NOW()),
('550e8400-e29b-41d4-a716-440655440091'::uuid, 'manage_roles', 'admin', 'update', 'Manage roles and permissions', NOW()),
('550e8400-e29b-41d4-a716-440655440092'::uuid, 'admin_dashboard', 'admin', 'read', 'Access admin dashboard', NOW()),

-- Onboarding permissions
('550e8400-e29b-41d4-a716-440655440100'::uuid, 'onboarding_register', 'onboarding', 'create', 'Register for platform', NOW()),
('550e8400-e29b-41d4-a716-440655440101'::uuid, 'onboarding_import', 'onboarding', 'create', 'Import onboarding data', NOW()),

-- Global permissions
('550e8400-e29b-41d4-a716-440655440110'::uuid, 'view_dashboard', 'dashboard', 'read', 'View tenant dashboard', NOW()),
('550e8400-e29b-41d4-a716-440655440111'::uuid, 'export_data', 'data', 'export', 'Export engagement data', NOW()),
('550e8400-e29b-41d4-a716-440655440112'::uuid, 'manage_settings', 'settings', 'update', 'Manage account settings', NOW());

-- Insert system roles
INSERT INTO roles (
  id, name, type, description, created_at, updated_at
) VALUES
-- System Admin - has all permissions
('750e8400-e29b-41d4-a716-440655440001'::uuid, 'System Administrator', 'system', 'Full platform access and system administration', NOW(), NOW()),

-- Auditor roles
('750e8400-e29b-41d4-a716-440655440010'::uuid, 'Audit Manager', 'system', 'Manages audit engagements and generates reports', NOW(), NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, 'Audit Senior', 'system', 'Conducts audit fieldwork and verification', NOW(), NOW()),
('750e8400-e29b-41d4-a716-440655440012'::uuid, 'Audit Junior', 'system', 'Supports audit procedures under supervision', NOW(), NOW()),

-- VASP roles
('750e8400-e29b-41d4-a716-440655440020'::uuid, 'VASP Compliance Officer', 'system', 'Manages VASP compliance and audit coordination', NOW(), NOW()),
('750e8400-e29b-41d4-a716-440655440021'::uuid, 'VASP Treasury Manager', 'system', 'Manages asset wallets and reserves', NOW(), NOW()),

-- Regulator role
('750e8400-e29b-41d4-a716-440655440030'::uuid, 'Regulatory Supervisor', 'system', 'Supervises VASPs and reviews audits', NOW(), NOW());

-- Assign permissions to System Administrator role
INSERT INTO role_permissions (role_id, permission_id, created_at)
SELECT '750e8400-e29b-41d4-a716-440655440001'::uuid, id, NOW()
FROM permissions
WHERE id IN (
  SELECT id FROM permissions
);

-- Assign permissions to Audit Manager
INSERT INTO role_permissions (role_id, permission_id, created_at)
VALUES
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440021'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440022'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440024'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440040'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440041'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440050'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440051'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440060'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440061'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440070'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440071'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440072'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440080'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440081'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440110'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440010'::uuid, '550e8400-e29b-41d4-a716-440655440111'::uuid, NOW());

-- Assign permissions to Audit Senior
INSERT INTO role_permissions (role_id, permission_id, created_at)
VALUES
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440040'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440041'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440050'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440051'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440060'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440061'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440070'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440080'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440011'::uuid, '550e8400-e29b-41d4-a716-440655440110'::uuid, NOW());

-- Assign permissions to Audit Junior
INSERT INTO role_permissions (role_id, permission_id, created_at)
VALUES
('750e8400-e29b-41d4-a716-440655440012'::uuid, '550e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440012'::uuid, '550e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440012'::uuid, '550e8400-e29b-41d4-a716-440655440040'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440012'::uuid, '550e8400-e29b-41d4-a716-440655440050'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440012'::uuid, '550e8400-e29b-41d4-a716-440655440060'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440012'::uuid, '550e8400-e29b-41d4-a716-440655440070'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440012'::uuid, '550e8400-e29b-41d4-a716-440655440110'::uuid, NOW());

-- Assign permissions to VASP Compliance Officer
INSERT INTO role_permissions (role_id, permission_id, created_at)
VALUES
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440033'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440040'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440050'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440070'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440100'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440101'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440110'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440020'::uuid, '550e8400-e29b-41d4-a716-440655440112'::uuid, NOW());

-- Assign permissions to VASP Treasury Manager
INSERT INTO role_permissions (role_id, permission_id, created_at)
VALUES
('750e8400-e29b-41d4-a716-440655440021'::uuid, '550e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440021'::uuid, '550e8400-e29b-41d4-a716-440655440040'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440021'::uuid, '550e8400-e29b-41d4-a716-440655440060'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440021'::uuid, '550e8400-e29b-41d4-a716-440655440062'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440021'::uuid, '550e8400-e29b-41d4-a716-440655440110'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440021'::uuid, '550e8400-e29b-41d4-a716-440655440112'::uuid, NOW());

-- Assign permissions to Regulatory Supervisor
INSERT INTO role_permissions (role_id, permission_id, created_at)
VALUES
('750e8400-e29b-41d4-a716-440655440030'::uuid, '550e8400-e29b-41d4-a716-440655440010'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440030'::uuid, '550e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440030'::uuid, '550e8400-e29b-41d4-a716-440655440070'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440030'::uuid, '550e8400-e29b-41d4-a716-440655440090'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440030'::uuid, '550e8400-e29b-41d4-a716-440655440110'::uuid, NOW()),
('750e8400-e29b-41d4-a716-440655440030'::uuid, '550e8400-e29b-41d4-a716-440655440111'::uuid, NOW());

-- Assign roles to users
-- System admins
INSERT INTO user_roles (user_id, role_id, created_at)
VALUES
('650e8400-e29b-41d4-a716-446655440001'::uuid, '750e8400-e29b-41d4-a716-440655440001'::uuid, NOW()),
('650e8400-e29b-41d4-a716-446655440002'::uuid, '750e8400-e29b-41d4-a716-440655440001'::uuid, NOW()),
('650e8400-e29b-41d4-a716-446655440003'::uuid, '750e8400-e29b-41d4-a716-440655440001'::uuid, NOW()),
('650e8400-e29b-41d4-a716-446655440004'::uuid, '750e8400-e29b-41d4-a716-440655440001'::uuid, NOW()),
('650e8400-e29b-41d4-a716-446655440005'::uuid, '750e8400-e29b-41d4-a716-440655440001'::uuid, NOW()),
-- Auditors from Big4 - mix of managers and seniors
('750e8400-e29b-41d4-a716-446655440001'::uuid, '750e8400-e29b-41d4-a716-440655440010'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440002'::uuid, '750e8400-e29b-41d4-a716-440655440011'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440003'::uuid, '750e8400-e29b-41d4-a716-440655440012'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440004'::uuid, '750e8400-e29b-41d4-a716-440655440011'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440005'::uuid, '750e8400-e29b-41d4-a716-440655440012'::uuid, NOW()),
-- Auditors from Crypto Compliance
('750e8400-e29b-41d4-a716-446655440006'::uuid, '750e8400-e29b-41d4-a716-440655440010'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440007'::uuid, '750e8400-e29b-41d4-a716-440655440011'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440008'::uuid, '750e8400-e29b-41d4-a716-440655440012'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440009'::uuid, '750e8400-e29b-41d4-a716-440655440011'::uuid, NOW()),
('750e8400-e29b-41d4-a716-446655440010'::uuid, '750e8400-e29b-41d4-a716-440655440012'::uuid, NOW()),
-- VASP users - compliance and treasury
('850e8400-e29b-41d4-a716-446655440001'::uuid, '750e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440002'::uuid, '750e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440003'::uuid, '750e8400-e29b-41d4-a716-440655440021'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440004'::uuid, '750e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440005'::uuid, '750e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440006'::uuid, '750e8400-e29b-41d4-a716-440655440021'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440007'::uuid, '750e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440008'::uuid, '750e8400-e29b-41d4-a716-440655440020'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440009'::uuid, '750e8400-e29b-41d4-a716-440655440021'::uuid, NOW()),
('850e8400-e29b-41d4-a716-446655440010'::uuid, '750e8400-e29b-41d4-a716-440655440021'::uuid, NOW()),
-- Regulators
('a50e8400-e29b-41d4-a716-446655440001'::uuid, '750e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('a50e8400-e29b-41d4-a716-446655440002'::uuid, '750e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('a50e8400-e29b-41d4-a716-446655440003'::uuid, '750e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('a50e8400-e29b-41d4-a716-446655440004'::uuid, '750e8400-e29b-41d4-a716-440655440030'::uuid, NOW()),
('a50e8400-e29b-41d4-a716-446655440005'::uuid, '750e8400-e29b-41d4-a716-440655440030'::uuid, NOW());

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_roles_type ON roles(type);
CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_id ON user_roles(role_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id ON role_permissions(role_id);
