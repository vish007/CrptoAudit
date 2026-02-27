-- Seed initial tenants
-- 2 auditor tenants, 3 VASP tenants, 1 regulator

INSERT INTO tenants (
  id, name, type, vara_license_number, description, logo_url, status, settings, created_at, updated_at
) VALUES
-- Auditor Tenants
(
  '550e8400-e29b-41d4-a716-446655440001'::uuid,
  'Big4 Auditors LLP',
  'auditor',
  NULL,
  'Global audit firm specializing in crypto asset verification',
  'https://cdn.example.com/logos/big4.svg',
  'active',
  jsonb_build_object(
    'timezone', 'UTC',
    'currency', 'USD',
    'min_reserve_threshold', 100.0,
    'critical_reserve_threshold', 95.0
  ),
  NOW(),
  NOW()
),
(
  '550e8400-e29b-41d4-a716-446655440002'::uuid,
  'Crypto Compliance Partners',
  'auditor',
  NULL,
  'Specialized crypto compliance and audit services',
  'https://cdn.example.com/logos/crypto-compliance.svg',
  'active',
  jsonb_build_object(
    'timezone', 'UTC',
    'currency', 'USD',
    'min_reserve_threshold', 100.0,
    'critical_reserve_threshold', 95.0
  ),
  NOW(),
  NOW()
),

-- VASP Tenants
(
  '550e8400-e29b-41d4-a716-446655440010'::uuid,
  'Kraken',
  'vasp',
  'VARA-2023-001',
  'Leading cryptocurrency exchange with billions in AUM',
  'https://cdn.example.com/logos/kraken.svg',
  'active',
  jsonb_build_object(
    'timezone', 'America/Los_Angeles',
    'currency', 'USD',
    'business_model', 'exchange',
    'aum_usd', 15000000000.0,
    'customer_count', 5000000,
    'countries', jsonb_build_array('US', 'EU', 'JP', 'SG')
  ),
  NOW(),
  NOW()
),
(
  '550e8400-e29b-41d4-a716-446655440011'::uuid,
  'Coinbase',
  'vasp',
  'VARA-2023-002',
  'US-regulated cryptocurrency exchange',
  'https://cdn.example.com/logos/coinbase.svg',
  'active',
  jsonb_build_object(
    'timezone', 'America/New_York',
    'currency', 'USD',
    'business_model', 'exchange',
    'aum_usd', 18000000000.0,
    'customer_count', 8000000,
    'countries', jsonb_build_array('US', 'EU', 'CA')
  ),
  NOW(),
  NOW()
),
(
  '550e8400-e29b-41d4-a716-446655440012'::uuid,
  'Celsius Network',
  'vasp',
  'VARA-2023-003',
  'Decentralized finance lending platform',
  'https://cdn.example.com/logos/celsius.svg',
  'active',
  jsonb_build_object(
    'timezone', 'America/New_York',
    'currency', 'USD',
    'business_model', 'lending',
    'aum_usd', 8000000000.0,
    'customer_count', 1500000,
    'countries', jsonb_build_array('US', 'EU')
  ),
  NOW(),
  NOW()
),

-- Regulator Tenant
(
  '550e8400-e29b-41d4-a716-446655440020'::uuid,
  'Financial Conduct Authority',
  'regulator',
  NULL,
  'UK financial regulator',
  'https://cdn.example.com/logos/fca.svg',
  'active',
  jsonb_build_object(
    'timezone', 'Europe/London',
    'currency', 'GBP',
    'jurisdiction', 'UK'
  ),
  NOW(),
  NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_tenants_type ON tenants(type);
CREATE INDEX IF NOT EXISTS idx_tenants_status ON tenants(status);
CREATE INDEX IF NOT EXISTS idx_tenants_vara_license ON tenants(vara_license_number);
