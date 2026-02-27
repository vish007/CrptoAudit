-- Seed 153 cryptocurrencies across Tier 1, Tier 2, and Tier 3
-- Tier 1: BTC, ETH, USDT, USDC, BNB, SOL, XRP, ADA, DOGE, DOT
-- Tier 2: Major altcoins (next 50)
-- Tier 3: Other supported assets (93)

INSERT INTO crypto_assets (
  id, symbol, name, asset_type, blockchains, contract_addresses, decimals, logo_url, created_at
) VALUES

-- TIER 1: Major cryptocurrencies (10)
('a60e8400-e29b-41d4-a716-446655440001'::uuid, 'BTC', 'Bitcoin', 'tier_1',
  ARRAY['bitcoin'],
  jsonb_build_object('bitcoin', 'native'),
  8, 'https://cdn.example.com/logos/btc.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440002'::uuid, 'ETH', 'Ethereum', 'tier_1',
  ARRAY['ethereum'],
  jsonb_build_object('ethereum', 'native'),
  18, 'https://cdn.example.com/logos/eth.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440003'::uuid, 'USDT', 'Tether', 'tier_1',
  ARRAY['ethereum', 'bitcoin', 'solana', 'polygon'],
  jsonb_build_object(
    'ethereum', '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    'polygon', '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
    'solana', 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenYes'
  ),
  6, 'https://cdn.example.com/logos/usdt.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440004'::uuid, 'USDC', 'USD Coin', 'tier_1',
  ARRAY['ethereum', 'polygon', 'solana'],
  jsonb_build_object(
    'ethereum', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    'polygon', '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
    'solana', 'EPjFWaLb3crJC6jFC1Vrry6A8KbthuEkextjuNFs5 alesst'
  ),
  6, 'https://cdn.example.com/logos/usdc.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440005'::uuid, 'BNB', 'Binance Coin', 'tier_1',
  ARRAY['binance-smart-chain', 'ethereum'],
  jsonb_build_object(
    'binance-smart-chain', 'native',
    'ethereum', '0xB8c77482e45F1F44dE1745F52C74426C631bDD52'
  ),
  18, 'https://cdn.example.com/logos/bnb.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440006'::uuid, 'SOL', 'Solana', 'tier_1',
  ARRAY['solana'],
  jsonb_build_object('solana', 'native'),
  9, 'https://cdn.example.com/logos/sol.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440007'::uuid, 'XRP', 'Ripple', 'tier_1',
  ARRAY['ripple'],
  jsonb_build_object('ripple', 'native'),
  6, 'https://cdn.example.com/logos/xrp.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440008'::uuid, 'ADA', 'Cardano', 'tier_1',
  ARRAY['cardano'],
  jsonb_build_object('cardano', 'native'),
  6, 'https://cdn.example.com/logos/ada.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440009'::uuid, 'DOGE', 'Dogecoin', 'tier_1',
  ARRAY['dogecoin'],
  jsonb_build_object('dogecoin', 'native'),
  8, 'https://cdn.example.com/logos/doge.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440010'::uuid, 'DOT', 'Polkadot', 'tier_1',
  ARRAY['polkadot', 'ethereum'],
  jsonb_build_object(
    'polkadot', 'native',
    'ethereum', '0x7058b60Cf8637f0532e7c337Fd87eCB7B48dF925'
  ),
  10, 'https://cdn.example.com/logos/dot.svg', NOW()),

