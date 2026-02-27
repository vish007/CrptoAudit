-- Seed customer liabilities: 50 customers × 5 assets each = 250 records
-- Mix of spot, margin, earn, staking accounts

-- Engagement 1 Kraken (customers 1-10)
INSERT INTO customer_liabilities (
  id, engagement_id, customer_account_id, customer_label, asset_symbol, account_type, reported_balance, balance_usd, verified, notes, created_at
) VALUES

-- Customer 1 - 5 assets
('g60e8400-e29b-41d4-a716-446655440001'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_001', 'Customer A1', 'BTC', 'spot', '2.5432', 105928.45, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440002'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_001', 'Customer A1', 'ETH', 'spot', '25.6789', 38508.45, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440003'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_001', 'Customer A1', 'USDT', 'earning', '50000.00', 50000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440004'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_001', 'Customer A1', 'USDC', 'spot', '25000.00', 25000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440005'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_001', 'Customer A1', 'SOL', 'staking', '150.2345', 32924.51, false, NULL, NOW()),

-- Customer 2
('g60e8400-e29b-41d4-a716-446655440006'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_002', 'Customer A2', 'BTC', 'spot', '5.1234', 213523.48, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440007'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_002', 'Customer A2', 'ETH', 'margin', '100.5678', 150852.30, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440008'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_002', 'Customer A2', 'USDT', 'spot', '75000.00', 75000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440009'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_002', 'Customer A2', 'USDC', 'earning', '100000.00', 100000.00, false, 'Interest accruing', NOW()),
('g60e8400-e29b-41d4-a716-446655440010'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_002', 'Customer A2', 'SOL', 'spot', '500.0000', 109500.00, true, NULL, NOW()),

-- Customer 3
('g60e8400-e29b-41d4-a716-446655440011'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_003', 'Customer A3', 'BTC', 'earning', '1.2345', 51405.12, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440012'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_003', 'Customer A3', 'ETH', 'staking', '50.2345', 75351.75, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440013'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_003', 'Customer A3', 'USDT', 'spot', '10000.00', 10000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440014'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_003', 'Customer A3', 'USDC', 'margin', '50000.00', 50000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440015'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_003', 'Customer A3', 'SOL', 'spot', '250.1234', 54775.50, false, NULL, NOW()),

-- Customer 4
('g60e8400-e29b-41d4-a716-446655440016'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_004', 'Customer A4', 'BTC', 'spot', '0.5000', 20830.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440017'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_004', 'Customer A4', 'ETH', 'spot', '10.0000', 15010.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440018'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_004', 'Customer A4', 'USDT', 'earning', '5000.00', 5000.00, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440019'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_004', 'Customer A4', 'USDC', 'spot', '0.00', 0.00, true, 'Zero balance', NOW()),
('g60e8400-e29b-41d4-a716-446655440020'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_004', 'Customer A4', 'SOL', 'spot', '0.0001', 0.02, true, 'Very small balance', NOW()),

-- Customer 5
('g60e8400-e29b-41d4-a716-446655440021'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_005', 'Customer A5', 'BTC', 'spot', '8.2345', 342865.45, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440022'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_005', 'Customer A5', 'ETH', 'staking', '75.5432', 113314.80, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440023'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_005', 'Customer A5', 'USDT', 'spot', '200000.00', 200000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440024'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_005', 'Customer A5', 'USDC', 'earning', '150000.00', 150000.00, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440025'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_005', 'Customer A5', 'SOL', 'spot', '1200.5678', 263084.26, true, NULL, NOW()),

-- Customer 6
('g60e8400-e29b-41d4-a716-446655440026'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_006', 'Customer A6', 'BTC', 'margin', '3.5432', 147514.25, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440027'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_006', 'Customer A6', 'ETH', 'spot', '45.2345', 67851.75, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440028'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_006', 'Customer A6', 'USDT', 'spot', '30000.00', 30000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440029'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_006', 'Customer A6', 'USDC', 'margin', '25000.00', 25000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440030'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_006', 'Customer A6', 'SOL', 'staking', '400.1234', 87626.94, false, NULL, NOW()),

-- Customer 7
('g60e8400-e29b-41d4-a716-446655440031'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_007', 'Customer A7', 'BTC', 'spot', '12.4567', 518500.79, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440032'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_007', 'Customer A7', 'ETH', 'earning', '200.3456', 300520.40, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440033'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_007', 'Customer A7', 'USDT', 'spot', '500000.00', 500000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440034'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_007', 'Customer A7', 'USDC', 'spot', '250000.00', 250000.00, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440035'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_007', 'Customer A7', 'SOL', 'spot', '2000.0000', 438000.00, true, NULL, NOW()),

-- Customer 8
('g60e8400-e29b-41d4-a716-446655440036'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_008', 'Customer A8', 'BTC', 'spot', '0.1234', 5138.42, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440037'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_008', 'Customer A8', 'ETH', 'margin', '5.2345', 7851.75, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440038'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_008', 'Customer A8', 'USDT', 'earning', '2000.00', 2000.00, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440039'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_008', 'Customer A8', 'USDC', 'spot', '1500.00', 1500.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440040'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_008', 'Customer A8', 'SOL', 'spot', '50.5432', 11068.94, true, NULL, NOW()),

-- Customer 9
('g60e8400-e29b-41d4-a716-446655440041'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_009', 'Customer A9', 'BTC', 'earning', '4.5678', 190289.84, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440042'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_009', 'Customer A9', 'ETH', 'spot', '67.8901', 101834.01, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440043'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_009', 'Customer A9', 'USDT', 'spot', '75000.00', 75000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440044'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_009', 'Customer A9', 'USDC', 'margin', '100000.00', 100000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440045'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_009', 'Customer A9', 'SOL', 'staking', '800.1234', 175307.54, false, NULL, NOW()),

-- Customer 10
('g60e8400-e29b-41d4-a716-446655440046'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_010', 'Customer A10', 'BTC', 'spot', '2.9876', 124425.82, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440047'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_010', 'Customer A10', 'ETH', 'spot', '35.6789', 53503.35, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440048'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_010', 'Customer A10', 'USDT', 'earning', '45000.00', 45000.00, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440049'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_010', 'Customer A10', 'USDC', 'spot', '50000.00', 50000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440050'::uuid, 'e60e8400-e29b-41d4-a716-446655440001'::uuid, 'kraken_cust_010', 'Customer A10', 'SOL', 'spot', '350.2345', 76701.13, true, NULL, NOW());

-- Engagement 2: Coinbase customers (11-20 with XRP focus)
INSERT INTO customer_liabilities (
  id, engagement_id, customer_account_id, customer_label, asset_symbol, account_type, reported_balance, balance_usd, verified, notes, created_at
) VALUES
('g60e8400-e29b-41d4-a716-446655440051'::uuid, 'e60e8400-e29b-41d4-a716-446655440002'::uuid, 'coinbase_cust_001', 'Customer B1', 'XRP', 'spot', '10000.0000', 5500.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440052'::uuid, 'e60e8400-e29b-41d4-a716-446655440002'::uuid, 'coinbase_cust_001', 'Customer B1', 'BTC', 'spot', '0.5000', 20830.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440053'::uuid, 'e60e8400-e29b-41d4-a716-446655440002'::uuid, 'coinbase_cust_001', 'Customer B1', 'ETH', 'staking', '5.0000', 7505.00, false, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440054'::uuid, 'e60e8400-e29b-41d4-a716-446655440002'::uuid, 'coinbase_cust_001', 'Customer B1', 'USDT', 'spot', '15000.00', 15000.00, true, NULL, NOW()),
('g60e8400-e29b-41d4-a716-446655440055'::uuid, 'e60e8400-e29b-41d4-a716-446655440002'::uuid, 'coinbase_cust_001', 'Customer B1', 'USDC', 'earning', '10000.00', 10000.00, true, NULL, NOW());

-- Continue with more customers (21-50) - abbreviated for brevity
-- Generate patterns for customers 2-10 (additional 9 × 5 = 45 records)

INSERT INTO customer_liabilities (id, engagement_id, customer_account_id, customer_label, asset_symbol, account_type, reported_balance, balance_usd, verified, notes, created_at)
SELECT
  gen_random_uuid()::uuid,
  'e60e8400-e29b-41d4-a716-446655440002'::uuid,
  'coinbase_cust_' || LPAD((i/5 + 1)::text, 3, '0'),
  'Customer B' || (i/5 + 1),
  ARRAY['XRP', 'BTC', 'ETH', 'USDT', 'USDC'][((i % 5) + 1)],
  ARRAY['spot', 'margin', 'earning', 'staking', 'other'][((i % 5) + 1)],
  (random() * 100000)::numeric(15,4),
  (random() * 100000)::numeric(15,2),
  (random() > 0.1)::boolean,
  CASE WHEN (random() > 0.8) THEN 'Flagged for review' ELSE NULL END,
  NOW()
FROM generate_series(0, 44) AS t(i)
ON CONFLICT DO NOTHING;

-- Engagement 3: Celsius customers (21-30)
INSERT INTO customer_liabilities (id, engagement_id, customer_account_id, customer_label, asset_symbol, account_type, reported_balance, balance_usd, verified, notes, created_at)
SELECT
  gen_random_uuid()::uuid,
  'e60e8400-e29b-41d4-a716-446655440003'::uuid,
  'celsius_cust_' || LPAD((i/5 + 1)::text, 3, '0'),
  'Customer C' || (i/5 + 1),
  ARRAY['BTC', 'ETH', 'DAI', 'USDC', 'SOL'][((i % 5) + 1)],
  ARRAY['earning', 'staking', 'spot', 'lending', 'other'][((i % 5) + 1)],
  (random() * 50000)::numeric(15,4),
  (random() * 50000)::numeric(15,2),
  (random() > 0.15)::boolean,
  NULL,
  NOW()
FROM generate_series(0, 49) AS t(i)
ON CONFLICT DO NOTHING;

-- Engagements 4-5: Mixed customers
INSERT INTO customer_liabilities (id, engagement_id, customer_account_id, customer_label, asset_symbol, account_type, reported_balance, balance_usd, verified, notes, created_at)
SELECT
  gen_random_uuid()::uuid,
  (ARRAY['e60e8400-e29b-41d4-a716-446655440004'::uuid, 'e60e8400-e29b-41d4-a716-446655440005'::uuid])[1 + (i / 50)],
  'cust_' || LPAD(i::text, 4, '0'),
  'Customer ' || i,
  ARRAY['BTC', 'ETH', 'USDT', 'USDC', 'SOL'][((i % 5) + 1)],
  ARRAY['spot', 'margin', 'earning', 'staking', 'other'][((i % 5) + 1)],
  (random() * 150000)::numeric(15,4),
  (random() * 150000)::numeric(15,2),
  (random() > 0.12)::boolean,
  CASE WHEN (random() > 0.85) THEN 'Large position - requires verification' ELSE NULL END,
  NOW()
FROM generate_series(1, 100) AS t(i)
WHERE i <= 100
ON CONFLICT DO NOTHING;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_customer_liabilities_engagement_id ON customer_liabilities(engagement_id);
CREATE INDEX IF NOT EXISTS idx_customer_liabilities_customer_account_id ON customer_liabilities(customer_account_id);
CREATE INDEX IF NOT EXISTS idx_customer_liabilities_asset_symbol ON customer_liabilities(asset_symbol);
CREATE INDEX IF NOT EXISTS idx_customer_liabilities_verified ON customer_liabilities(verified);
