-- Seed 5 demo engagements at different stages

INSERT INTO engagements (
  id, vasp_tenant_id, auditor_tenant_id, status, audit_date, engagement_type, scope, notes, total_assets_usd, asset_count, wallet_count, customer_count, reserve_ratio, created_at, updated_at, completed_at
) VALUES

-- 1. Completed Engagement
(
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  '550e8400-e29b-41d4-a716-446655440010'::uuid,
  '550e8400-e29b-41d4-a716-446655440001'::uuid,
  'completed',
  '2024-01-15'::date,
  'full_audit',
  jsonb_build_object(
    'assets', jsonb_build_array('BTC', 'ETH', 'USDT', 'USDC', 'SOL'),
    'blockchains', jsonb_build_array('bitcoin', 'ethereum', 'solana')
  ),
  'Initial PoR audit for Kraken - comprehensive review of reserves and customer liabilities',
  15234567.89,
  5,
  32,
  4250,
  102.3,
  '2024-01-01'::timestamp,
  '2024-01-31'::timestamp,
  '2024-01-31'::timestamp
),

-- 2. Reporting Stage
(
  'e60e8400-e29b-41d4-a716-446655440002'::uuid,
  '550e8400-e29b-41d4-a716-446655440011'::uuid,
  '550e8400-e29b-41d4-a716-446655440001'::uuid,
  'reporting',
  '2024-02-01'::date,
  'full_audit',
  jsonb_build_object(
    'assets', jsonb_build_array('BTC', 'ETH', 'USDT', 'USDC', 'BNB'),
    'blockchains', jsonb_build_array('bitcoin', 'ethereum', 'binance-smart-chain')
  ),
  'Coinbase Q1 2024 PoR - Final verification and report generation underway',
  18567890.12,
  5,
  45,
  6700,
  103.1,
  '2024-01-20'::timestamp,
  '2024-02-20'::timestamp,
  NULL
),

-- 3. Verification Stage
(
  'e60e8400-e29b-41d4-a716-446655440003'::uuid,
  '550e8400-e29b-41d4-a716-446655440012'::uuid,
  '550e8400-e29b-41d4-a716-446655440002'::uuid,
  'verification',
  '2024-02-10'::date,
  'full_audit',
  jsonb_build_object(
    'assets', jsonb_build_array('BTC', 'ETH', 'DAI', 'USDC'),
    'blockchains', jsonb_build_array('ethereum')
  ),
  'Celsius Network DeFi reserve audit - Verification of Merkle tree and segregation',
  8123456.34,
  4,
  28,
  1800,
  101.8,
  '2024-02-01'::timestamp,
  '2024-02-15'::timestamp,
  NULL
),

-- 4. Data Collection Stage
(
  'e60e8400-e29b-41d4-a716-446655440004'::uuid,
  '550e8400-e29b-41d4-a716-446655440010'::uuid,
  '550e8400-e29b-41d4-a716-446655440002'::uuid,
  'data_collection',
  '2024-02-20'::date,
  'full_audit',
  jsonb_build_object(
    'assets', jsonb_build_array('BTC', 'ETH', 'USDT', 'XRP', 'ADA'),
    'blockchains', jsonb_build_array('bitcoin', 'ethereum', 'ripple', 'cardano')
  ),
  'Kraken Q2 2024 interim audit - Currently collecting wallet and liability data',
  22345678.56,
  5,
  62,
  8500,
  NULL,
  '2024-02-15'::timestamp,
  '2024-02-15'::timestamp,
  NULL
),

-- 5. Planning Stage
(
  'e60e8400-e29b-41d4-a716-446655440005'::uuid,
  '550e8400-e29b-41d4-a716-446655440011'::uuid,
  '550e8400-e29b-41d4-a716-446655440001'::uuid,
  'planning',
  '2024-03-15'::date,
  'full_audit',
  jsonb_build_object(
    'assets', jsonb_build_array('BTC', 'ETH', 'SOL', 'MATIC'),
    'blockchains', jsonb_build_array('bitcoin', 'ethereum', 'solana', 'polygon')
  ),
  'Coinbase Special Engagement - Audit scope and procedures being finalized',
  12987654.78,
  4,
  38,
  3200,
  NULL,
  '2024-02-15'::timestamp,
  '2024-02-15'::timestamp,
  NULL
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_engagements_status ON engagements(status);
CREATE INDEX IF NOT EXISTS idx_engagements_vasp_tenant_id ON engagements(vasp_tenant_id);
CREATE INDEX IF NOT EXISTS idx_engagements_auditor_tenant_id ON engagements(auditor_tenant_id);
CREATE INDEX IF NOT EXISTS idx_engagements_audit_date ON engagements(audit_date);
CREATE INDEX IF NOT EXISTS idx_engagements_created_at ON engagements(created_at);