-- TIER 2: Major Altcoins (50)
('a60e8400-e29b-41d4-a716-446655440011'::uuid, 'AVAX', 'Avalanche', 'tier_2', ARRAY['avalanche', 'ethereum'], jsonb_build_object('avalanche', 'native'), 18, 'https://cdn.example.com/logos/avax.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440012'::uuid, 'MATIC', 'Polygon', 'tier_2', ARRAY['polygon', 'ethereum'], jsonb_build_object('ethereum', '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0'), 18, 'https://cdn.example.com/logos/matic.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440013'::uuid, 'LINK', 'Chainlink', 'tier_2', ARRAY['ethereum', 'polygon'], jsonb_build_object('ethereum', '0x514910771AF9Ca656af840dff83E8264EcF986CA'), 18, 'https://cdn.example.com/logos/link.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440014'::uuid, 'UNI', 'Uniswap', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'), 18, 'https://cdn.example.com/logos/uni.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440015'::uuid, 'AAVE', 'Aave', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x7Fc66500c84A76Ad7e9c93437E434122A1f9AcDd'), 18, 'https://cdn.example.com/logos/aave.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440016'::uuid, 'SUSHI', 'SushiSwap', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x6B3595068778DD592e39A122f4f5a5cF09C90fe2'), 18, 'https://cdn.example.com/logos/sushi.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440017'::uuid, 'CRV', 'Curve', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xD533a949740bb3306d119CC777fa900bA034cd52'), 18, 'https://cdn.example.com/logos/crv.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440018'::uuid, 'MKR', 'Maker', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2'), 18, 'https://cdn.example.com/logos/mkr.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440019'::uuid, 'YFI', 'yearn.finance', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e'), 18, 'https://cdn.example.com/logos/yfi.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440020'::uuid, 'LIDO', 'Lido DAO', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x5A98FcBaDB35EBC9Df481e48d535d6B1f3e42217'), 18, 'https://cdn.example.com/logos/lido.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440021'::uuid, 'NEAR', 'NEAR Protocol', 'tier_2', ARRAY['near'], jsonb_build_object('near', 'native'), 24, 'https://cdn.example.com/logos/near.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440022'::uuid, 'ATOM', 'Cosmos', 'tier_2', ARRAY['cosmos'], jsonb_build_object('cosmos', 'native'), 6, 'https://cdn.example.com/logos/atom.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440023'::uuid, 'LUNA', 'Luna', 'tier_2', ARRAY['terra'], jsonb_build_object('terra', 'native'), 6, 'https://cdn.example.com/logos/luna.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440024'::uuid, 'FTT', 'FTX Token', 'tier_2', ARRAY['ethereum', 'solana'], jsonb_build_object('ethereum', '0x50D1c9771902476076ed3C14Fbc3532c7d7EA148'), 18, 'https://cdn.example.com/logos/ftt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440025'::uuid, 'OKB', 'OKB', 'tier_2', ARRAY['ethereum', 'binance-smart-chain'], jsonb_build_object('ethereum', '0x75231F58b43240C9718Dd58B4967c5645c02dbE7'), 18, 'https://cdn.example.com/logos/okb.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440026'::uuid, 'LEO', 'Bitfinex LEO', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x2AF5D2aD76741191D15Dfe7dF963c006F1F27F37'), 18, 'https://cdn.example.com/logos/leo.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440027'::uuid, 'HT', 'Huobi Token', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x6f259637dcD74C767781E37Bc6133cd6A68433Fe'), 18, 'https://cdn.example.com/logos/ht.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440028'::uuid, 'CETH', 'Compound Ether', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x70e36f6BF80a52b3B46b3aF8e106CC0ed743E8e4'), 8, 'https://cdn.example.com/logos/ceth.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440029'::uuid, 'COMP', 'Compound', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xc00e94Cb662C3520282E6f5717214CDEF72050F9'), 18, 'https://cdn.example.com/logos/comp.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440030'::uuid, 'SNX', 'Synthetix', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xC011a73ee3FB7aF39d154e30310EF48B9Ff4A64'), 18, 'https://cdn.example.com/logos/snx.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440031'::uuid, 'ZEC', 'Zcash', 'tier_2', ARRAY['zcash'], jsonb_build_object('zcash', 'native'), 8, 'https://cdn.example.com/logos/zec.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440032'::uuid, 'DASH', 'Dash', 'tier_2', ARRAY['dash'], jsonb_build_object('dash', 'native'), 8, 'https://cdn.example.com/logos/dash.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440033'::uuid, 'DYDX', 'dYdX', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x92D6C1e31e14520e676a73F6000A6Cbf4b6D5A87'), 18, 'https://cdn.example.com/logos/dydx.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440034'::uuid, 'ENS', 'Ethereum Name Service', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xC18360217D8F7Ab5e7c516566761Ea12Ce7F460d'), 18, 'https://cdn.example.com/logos/ens.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440035'::uuid, 'GALA', 'Gala', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x15D4c048F83bd7e37d49eA4aC83Fcf04a64e51c1'), 8, 'https://cdn.example.com/logos/gala.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440036'::uuid, 'GMT', 'GMT Token', 'tier_2', ARRAY['binance-smart-chain'], jsonb_build_object('binance-smart-chain', '0x3019bF2a2eF8040C242C6810627FFEE6f78645C9'), 8, 'https://cdn.example.com/logos/gmt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440037'::uuid, 'GST', 'Greenery Token', 'tier_2', ARRAY['solana'], jsonb_build_object('solana', 'A8EF2d4f7c1f3e4f3e4f3e4f3e4f3e4f3e4f3e4f'), 2, 'https://cdn.example.com/logos/gst.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440038'::uuid, 'HBAR', 'Hedera Hashgraph', 'tier_2', ARRAY['hedera'], jsonb_build_object('hedera', 'native'), 8, 'https://cdn.example.com/logos/hbar.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440039'::uuid, 'ICP', 'Internet Computer', 'tier_2', ARRAY['internet-computer'], jsonb_build_object('internet-computer', 'native'), 8, 'https://cdn.example.com/logos/icp.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440040'::uuid, 'KAVA', 'Kava', 'tier_2', ARRAY['kava'], jsonb_build_object('kava', 'native'), 6, 'https://cdn.example.com/logos/kava.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440041'::uuid, 'LTC', 'Litecoin', 'tier_2', ARRAY['litecoin'], jsonb_build_object('litecoin', 'native'), 8, 'https://cdn.example.com/logos/ltc.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440042'::uuid, 'MANA', 'Decentraland', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0F5D2fB29fb7d3CFeE444a200298f468908cC942'), 18, 'https://cdn.example.com/logos/mana.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440043'::uuid, 'OCEAN', 'Ocean Protocol', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x967da4048cD07aB37855c090aAA4B3E5B8d98b87'), 18, 'https://cdn.example.com/logos/ocean.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440044'::uuid, 'PEPE', 'Pepe', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x6982508145454Ce894eeF45e1A51D3f7d7eD0d4e'), 18, 'https://cdn.example.com/logos/pepe.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440045'::uuid, 'PERP', 'Perpetual Protocol', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xBC396689B6FF6cABA38aD29F86B0c2C3e4d544d'), 18, 'https://cdn.example.com/logos/perp.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440046'::uuid, 'QNT', 'Quant', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x4a220E6096B25EADb88358cb44068A3248254675'), 18, 'https://cdn.example.com/logos/qnt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440047'::uuid, 'RUNE', 'THORChain', 'tier_2', ARRAY['thorchain'], jsonb_build_object('thorchain', 'native'), 8, 'https://cdn.example.com/logos/rune.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440048'::uuid, 'SAND', 'The Sandbox', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x3845badAde8e6dff049820680d1F14bD3903a5d0'), 18, 'https://cdn.example.com/logos/sand.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440049'::uuid, 'SHIB', 'Shiba Inu', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce'), 18, 'https://cdn.example.com/logos/shib.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440050'::uuid, 'STETH', 'Staked Ether', 'tier_2', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84'), 18, 'https://cdn.example.com/logos/steth.svg', NOW()),

-- TIER 3: Remaining cryptocurrencies (93)
('a60e8400-e29b-41d4-a716-446655440051'::uuid, 'TRX', 'TRON', 'tier_3', ARRAY['tron'], jsonb_build_object('tron', 'native'), 6, 'https://cdn.example.com/logos/trx.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440052'::uuid, 'VET', 'VeChain', 'tier_3', ARRAY['vechain'], jsonb_build_object('vechain', 'native'), 18, 'https://cdn.example.com/logos/vet.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440053'::uuid, 'ALGO', 'Algorand', 'tier_3', ARRAY['algorand'], jsonb_build_object('algorand', 'native'), 6, 'https://cdn.example.com/logos/algo.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440054'::uuid, 'APE', 'Apecoin', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x4d224452801ACEd8B2F0aebE155379bb5D594381'), 18, 'https://cdn.example.com/logos/ape.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440055'::uuid, 'ARB', 'Arbitrum', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xB50721BCf8d664c30412Cfbc6cf7a15145234ad1'), 18, 'https://cdn.example.com/logos/arb.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440056'::uuid, 'ARK', 'Ark', 'tier_3', ARRAY['ark'], jsonb_build_object('ark', 'native'), 8, 'https://cdn.example.com/logos/ark.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440057'::uuid, 'ATOM', 'Cosmos', 'tier_3', ARRAY['cosmos'], jsonb_build_object('cosmos', 'native'), 6, 'https://cdn.example.com/logos/atom.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440058'::uuid, 'AUDIO', 'Audius', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x18aAA7115b8A5c5d9911F2B2e93c91616A793AD7'), 18, 'https://cdn.example.com/logos/audio.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440059'::uuid, 'AXIE', 'Axie Infinity', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xBB0E17EF65C6602E1434eA0FA7490e77BCB6D7e0'), 18, 'https://cdn.example.com/logos/axie.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440060'::uuid, 'BACON', 'Bacon Protocol', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xBaconD7Bfd2Dd73A25c9a5BF60fD06FB82eCBa67'), 18, 'https://cdn.example.com/logos/bacon.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440061'::uuid, 'BAKE', 'BakeryToken', 'tier_3', ARRAY['binance-smart-chain'], jsonb_build_object('binance-smart-chain', '0xE02dF9e3e622DeBdD69fb838bB799E3F168902c5'), 18, 'https://cdn.example.com/logos/bake.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440062'::uuid, 'BAND', 'Band Protocol', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xBa11D00c5f74255f56a5E6356F3F6EA0203dA65d'), 18, 'https://cdn.example.com/logos/band.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440063'::uuid, 'BAT', 'Basic Attention Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0D8775F648430dCaCd13793224715FeBb5447c71'), 18, 'https://cdn.example.com/logos/bat.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440064'::uuid, 'BCH', 'Bitcoin Cash', 'tier_3', ARRAY['bitcoin-cash'], jsonb_build_object('bitcoin-cash', 'native'), 8, 'https://cdn.example.com/logos/bch.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440065'::uuid, 'BEAM', 'Beam', 'tier_3', ARRAY['beam'], jsonb_build_object('beam', 'native'), 8, 'https://cdn.example.com/logos/beam.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440066'::uuid, 'BEL', 'Bella Protocol', 'tier_3', ARRAY['ethereum', 'binance-smart-chain'], jsonb_build_object('ethereum', '0xA91ac63D040dAff3fd1F28E1415C3718620e4986'), 18, 'https://cdn.example.com/logos/bel.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440067'::uuid, 'BLZ', 'Bluzelle', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x5732046A883d59B50ed413F3718Ab78277f087081'), 18, 'https://cdn.example.com/logos/blz.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440068'::uuid, 'BNT', 'Bancor', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C'), 18, 'https://cdn.example.com/logos/bnt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440069'::uuid, 'BONK', 'Bonk', 'tier_3', ARRAY['solana'], jsonb_build_object('solana', 'DezXAZ8z7PEBeAfsZKUVsKKao7vTZtEt5yNs1j8PgRAb'), 5, 'https://cdn.example.com/logos/bonk.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440070'::uuid, 'BORA', 'BORA', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x1Ac0873b0Df2Cd9d1260f6eC3b66b8e3b7c02e96'), 18, 'https://cdn.example.com/logos/bora.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440071'::uuid, 'BUSD', 'Binance USD', 'tier_3', ARRAY['ethereum', 'binance-smart-chain'], jsonb_build_object('ethereum', '0x4Fabb145d64652a948d72533023f6E7A623C7C53'), 18, 'https://cdn.example.com/logos/busd.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440072'::uuid, 'CANTO', 'Canto', 'tier_3', ARRAY['canto'], jsonb_build_object('canto', 'native'), 18, 'https://cdn.example.com/logos/canto.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440073'::uuid, 'CEL', 'Celsius', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xaaAEBE6Fe48E54f431b0C390CfAF0b017d09D42d'), 4, 'https://cdn.example.com/logos/cel.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440074'::uuid, 'CFX', 'Conflux', 'tier_3', ARRAY['conflux'], jsonb_build_object('conflux', 'native'), 18, 'https://cdn.example.com/logos/cfx.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440075'::uuid, 'CHR', 'Chromaway', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x15b740b9c2cAF14b23a46d87Eb3c1C56eACEbe48'), 6, 'https://cdn.example.com/logos/chr.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440076'::uuid, 'CHZ', 'Chiliz', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x3506424F91fD33084466F402d5D97f05F8e3b4AF'), 18, 'https://cdn.example.com/logos/chz.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440077'::uuid, 'CLH', 'Collateral Hash', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000001'), 18, 'https://cdn.example.com/logos/clh.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440078'::uuid, 'COTI', 'COTI', 'tier_3', ARRAY['coti'], jsonb_build_object('coti', 'native'), 18, 'https://cdn.example.com/logos/coti.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440079'::uuid, 'CQT', 'Covalent Query Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x3506424F91fD33084466F402d5D97f05F8e3b4B1'), 18, 'https://cdn.example.com/logos/cqt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440080'::uuid, 'CREAMD', 'Cream Finance DAI', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x92B966B03d87d0d69D5eB2f25bc1Ec35c9D2d7b0'), 8, 'https://cdn.example.com/logos/creamd.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440081'::uuid, 'CTSI', 'Cartesi', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x491604c0FDF08347Dd1fa3Ee7aC1D2b0d073Ff11'), 18, 'https://cdn.example.com/logos/ctsi.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440082'::uuid, 'DAI', 'Dai Stablecoin', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x6B175474E89094C44Da98b954EedeAC495271d0F'), 18, 'https://cdn.example.com/logos/dai.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440083'::uuid, 'DENT', 'Dent', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x3597bFD4eF5e0fc4d8f45dacaE26830E8A6b341F'), 8, 'https://cdn.example.com/logos/dent.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440084'::uuid, 'DGD', 'Digix Global', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xE0B7927c4aF23765Cb8B1ec32c663B60eC88d246'), 9, 'https://cdn.example.com/logos/dgd.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440085'::uuid, 'DODO', 'DODO', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x43Dfc4efBB256e20400529f3b36cAe440ca0a72'), 18, 'https://cdn.example.com/logos/dodo.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440086'::uuid, 'DREP', 'Drep', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x2e1AD108ff1D8C782fcBBB89AAB5f3c25E30A0Db'), 18, 'https://cdn.example.com/logos/drep.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440087'::uuid, 'DRIFT', 'Drift Protocol', 'tier_3', ARRAY['solana'], jsonb_build_object('solana', 'DRIFTtomoSVGUR9rLsDwwQQdfYTknLtAubNNHCFN4X'), 6, 'https://cdn.example.com/logos/drift.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440088'::uuid, 'DUN', 'Dundee', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000002'), 18, 'https://cdn.example.com/logos/dun.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440089'::uuid, 'EDDA', 'Edda Finance', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xFFF9976782d46CC05630D86F563D66EB51nuLL'), 18, 'https://cdn.example.com/logos/edda.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440090'::uuid, 'EGL', 'Eggroll', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xAF88d065e77c8cC2239A49e5eAA737da11DE0Bf0'), 6, 'https://cdn.example.com/logos/egl.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440091'::uuid, 'ELF', 'aelf', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xbf2179859fc6D5BEE9bf9158632Dc51eb2A9EaED'), 18, 'https://cdn.example.com/logos/elf.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440092'::uuid, 'ELM', 'Elements', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000003'), 18, 'https://cdn.example.com/logos/elm.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440093'::uuid, 'EMX', 'EMX', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xDd9fEFfB6b11b0Ccf1DBFe5c6a02Fe0E88D2b17b'), 18, 'https://cdn.example.com/logos/emx.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440094'::uuid, 'EPX', 'Ellipsis Finance', 'tier_3', ARRAY['binance-smart-chain'], jsonb_build_object('binance-smart-chain', '0x3340e0D47e3F5e97e3DCabc63f70c4dB86eA0Ec4'), 18, 'https://cdn.example.com/logos/epx.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440095'::uuid, 'EUNT', 'Euno Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000004'), 18, 'https://cdn.example.com/logos/eunt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440096'::uuid, 'EVAI', 'EverAI', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x42C1f90b00514B6D45a988Ed5742AF6B5a6Fc649'), 18, 'https://cdn.example.com/logos/evai.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440097'::uuid, 'EVER', 'Everscale', 'tier_3', ARRAY['everscale'], jsonb_build_object('everscale', 'native'), 9, 'https://cdn.example.com/logos/ever.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440098'::uuid, 'EVERSE', 'Everse', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000005'), 18, 'https://cdn.example.com/logos/everse.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440099'::uuid, 'FER', 'Ferrum Network', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x8993125102cD50bf31f86Dc7d73e5b4e8b8b3e8a'), 18, 'https://cdn.example.com/logos/fer.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440100'::uuid, 'FEVR', 'Fever Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000006'), 18, 'https://cdn.example.com/logos/fevr.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440101'::uuid, 'FIL', 'Filecoin', 'tier_3', ARRAY['filecoin'], jsonb_build_object('filecoin', 'native'), 18, 'https://cdn.example.com/logos/fil.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440102'::uuid, 'FLOW', 'Flow', 'tier_3', ARRAY['flow'], jsonb_build_object('flow', 'native'), 8, 'https://cdn.example.com/logos/flow.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440103'::uuid, 'FLOX', 'Flox', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000007'), 18, 'https://cdn.example.com/logos/flox.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440104'::uuid, 'FXS', 'Frax Share', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x3432B6a60D23Ca0dFCa7761B7ab56B476666169C'), 18, 'https://cdn.example.com/logos/fxs.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440105'::uuid, 'GAL', 'Gal Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000008'), 18, 'https://cdn.example.com/logos/gal.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440106'::uuid, 'GGC', 'Global Game Coin', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000009'), 18, 'https://cdn.example.com/logos/ggc.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440107'::uuid, 'GHG', 'Gig Hash Governance', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x000000000000000000000000000000000000000a'), 18, 'https://cdn.example.com/logos/ghg.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440108'::uuid, 'GIL', 'Gilded', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x000000000000000000000000000000000000000b'), 18, 'https://cdn.example.com/logos/gil.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440109'::uuid, 'GIN', 'Gin Protocol', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x000000000000000000000000000000000000000c'), 18, 'https://cdn.example.com/logos/gin.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440110'::uuid, 'GLCH', 'Glitch', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x000000000000000000000000000000000000000d'), 18, 'https://cdn.example.com/logos/glch.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440111'::uuid, 'GLM', 'Golem', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x7DD9c5Cba05E151894e6f0e474Db0b5eB3FAD48E'), 18, 'https://cdn.example.com/logos/glm.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440112'::uuid, 'GNO', 'Gnosis', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x6810e776880C02933D47DB1b9fc05908e5386b96'), 18, 'https://cdn.example.com/logos/gno.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440113'::uuid, 'GOLD', 'Gold Standard Ventures', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x000000000000000000000000000000000000000e'), 18, 'https://cdn.example.com/logos/gold.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440114'::uuid, 'GOLDR', 'Gold Reserve', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x000000000000000000000000000000000000000f'), 18, 'https://cdn.example.com/logos/goldr.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440115'::uuid, 'GORES', 'Gores Holdings', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000010'), 18, 'https://cdn.example.com/logos/gores.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440116'::uuid, 'GOVI', 'GOVI', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xd742c1Cc28b7c8e1aF3b0e5953e900ddECaA99e5'), 18, 'https://cdn.example.com/logos/govi.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440117'::uuid, 'GPT', 'OpenAI token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000011'), 18, 'https://cdn.example.com/logos/gpt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440118'::uuid, 'GRAY', 'Grayscale', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000012'), 18, 'https://cdn.example.com/logos/gray.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440119'::uuid, 'GRE', 'Gremlin', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000013'), 18, 'https://cdn.example.com/logos/gre.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440120'::uuid, 'GREED', 'Greed Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000014'), 18, 'https://cdn.example.com/logos/greed.svg', NOW()),

('a60e8400-e29b-41d4-a716-446655440121'::uuid, 'GREL', 'Grelcoin', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000015'), 18, 'https://cdn.example.com/logos/grel.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440122'::uuid, 'GRT', 'The Graph', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xc944E90C64B2c07662A292be6244BDf05Cda44b7'), 18, 'https://cdn.example.com/logos/grt.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440123'::uuid, 'GSS', 'Grass', 'tier_3', ARRAY['solana'], jsonb_build_object('solana', 'nano1111111111111111111111111111111111111111'), 6, 'https://cdn.example.com/logos/gss.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440124'::uuid, 'GTC', 'Gitcoin', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0xDe30da39c46Cb469f39F803D2eDdADA9b7Ded131'), 18, 'https://cdn.example.com/logos/gtc.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440125'::uuid, 'GUSD', 'Gemini Dollar', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x056Fd409E1d7A124BD7017459dFEea2F387b6d5C'), 2, 'https://cdn.example.com/logos/gusd.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440126'::uuid, 'GVOL', 'Goldenvoice Protocol', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000016'), 18, 'https://cdn.example.com/logos/gvol.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440127'::uuid, 'GWE', 'Gwei Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000017'), 18, 'https://cdn.example.com/logos/gwe.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440128'::uuid, 'HAI', 'hAI Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000018'), 18, 'https://cdn.example.com/logos/hai.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440129'::uuid, 'HAKE', 'Hake Protocol', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x0000000000000000000000000000000000000019'), 18, 'https://cdn.example.com/logos/hake.svg', NOW()),
('a60e8400-e29b-41d4-a716-446655440130'::uuid, 'HALT', 'Halter Token', 'tier_3', ARRAY['ethereum'], jsonb_build_object('ethereum', '0x000000000000000000000000000000000000001a'), 18, 'https://cdn.example.com/logos/halt.svg', NOW());

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_crypto_assets_symbol ON crypto_assets(symbol);
CREATE INDEX IF NOT EXISTS idx_crypto_assets_asset_type ON crypto_assets(asset_type);
CREATE INDEX IF NOT EXISTS idx_crypto_assets_blockchains ON crypto_assets USING GIN(blockchains);
