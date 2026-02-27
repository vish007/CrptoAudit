-- Seed Merkle tree data for completed engagement

INSERT INTO merkle_trees (
  id, engagement_id, root_hash, leaf_count, tree_depth, hash_algorithm, created_at, updated_at
) VALUES
(
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'e60e8400-e29b-41d4-a716-446655440001'::uuid,
  'a1f2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b',
  4250,
  12,
  'SHA256',
  NOW(),
  NOW()
);

-- Insert sample Merkle proofs for customers
INSERT INTO merkle_proofs (
  id, merkle_tree_id, customer_id, balance, leaf_index, proof, created_at
) VALUES
-- Customer 1 proof
(
  'i60e8400-e29b-41d4-a716-446655440001'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_001',
  '113432.96',
  0,
  ARRAY[
    'c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5',
    'd6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6',
    'e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7'
  ]::text[],
  NOW()
),
-- Customer 2 proof
(
  'i60e8400-e29b-41d4-a716-446655440002'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_002',
  '328852.30',
  1,
  ARRAY[
    'f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8',
    'a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9',
    'b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0'
  ]::text[],
  NOW()
),
-- Customer 3 proof
(
  'i60e8400-e29b-41d4-a716-446655440003'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_003',
  '136126.87',
  2,
  ARRAY[
    'c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1',
    'd2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2',
    'e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3'
  ]::text[],
  NOW()
),
-- Customer 4 proof
(
  'i60e8400-e29b-41d4-a716-446655440004'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_004',
  '36340.02',
  3,
  ARRAY[
    'f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4',
    'a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5'
  ]::text[],
  NOW()
),
-- Customer 5 proof
(
  'i60e8400-e29b-41d4-a716-446655440005'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_005',
  '706399.06',
  4,
  ARRAY[
    'b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6',
    'c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7',
    'd8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8'
  ]::text[],
  NOW()
),
-- Customer 6 proof
(
  'i60e8400-e29b-41d4-a716-446655440006'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_006',
  '88851.94',
  5,
  ARRAY[
    'e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9',
    'f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0'
  ]::text[],
  NOW()
),
-- Customer 7 proof
(
  'i60e8400-e29b-41d4-a716-446655440007'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_007',
  '1051021.19',
  6,
  ARRAY[
    'a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1',
    'b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2'
  ]::text[],
  NOW()
),
-- Customer 8 proof
(
  'i60e8400-e29b-41d4-a716-446655440008'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_008',
  '9360.11',
  7,
  ARRAY[
    'c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3',
    'd4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4'
  ]::text[],
  NOW()
),
-- Customer 9 proof
(
  'i60e8400-e29b-41d4-a716-446655440009'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_009',
  '280923.54',
  8,
  ARRAY[
    'e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5',
    'f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6'
  ]::text[],
  NOW()
),
-- Customer 10 proof
(
  'i60e8400-e29b-41d4-a716-446655440010'::uuid,
  'h60e8400-e29b-41d4-a716-446655440001'::uuid,
  'kraken_cust_010',
  '198904.48',
  9,
  ARRAY[
    'a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7',
    'b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8'
  ]::text[],
  NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_merkle_trees_engagement_id ON merkle_trees(engagement_id);
CREATE INDEX IF NOT EXISTS idx_merkle_proofs_merkle_tree_id ON merkle_proofs(merkle_tree_id);
CREATE INDEX IF NOT EXISTS idx_merkle_proofs_customer_id ON merkle_proofs(customer_id);
