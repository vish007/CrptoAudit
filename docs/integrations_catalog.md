# SimplyFI PoR Platform: Integrations Catalog

**Document Version**: 1.0
**Last Updated**: February 2026
**Target Audience**: Engineering, DevOps, Integration Architects

---

## Table of Contents

1. [Blockchain Integrations](#blockchain-integrations)
2. [DeFi Protocol Integrations](#defi-protocol-integrations)
3. [Third-Party Custodian Integrations](#third-party-custodian-integrations)
4. [Notification Integrations](#notification-integrations)
5. [KYC & Identity Integrations](#kyc--identity-integrations)
6. [Monitoring & Observability Integrations](#monitoring--observability-integrations)
7. [Storage Integrations](#storage-integrations)

---

## Blockchain Integrations

### 1. Bitcoin (BTC)

**Supported Networks**: Bitcoin Mainnet, Testnet

**Primary Providers**:

#### Blockstream API
- **Endpoint**: `https://blockstream.info/api`
- **Authentication**: None (public API)
- **Rate Limit**: Unlimited (Blockstream's terms)
- **SLA**: 99.5% uptime
- **Health Check**: `GET /api/blocks/tip/hash`

**Request Examples**:

Get UTXO balance for address:
```bash
GET https://blockstream.info/api/address/bc1qz3khxnyq05mtp2v6ujjmqwg87fv5k6n3wpuqhd
```

Response:
```json
{
  "address": "bc1qz3khxnyq05mtp2v6ujjmqwg87fv5k6n3wpuqhd",
  "chain_stats": {
    "funded_txo_count": 10,
    "funded_txo_sum": 500000000,
    "spent_txo_count": 5,
    "spent_txo_sum": 250000000
  },
  "mempool_stats": {
    "funded_txo_count": 1,
    "funded_txo_sum": 10000000,
    "spent_txo_count": 0,
    "spent_txo_sum": 0
  }
}
```

Get transaction details:
```bash
GET https://blockstream.info/api/tx/{txid}
```

Response:
```json
{
  "txid": "abc123...",
  "version": 2,
  "locktime": 0,
  "vin": [
    {
      "txid": "prev_txid",
      "vout": 0,
      "witness": ["signature", "pubkey"]
    }
  ],
  "vout": [
    {
      "scriptpubkey": "bc1...",
      "scriptpubkey_asm": "OP_0 ...",
      "value": 100000000
    }
  ],
  "size": 250,
  "weight": 1000,
  "fee": 5000,
  "status": {
    "confirmed": true,
    "block_height": 850000,
    "block_hash": "0000...",
    "block_time": 1702000000
  }
}
```

#### Mempool.space API (Fallback)
- **Endpoint**: `https://mempool.space/api`
- **Authentication**: None (public API)
- **Rate Limit**: 10 requests/second (per IP)
- **SLA**: 99.0% uptime
- **Health Check**: `GET /api/v1/blocks/tip/height`

**Configuration**:
```python
# backend/app/core/config.py
BLOCKCHAIN_API_KEYS = {
    "bitcoin": {
        "primary": "blockstream",
        "fallback": ["mempool_space"],
        "timeout": 30
    }
}

# backend/app/services/blockchain/bitcoin_adapter.py
class BitcoinAdapter(BaseBlockchainAdapter):
    PRIMARY_PROVIDER = "https://blockstream.info/api"
    FALLBACK_PROVIDERS = [
        "https://mempool.space/api"
    ]

    async def verify_balance(self, address: str) -> Balance:
        """Verify Bitcoin UTXO balance."""
        try:
            # Try primary provider
            response = await self.query_blockstream(address)
            balance = response['chain_stats']['funded_txo_sum'] - \
                      response['chain_stats']['spent_txo_sum']
            return Balance(
                address=address,
                balance=balance,
                blockchain="Bitcoin",
                verified_at=datetime.utcnow(),
                block_height=await self.get_tip_height(),
                method="BLOCKSTREAM_API"
            )
        except Exception as e:
            # Fallback to Mempool.space
            logger.warning(f"Blockstream failed: {e}, trying Mempool")
            return await self.query_mempool(address)
```

**Error Handling**:
```python
# Circuit breaker pattern
CIRCUIT_BREAKER = {
    "failure_threshold": 5,
    "recovery_timeout": 300,  # 5 minutes
    "fallback_timeout": 30
}

# Retry policy
RETRY_POLICY = {
    "max_retries": 3,
    "backoff": "exponential",
    "base_delay": 1,  # seconds
    "max_delay": 30
}
```

---

### 2. Ethereum & EVM-Compatible Chains

**Supported Networks**: Ethereum Mainnet, Polygon, Arbitrum, Optimism, Base, BNB Chain, zkSync

**Primary Providers**:

#### Infura (Primary)
- **Endpoint**: `https://mainnet.infura.io/v3/{PROJECT_ID}`
- **Authentication**: API Key (PROJECT_ID)
- **Rate Limit**: 100 requests/second (paid tier)
- **SLA**: 99.9% uptime
- **Health Check**: `POST /` with JSON-RPC method `eth_blockNumber`

**Request Examples**:

Get account balance:
```bash
POST https://mainnet.infura.io/v3/YOUR_PROJECT_ID
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "eth_getBalance",
  "params": ["0x1234567890123456789012345678901234567890", "latest"],
  "id": 1
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x1bc16d674ec80000"
}
```

Get ERC-20 token balance:
```bash
POST https://mainnet.infura.io/v3/YOUR_PROJECT_ID
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "eth_call",
  "params": [
    {
      "to": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC contract
      "data": "0x70a08231000000000000000000000000{address}"  # balanceOf(address)
    },
    "latest"
  ],
  "id": 1
}
```

Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x0000000000000000000000000000000000000000000000000000000e8d4a51000"
}
```

#### Etherscan API (Fallback)
- **Endpoint**: `https://api.etherscan.io/api`
- **Authentication**: API Key (ETHERSCAN_API_KEY)
- **Rate Limit**: 5 calls/second
- **SLA**: 99.5% uptime
- **Health Check**: `GET /api?module=gastracker&action=gasoracle&apikey={KEY}`

#### Alchemy (Fallback)
- **Endpoint**: `https://eth-mainnet.alchemy.com/v2/{API_KEY}`
- **Authentication**: API Key
- **Rate Limit**: 300 requests/second (standard tier)
- **SLA**: 99.95% uptime

**Configuration**:
```python
# backend/app/core/config.py
BLOCKCHAIN_API_KEYS = {
    "ethereum": {
        "infura_key": "YOUR_INFURA_PROJECT_ID",
        "etherscan_key": "YOUR_ETHERSCAN_API_KEY",
        "alchemy_key": "YOUR_ALCHEMY_API_KEY",
        "providers": {
            "primary": "infura",
            "fallback": ["etherscan", "alchemy"],
            "timeout": 30
        }
    },
    "polygon": {
        "infura_key": "YOUR_INFURA_PROJECT_ID",
        "polygonscan_key": "YOUR_POLYGONSCAN_API_KEY",
        "providers": {
            "primary": "infura",
            "fallback": ["polygonscan"]
        }
    }
}

# backend/app/services/blockchain/ethereum_adapter.py
class EthereumAdapter(BaseBlockchainAdapter):
    async def verify_balance(self, address: str, token_address: Optional[str] = None) -> Balance:
        """Verify ETH or ERC-20 token balance."""
        if token_address:
            # ERC-20 token balance
            balance = await self.get_token_balance(address, token_address)
        else:
            # Native ETH balance
            balance = await self.get_eth_balance(address)

        return Balance(
            address=address,
            balance=balance,
            blockchain="Ethereum",
            verified_at=datetime.utcnow(),
            block_height=await self.get_block_number(),
            method="JSON_RPC"
        )

    async def get_token_balance(self, holder_address: str, token_contract: str) -> Decimal:
        """Query ERC-20 token balance using eth_call."""
        # Encode balanceOf(address) function call
        encoded_call = encode_packed(
            ["address"],
            [holder_address]
        )

        result = await self.json_rpc_call(
            "eth_call",
            {
                "to": token_contract,
                "data": f"0x70a08231{encoded_call}"
            },
            "latest"
        )

        # Decode result (uint256)
        return Decimal(int(result, 16))
```

---

### 3. Solana (SOL)

**Supported Networks**: Solana Mainnet

**Primary Provider**: Solana RPC

- **Endpoint**: `https://api.mainnet-beta.solana.com`
- **Backup Endpoints**:
  - `https://rpc.ankr.com/solana` (Ankr)
  - `https://solana-api.projectserum.com`
- **Authentication**: None (public RPC)
- **Rate Limit**: 100 requests/second
- **SLA**: 99.5% uptime
- **Health Check**: `POST /` with `getHealth` method

**Request Examples**:

Get account balance:
```bash
curl https://api.mainnet-beta.solana.com -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBalance",
    "params": ["4fYNw3dojWmq4dLFEday1r6z58VVzS1qaodJs1sPL2Z"]
  }'
```

Response:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "context": {
      "apiVersion": "1.17.0",
      "slot": 250000000
    },
    "value": 1000000
  },
  "id": 1
}
```

Get SPL token account balance:
```bash
curl https://api.mainnet-beta.solana.com -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTokenAccountsByOwner",
    "params": [
      "4fYNw3dojWmq4dLFEday1r6z58VVzS1qaodJs1sPL2Z",
      {
        "programId": "TokenkegQfeZyiNwAJsyFbPVwwQQfhardt5gNsQsKpr"
      },
      {
        "encoding": "jsonParsed"
      }
    ]
  }'
```

Response:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "context": {
      "apiVersion": "1.17.0",
      "slot": 250000000
    },
    "value": [
      {
        "account": {
          "data": {
            "parsed": {
              "info": {
                "tokenAmount": {
                  "amount": "1000000000",
                  "decimals": 6,
                  "uiAmount": 1000
                }
              }
            }
          }
        }
      }
    ]
  },
  "id": 1
}
```

**Configuration**:
```python
# backend/app/services/blockchain/solana_adapter.py
class SolanaAdapter(BaseBlockchainAdapter):
    PRIMARY_RPC = "https://api.mainnet-beta.solana.com"
    FALLBACK_RPCS = [
        "https://rpc.ankr.com/solana",
        "https://solana-api.projectserum.com"
    ]

    async def verify_balance(self, address: str, token_mint: Optional[str] = None) -> Balance:
        """Verify SOL or SPL token balance."""
        if token_mint:
            balance = await self.get_token_balance(address, token_mint)
        else:
            balance = await self.get_sol_balance(address)

        slot = await self.get_current_slot()
        return Balance(
            address=address,
            balance=balance,
            blockchain="Solana",
            verified_at=datetime.utcnow(),
            block_height=slot,
            method="RPC"
        )

    async def get_token_balance(self, owner: str, mint: str) -> Decimal:
        """Get SPL token balance."""
        result = await self.rpc_call(
            "getTokenAccountsByOwner",
            [owner, {"mint": mint}, {"encoding": "jsonParsed"}]
        )

        if result["value"]:
            amount = result["value"][0]["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"]
            return Decimal(amount)
        return Decimal(0)
```

---

### 4. XRP Ledger (XRP)

**Supported Networks**: XRP Ledger Mainnet

**Primary Provider**: XRP Ledger API (rippled)

- **Endpoint**: `https://xrpl.ws` (WebSocket)
- **HTTP Fallback**: `https://s1.ripple.com:51234`
- **Authentication**: None (public API)
- **Rate Limit**: 10 requests/second
- **SLA**: 99.0% uptime
- **Health Check**: `account_info` RPC call

**Request Examples**:

Get account balance:
```bash
curl -X POST https://s1.ripple.com:51234 \
  -H "Content-Type: application/json" \
  -d '{
    "method": "account_info",
    "params": [
      {
        "account": "rN7n7otQDd6FczFgLdlqtyMVrKDJzgaP",
        "ledger_index": "validated"
      }
    ]
  }'
```

Response:
```json
{
  "result": {
    "account_data": {
      "Account": "rN7n7otQDd6FczFgLdlqtyMVrKDJzgaP",
      "Balance": "1000000000",
      "Flags": 0,
      "LedgerEntryType": "AccountRoot",
      "OwnerNode": "0000000000000000",
      "PreviousTxnID": "abc123...",
      "PreviousTxnLgrSeq": 850000,
      "Sequence": 1
    },
    "ledger_hash": "...",
    "ledger_index": 850000,
    "validated": true
  }
}
```

Get token (trust line) balance:
```bash
curl -X POST https://s1.ripple.com:51234 \
  -H "Content-Type: application/json" \
  -d '{
    "method": "account_lines",
    "params": [
      {
        "account": "rN7n7otQDd6FczFgLdlqtyMVrKDJzgaP",
        "ledger_index": "validated"
      }
    ]
  }'
```

Response:
```json
{
  "result": {
    "account": "rN7n7otQDd6FczFgLdlqtyMVrKDJzgaP",
    "lines": [
      {
        "account": "rHub54yEBCd87jkY1K6kJzC4ZLtzKK6KzX",
        "balance": "1000000",
        "currency": "USD",
        "limit": "5000000",
        "limit_peer": "1000000"
      }
    ]
  }
}
```

**Configuration**:
```python
# backend/app/services/blockchain/xrp_adapter.py
class XRPAdapter(BaseBlockchainAdapter):
    PRIMARY_RPC = "https://s1.ripple.com:51234"
    FALLBACK_RPC = "https://s2.ripple.com:51234"

    async def verify_balance(self, address: str, currency: Optional[str] = None) -> Balance:
        """Verify XRP or trust line balance."""
        if currency:
            # Trust line (issued currency)
            balance = await self.get_trust_line_balance(address, currency)
        else:
            # Native XRP
            balance = await self.get_xrp_balance(address)

        ledger_info = await self.get_ledger_info()
        return Balance(
            address=address,
            balance=balance,
            blockchain="XRP",
            verified_at=datetime.utcnow(),
            block_height=ledger_info["ledger_index"],
            method="RIPPLED_RPC"
        )
```

---

### 5. BNB Chain (BSC)

**Supported Networks**: BNB Chain Mainnet

**Primary Providers**:

#### Ankr RPC
- **Endpoint**: `https://rpc.ankr.com/bsc`
- **Authentication**: None (public RPC)
- **Rate Limit**: 100 requests/second
- **SLA**: 99.5% uptime

#### BSCScan API
- **Endpoint**: `https://api.bscscan.com/api`
- **Authentication**: API Key
- **Rate Limit**: 5 calls/second
- **SLA**: 99.5% uptime

**Configuration**:
```python
# Similar to Ethereum adapter but for BNB Chain
class BNBAdapter(BaseBlockchainAdapter):
    PRIMARY_RPC = "https://rpc.ankr.com/bsc"
    ETHERSCAN_COMPATIBLE = True  # Uses same ABI as Ethereum

    async def verify_balance(self, address: str, token_address: Optional[str] = None) -> Balance:
        """Verify BNB or BEP-20 token balance."""
        # Uses same logic as Ethereum adapter
        if token_address:
            balance = await self.get_token_balance(address, token_address)
        else:
            balance = await self.get_native_balance(address)

        block_height = await self.get_block_number()
        return Balance(
            address=address,
            balance=balance,
            blockchain="BNB Chain",
            verified_at=datetime.utcnow(),
            block_height=block_height,
            method="RPC"
        )
```

---

### 6. Layer 2 Solutions (Polygon, Arbitrum, Optimism, Base)

**Common Pattern**: All L2s are EVM-compatible, use same JSON-RPC interface as Ethereum

#### Polygon (Matic)
- **RPC Endpoint**: `https://polygon-rpc.com`
- **Backup**: `https://rpc.ankr.com/polygon`
- **PolygonScan API**: `https://api.polygonscan.com/api`

#### Arbitrum One
- **RPC Endpoint**: `https://arb1.arbitrum.io/rpc`
- **Backup**: `https://rpc.ankr.com/arbitrum`
- **Arbiscan API**: `https://api.arbiscan.io/api`

#### Optimism Mainnet
- **RPC Endpoint**: `https://mainnet.optimism.io`
- **Backup**: `https://rpc.ankr.com/optimism`
- **Optimistic Etherscan**: `https://api-optimistic.etherscan.io/api`

#### Base
- **RPC Endpoint**: `https://base.publicrpc.com`
- **Backup**: `https://rpc.ankr.com/base`
- **BaseScan**: `https://api.basescan.org/api`

**Configuration**:
```python
# backend/app/services/blockchain/multi_chain_adapter.py
class MultiChainAdapter:
    CHAIN_CONFIGS = {
        "polygon": {
            "rpc": "https://polygon-rpc.com",
            "fallback": ["https://rpc.ankr.com/polygon"],
            "explorer": "https://api.polygonscan.com/api"
        },
        "arbitrum": {
            "rpc": "https://arb1.arbitrum.io/rpc",
            "fallback": ["https://rpc.ankr.com/arbitrum"],
            "explorer": "https://api.arbiscan.io/api"
        },
        "optimism": {
            "rpc": "https://mainnet.optimism.io",
            "fallback": ["https://rpc.ankr.com/optimism"],
            "explorer": "https://api-optimistic.etherscan.io/api"
        },
        "base": {
            "rpc": "https://base.publicrpc.com",
            "fallback": ["https://rpc.ankr.com/base"],
            "explorer": "https://api.basescan.org/api"
        }
    }

    async def verify_balance(self, chain: str, address: str, token: Optional[str] = None):
        """Unified interface for all EVM chains."""
        config = self.CHAIN_CONFIGS[chain]
        adapter = EVMAdapter(config)
        return await adapter.verify_balance(address, token)
```

---

## DeFi Protocol Integrations

### 1. Aave V3

**Purpose**: Verify lent assets and collateral positions

**Contract Addresses**:
- **Pool**: `0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9` (Ethereum)
- **DataProvider**: `0x7B4E16D9D94B4e4bA87A09466dcDnd1FE64e3477` (Ethereum)

**Integration Method**: Direct contract calls via eth_call

**Request Example**:

Get user account data (collateral, debt, health):
```json
{
  "method": "eth_call",
  "params": [
    {
      "to": "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9",
      "data": "0xbf92857c000000000000000000000000{user_address_padded}"
    },
    "latest"
  ]
}
```

**ABI Snippet**:
```json
[
  {
    "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
    "name": "getUserAccountData",
    "outputs": [
      {"internalType": "uint256", "name": "totalCollateralBase", "type": "uint256"},
      {"internalType": "uint256", "name": "totalDebtBase", "type": "uint256"},
      {"internalType": "uint256", "name": "availableBorrowsBase", "type": "uint256"},
      {"internalType": "uint256", "name": "currentLiquidationThreshold", "type": "uint256"},
      {"internalType": "uint256", "name": "ltv", "type": "uint256"},
      {"internalType": "uint256", "name": "healthFactor", "type": "uint256"}
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
```

**Configuration**:
```python
# backend/app/services/blockchain/defi_verifier.py
class AaveVerifier:
    POOL_ADDRESS = "0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9"
    POOL_ABI = [...]  # Full ABI

    async def verify_aave_position(self, user_address: str) -> Dict:
        """Verify Aave V3 position."""
        pool_contract = self.web3.eth.contract(
            address=self.POOL_ADDRESS,
            abi=self.POOL_ABI
        )

        account_data = pool_contract.functions.getUserAccountData(user_address).call()

        return {
            "collateral_usd": Decimal(account_data[0]) / Decimal(1e8),
            "debt_usd": Decimal(account_data[1]) / Decimal(1e8),
            "available_borrows_usd": Decimal(account_data[2]) / Decimal(1e8),
            "liquidation_threshold": Decimal(account_data[3]) / Decimal(1e4),
            "ltv": Decimal(account_data[4]) / Decimal(1e4),
            "health_factor": Decimal(account_data[5]) / Decimal(1e18),
            "verified_at": datetime.utcnow()
        }
```

---

### 2. Compound V3

**Purpose**: Verify lending positions and collateral

**Contract**: `0xc3d66e191d4ac3e44a5e5e9f42d80f87a47f8561` (cUSDCv3 on Ethereum)

**Integration**: Similar to Aave - eth_call to protocol

**Key Functions**:
- `balanceOf(address)` - Get cToken balance
- `borrowBalanceCurrent(address)` - Get borrow balance
- `getAccountLiquidity(address)` - Get account health

---

### 3. Uniswap V3

**Purpose**: Verify LP (liquidity provider) positions

**Contract Addresses**:
- **PositionManager**: `0xc36442b4a4522e871399cd717abdd847ab11218e`
- **Router**: `0xe592427a0aece92de3edee1f18e0157c05861564`

**Integration**: Query position NFT and state

**Request Example**:

Get position details:
```json
{
  "method": "eth_call",
  "params": [
    {
      "to": "0xc36442b4a4522e871399cd717abdd847ab11218e",
      "data": "0x99fbab88{position_id_padded}"
    },
    "latest"
  ]
}
```

**ABI**:
```json
[
  {
    "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
    "name": "positions",
    "outputs": [
      {"internalType": "uint96", "name": "nonce", "type": "uint96"},
      {"internalType": "address", "name": "operator", "type": "address"},
      {"internalType": "address", "name": "token0", "type": "address"},
      {"internalType": "address", "name": "token1", "type": "address"},
      {"internalType": "uint24", "name": "fee", "type": "uint24"},
      {"internalType": "int24", "name": "tickLower", "type": "int24"},
      {"internalType": "int24", "name": "tickUpper", "type": "int24"},
      {"internalType": "uint128", "name": "liquidity", "type": "uint128"},
      {"internalType": "uint256", "name": "feeGrowthInside0LastX128", "type": "uint256"},
      {"internalType": "uint256", "name": "feeGrowthInside1LastX128", "type": "uint256"},
      {"internalType": "uint128", "name": "tokensOwed0", "type": "uint128"},
      {"internalType": "uint128", "name": "tokensOwed1", "type": "uint128"}
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
```

---

### 4. Lido (Liquid Staking)

**Purpose**: Verify stETH/wstETH holdings

**Contract Addresses**:
- **stETH**: `0xae7ab96520de3a18e5e111b5eaab095312d7fe84`
- **wstETH**: `0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0`

**Key Functions**:
- `balanceOf(address)` - Get stETH balance
- `getStakingApy()` - Get current APY
- `stETH to ETH` conversion

**Integration**:
```python
# Query stETH balance
stETH_balance = web3.eth.call({
    "to": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
    "data": encode_function_signature("balanceOf(address)") +
            encode_address(user_address)
})

# Convert to ETH equivalent
# stETH is 1:1 with ETH, but can query exchange rate if needed
```

---

### 5. Rocket Pool (rETH)

**Purpose**: Verify Rocket Pool stake positions

**Contract**: `0xae78736cd615f374d3278519c3f3fab6e1da1601` (rETH on Ethereum)

**Integration**: Query rETH balance and exchange rate

**Key Functions**:
- `balanceOf(address)` - rETH balance
- `getExchangeRate()` - rETH to ETH exchange rate

---

## Third-Party Custodian Integrations

### 1. Fireblocks

**Purpose**: Query custody provider balances and approve test transactions

**Endpoint**: `https://api.fireblocks.io/v1`

**Authentication**:
- API Key (header: `X-API-Key`)
- JWT (generated from private key)

**Rate Limit**: 100 requests/minute

**Configuration**:
```python
# backend/app/core/config.py
FIREBLOCKS_CONFIG = {
    "api_key": "YOUR_FIREBLOCKS_API_KEY",
    "secret_key": "YOUR_FIREBLOCKS_SECRET",
    "vault_account_id": "VAULT_ACCOUNT_ID",
    "workspace_id": "WORKSPACE_ID"
}

# backend/app/services/custodian/fireblocks_adapter.py
class FireblocksAdapter:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.fireblocks.io/v1"

    def generate_jwt(self) -> str:
        """Generate JWT token for authentication."""
        import jwt
        payload = {
            "iss": self.api_key,
            "sub": self.api_key,
            "iat": int(time.time()),
            "exp": int(time.time()) + 60
        }
        return jwt.encode(payload, self.secret_key, algorithm="RS256")

    async def get_balance(self, asset_id: str) -> Balance:
        """Get custody balance from Fireblocks."""
        headers = {
            "X-API-Key": self.api_key,
            "Authorization": f"Bearer {self.generate_jwt()}"
        }

        response = await httpx.get(
            f"{self.base_url}/vault/accounts",
            headers=headers
        )

        # Parse response and extract balance
        return Balance(...)

    async def create_test_transaction(
        self,
        source_account: str,
        destination: str,
        amount: str,
        asset: str
    ) -> TransactionRequest:
        """Create a test transaction for proof of control."""
        payload = {
            "operation": "TRANSFER",
            "accountId": source_account,
            "externalAccountId": "TEST_ACCOUNT",
            "assetId": asset,
            "amount": amount,
            "destination": {
                "type": "ONE_TIME_ADDRESS",
                "address": destination
            }
        }

        headers = {
            "X-API-Key": self.api_key,
            "Authorization": f"Bearer {self.generate_jwt()}"
        }

        response = await httpx.post(
            f"{self.base_url}/transactions",
            json=payload,
            headers=headers
        )

        return TransactionRequest.parse_obj(response.json())
```

**API Endpoints**:

Get vault accounts:
```
GET /v1/vault/accounts
Response: List of accounts with balances per asset
```

Create transaction:
```
POST /v1/transactions
Body: {
  "operation": "TRANSFER",
  "accountId": "0",
  "assetId": "BTC",
  "amount": "0.001",
  "destination": {
    "type": "ONE_TIME_ADDRESS",
    "address": "1A1z7agoat..."
  }
}
Response: {
  "id": "transaction_id",
  "status": "SUBMITTED"
}
```

---

### 2. BitGo

**Purpose**: Query BitGo-custodied wallets and confirm balances

**Endpoint**: `https://www.bitgo.com/api/v2`

**Authentication**: Access Token (Bearer token)

**Configuration**:
```python
# backend/app/services/custodian/bitgo_adapter.py
class BitGoAdapter:
    API_URL = "https://www.bitgo.com/api/v2"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    async def get_wallet_balance(self, wallet_id: str, coin: str) -> Balance:
        """Get BitGo wallet balance."""
        response = await httpx.get(
            f"{self.API_URL}/{coin}/wallet/{wallet_id}",
            headers=self.headers
        )

        wallet_data = response.json()
        balance = Decimal(wallet_data["balance"]) / Decimal(1e8)

        return Balance(
            address=wallet_id,
            balance=balance,
            blockchain=coin,
            custody_provider="BitGo",
            verified_at=datetime.utcnow()
        )

    async def send_test_transaction(
        self,
        wallet_id: str,
        coin: str,
        destination: str,
        amount: str
    ) -> str:
        """Send test transaction for proof of control."""
        payload = {
            "address": destination,
            "amount": int(Decimal(amount) * Decimal(1e8)),
            "numBlocks": 10,
            "feeRate": 50,
            "walletPassphrase": "PASSPHRASE"  # Should be from secure storage
        }

        response = await httpx.post(
            f"{self.API_URL}/{coin}/wallet/{wallet_id}/sendcoins",
            json=payload,
            headers=self.headers
        )

        return response.json()["id"]  # Transaction ID
```

**API Endpoints**:

Get wallet:
```
GET /api/v2/{coin}/wallet/{walletId}
Response: {
  "id": "wallet_id",
  "balance": 1000000000,
  "confirmedBalance": 1000000000,
  "spendableBalance": 1000000000
}
```

Send transaction:
```
POST /api/v2/{coin}/wallet/{walletId}/sendcoins
Body: {
  "address": "destination_address",
  "amount": 100000,
  "numBlocks": 10
}
Response: {
  "id": "tx_id",
  "txid": "blockchain_tx_hash"
}
```

---

### 3. Copper

**Purpose**: Interface with Copper custody for balance verification

**Endpoint**: `https://api.copper.co/v1`

**Authentication**: API Key + Client ID (headers)

**Configuration**:
```python
class CopperAdapter:
    API_URL = "https://api.copper.co/v1"

    def __init__(self, api_key: str, client_id: str):
        self.api_key = api_key
        self.client_id = client_id
        self.headers = {
            "X-API-Key": api_key,
            "X-Client-Id": client_id,
            "Content-Type": "application/json"
        }

    async def get_account_balance(self, account_id: str) -> Dict:
        """Get Copper account balance."""
        response = await httpx.get(
            f"{self.API_URL}/accounts/{account_id}/balances",
            headers=self.headers
        )
        return response.json()
```

---

### 4. Generic Custodian Adapter

**Purpose**: Provide abstraction for any third-party custodian

```python
# backend/app/services/custodian/base_custodian.py
from abc import ABC, abstractmethod

class BaseCustodianAdapter(ABC):
    """Base class for custodian integrations."""

    @abstractmethod
    async def get_balance(self, account_id: str, asset: str) -> Balance:
        """Get balance from custodian."""
        pass

    @abstractmethod
    async def verify_control(self, account_id: str, transaction_id: str) -> bool:
        """Verify proof of control transaction."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if custodian API is healthy."""
        pass

    @abstractmethod
    async def list_accounts(self) -> List[str]:
        """List all accounts under custody."""
        pass

# Factory for custodian selection
class CustodianFactory:
    ADAPTERS = {
        "fireblocks": FireblocksAdapter,
        "bitgo": BitGoAdapter,
        "copper": CopperAdapter,
        "coinbase_prime": CoinbasePrimeAdapter,
    }

    @staticmethod
    def create(custodian_type: str, **kwargs) -> BaseCustodianAdapter:
        adapter_class = CustodianFactory.ADAPTERS.get(custodian_type)
        if not adapter_class:
            raise ValueError(f"Unknown custodian: {custodian_type}")
        return adapter_class(**kwargs)
```

---

## Notification Integrations

### 1. Email (SMTP/SendGrid)

**Provider Options**:

#### SendGrid API
- **Endpoint**: `https://api.sendgrid.com/v3`
- **Authentication**: API Key (Bearer token)
- **Rate Limit**: 100 requests/second

**Configuration**:
```python
# backend/app/core/config.py
SENDGRID_CONFIG = {
    "api_key": "YOUR_SENDGRID_API_KEY",
    "from_email": "noreply@simplyfi.com",
    "templates": {
        "engagement_created": "d-12345...",
        "report_ready": "d-23456...",
        "alert_under_reserved": "d-34567...",
        "liability_data_requested": "d-45678..."
    }
}

# backend/app/services/notifications/email.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailService:
    def __init__(self, api_key: str):
        self.sg = SendGridAPIClient(api_key)

    async def send_engagement_created(self, vasp_email: str, engagement_name: str):
        """Send email when engagement is created."""
        message = Mail(
            from_email="noreply@simplyfi.com",
            to_emails=vasp_email,
            subject=f"Audit Engagement Created: {engagement_name}",
            html_content=f"""
            <p>Your audit engagement has been created.</p>
            <p>Engagement: {engagement_name}</p>
            <p><a href="https://app.simplyfi.com/engagements">View Details</a></p>
            """
        )

        response = self.sg.send(message)
        return response.status_code == 202

    async def send_using_template(
        self,
        to_email: str,
        template_id: str,
        dynamic_data: Dict
    ):
        """Send email using SendGrid template."""
        message = Mail(
            from_email="noreply@simplyfi.com",
            to_emails=to_email
        )
        message.template_id = template_id
        message.dynamic_template_data = dynamic_data

        response = self.sg.send(message)
        return response.status_code == 202
```

**Email Templates**:

```
Template ID: d-12345...
Name: engagement_created
Subject: Audit Engagement Created: {{engagement_name}}
Variables:
  - engagement_name
  - vasp_name
  - auditor_name
  - engagement_url
  - data_deadline
```

### 2. SMS (Twilio)

**Endpoint**: `https://api.twilio.com/2010-04-01`

**Authentication**: Account SID + Auth Token

**Configuration**:
```python
from twilio.rest import Client

class SMSService:
    def __init__(self, account_sid: str, auth_token: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = "+1XXXXXXXXXX"

    async def send_alert_sms(self, phone_number: str, message: str):
        """Send SMS alert to compliance officer."""
        message = self.client.messages.create(
            body=message,
            from_=self.from_number,
            to=phone_number
        )
        return message.sid

# Example usage
sms = SMSService(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
await sms.send_alert_sms(
    "+1XXXXXXXXXX",
    "ALERT: BTC reserve ratio dropped to 93%. Review immediately."
)
```

### 3. Slack/Teams Webhooks

**Purpose**: Real-time alerts for compliance and operational teams

**Slack Webhook**:
```python
import httpx

class SlackNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send_alert(self, alert_type: str, message: str, severity: str):
        """Send alert to Slack."""
        color_map = {
            "CRITICAL": "ff0000",
            "HIGH": "ff9900",
            "MEDIUM": "ffcc00",
            "LOW": "0099ff"
        }

        payload = {
            "attachments": [
                {
                    "color": color_map.get(severity, "808080"),
                    "title": f"{alert_type} - {severity}",
                    "text": message,
                    "ts": int(time.time())
                }
            ]
        }

        response = await httpx.post(self.webhook_url, json=payload)
        return response.status_code == 200
```

### 4. In-App Notifications (WebSocket)

**Purpose**: Real-time notifications in web dashboard

```python
# backend/app/api/v1/endpoints/websocket.py
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        del self.active_connections[user_id]

    async def broadcast(self, message: Dict):
        """Broadcast to all connected users with appropriate permissions."""
        for user_id, websocket in self.active_connections.items():
            # Check if user should receive this notification
            if self.should_notify_user(user_id, message):
                await websocket.send_json(message)

    async def send_personal(self, user_id: str, message: Dict):
        """Send notification to specific user."""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)

# Notification event emission
async def emit_alert(alert_id: str, alert_type: str, severity: str):
    """Emit alert via WebSocket."""
    message = {
        "type": "alert",
        "alert_id": alert_id,
        "alert_type": alert_type,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat()
    }
    await manager.broadcast(message)
```

---

## KYC & Identity Integrations

### Jumio

**Purpose**: Verify VASP user identity (optional for certain roles)

**Endpoint**: `https://api.jumio.com/api/v1`

**Flow**:
```
User clicks "Verify Identity"
  ↓
Redirects to Jumio portal
  ↓
Captures ID and selfie
  ↓
Jumio processes and returns status
  ↓
Webhook callback confirms verification
  ↓
User record updated with verification status
```

### Onfido

**Alternative**: `https://api.onfido.com/v3.6`

**Integration**: Similar to Jumio, webhook-based verification

---

## Monitoring & Observability Integrations

### 1. OpenTelemetry

**Purpose**: Distributed tracing and metrics collection

**Configuration**:
```python
# backend/app/core/observability.py
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="localhost:4317"  # Default gRPC endpoint
)

trace_provider = TracerProvider()
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(trace_provider)

# Instrument key operations
tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("verify_balance")
async def verify_balance(address: str, blockchain: str):
    """Span: verify_balance"""
    span = trace.get_current_span()
    span.set_attribute("address", address)
    span.set_attribute("blockchain", blockchain)

    # ... verification logic

    span.set_attribute("status", "verified")
```

### 2. Prometheus Metrics

**Endpoint**: `http://localhost:9090`

**Configuration**:
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Metrics definition
verification_counter = Counter(
    "verifications_total",
    "Total verification attempts",
    ["blockchain", "status"]
)

verification_duration = Histogram(
    "verification_duration_seconds",
    "Verification duration",
    ["blockchain"],
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0)
)

reserve_ratio_gauge = Gauge(
    "reserve_ratio",
    "Current reserve ratio per asset",
    ["engagement_id", "asset"]
)

api_request_counter = Counter(
    "api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"]
)

# Recording metrics
verification_counter.labels(blockchain="BTC", status="success").inc()
reserve_ratio_gauge.labels(
    engagement_id="eng-123",
    asset="BTC"
).set(1.05)

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest())
```

### 3. Grafana Dashboards

**Data Source**: Prometheus

**Sample Dashboards**:
```
Dashboard: "Platform Health"
  - Verification success rate (%)
  - Average verification latency (ms)
  - Reserve ratio by engagement
  - Alert volume (CRITICAL, HIGH, MEDIUM, LOW)
  - Blockchain API health (% uptime)
  - Celery task queue depth
  - Database connection pool usage

Dashboard: "Engagement Progress"
  - Engagements by status (PLANNING, DATA_COLLECTION, VERIFICATION, etc.)
  - Verification completion % per engagement
  - Average time per engagement phase
  - Report generation time trend

Dashboard: "Compliance Monitor"
  - Under-reserved engagements (count)
  - Reserve ratio distribution
  - VARA compliance status
  - Alert trends (7-day, 30-day)
```

### 4. PagerDuty/OpsGenie

**Purpose**: On-call escalation for critical alerts

**Configuration**:
```python
# backend/app/services/alerting/pagerduty_integration.py
import httpx

class PagerDutyIntegration:
    API_URL = "https://api.pagerduty.com"

    def __init__(self, token: str, escalation_policy_id: str):
        self.token = token
        self.escalation_policy_id = escalation_policy_id
        self.headers = {
            "Authorization": f"Token token={token}",
            "Content-Type": "application/json"
        }

    async def create_incident(
        self,
        title: str,
        details: str,
        severity: str = "critical"
    ) -> str:
        """Create incident in PagerDuty."""
        payload = {
            "incident": {
                "type": "incident",
                "title": title,
                "service": {
                    "id": self.service_id,
                    "type": "service_reference"
                },
                "body": {
                    "type": "incident_body",
                    "details": details
                },
                "urgency": "high" if severity == "critical" else "medium",
                "escalation_policy": {
                    "id": self.escalation_policy_id,
                    "type": "escalation_policy_reference"
                }
            }
        }

        response = await httpx.post(
            f"{self.API_URL}/incidents",
            json=payload,
            headers=self.headers
        )

        return response.json()["incident"]["id"]

# Trigger on critical alerts
@app.post("/api/v1/alerts/critical")
async def handle_critical_alert(alert: Alert):
    if alert.severity == "CRITICAL":
        incident_id = await pagerduty.create_incident(
            title=f"CRITICAL: {alert.message}",
            details=f"Engagement: {alert.engagement_id}, Asset: {alert.asset_id}"
        )
        logger.critical(f"PagerDuty incident created: {incident_id}")
```

---

## Storage Integrations

### 1. S3 (MinIO or AWS)

**Purpose**: Store audit reports, backups, customer data

**Configuration**:
```python
# backend/app/core/storage.py
import boto3
from botocore.config import Config

class S3Storage:
    def __init__(self, endpoint_url: str = None, use_ssl: bool = True):
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url or "https://s3.amazonaws.com",
            config=Config(
                signature_version="s3v4",
                retries={"max_attempts": 3, "mode": "adaptive"}
            )
        )

    async def upload_report(self, engagement_id: str, report_pdf: bytes):
        """Upload audit report to S3."""
        key = f"audit-reports/{engagement_id}/report-{datetime.utcnow().date()}.pdf"

        self.client.put_object(
            Bucket="simplyfi-por-reports",
            Key=key,
            Body=report_pdf,
            ContentType="application/pdf",
            ServerSideEncryption="AES256",
            Metadata={"engagement_id": engagement_id}
        )

        # Generate presigned URL valid for 7 days
        url = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": "simplyfi-por-reports", "Key": key},
            ExpiresIn=604800  # 7 days
        )

        return url

    async def backup_database(self, backup_data: bytes, date: str):
        """Upload database backup."""
        key = f"backups/database/{date}.sql.gz"

        self.client.put_object(
            Bucket="simplyfi-por-backups",
            Key=key,
            Body=backup_data,
            ServerSideEncryption="AES256",
            StorageClass="STANDARD_IA"  # Infrequent access
        )

# S3 Bucket Structure
"""
simplyfi-por-reports/
  ├── audit-reports/
  │   ├── eng-001/
  │   │   ├── report-2024-01-15.pdf
  │   │   ├── report-2024-04-15.pdf
  │   └── eng-002/
  │       └── report-2024-02-01.pdf
  │
  simplyfi-por-backups/
  ├── database/
  │   ├── 2024-01-15.sql.gz
  │   ├── 2024-01-16.sql.gz
  │   └── ...
  │
  simplyfi-por-merkle-proofs/
  ├── eng-001/
  │   └── merkle-proofs-2024-01-15.json
"""
```

**Bucket Policies**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EncryptionRequired",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::simplyfi-por-*/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "AES256"
        }
      }
    },
    {
      "Sid": "BackupRetention",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT_ID:role/SimplyFiBackupRole"
      },
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::simplyfi-por-backups/*"
    }
  ]
}
```

### 2. PostgreSQL

**Purpose**: Store all application data (users, engagements, verification results)

**Configuration**:
```python
# backend/app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool

class DatabaseConfig:
    DATABASE_URL = "postgresql+asyncpg://user:password@host:5432/por_db"

    # Connection pooling
    POOL_SIZE = 20
    MAX_OVERFLOW = 10
    POOL_RECYCLE = 3600  # Recycle connections every hour
    POOL_PRE_PING = True  # Verify connection health before use

    # Timeouts
    CONNECT_TIMEOUT = 30
    STATEMENT_TIMEOUT = 60000  # 60 seconds

    # Replication (for high availability)
    READ_REPLICAS = [
        "postgresql+asyncpg://user:password@replica-1:5432/por_db",
        "postgresql+asyncpg://user:password@replica-2:5432/por_db"
    ]

# Initialize engine
engine = create_async_engine(
    DatabaseConfig.DATABASE_URL,
    echo=False,
    pool_size=DatabaseConfig.POOL_SIZE,
    max_overflow=DatabaseConfig.MAX_OVERFLOW,
    pool_recycle=DatabaseConfig.POOL_RECYCLE,
    pool_pre_ping=True,
    connect_args={"timeout": DatabaseConfig.CONNECT_TIMEOUT}
)
```

**Indexes**:
```sql
-- Key indexes for performance
CREATE INDEX ix_users_tenant_id_active ON users(tenant_id, is_active);
CREATE INDEX ix_engagements_status_reporting_date ON engagements(status, reporting_date);
CREATE INDEX ix_asset_balances_engagement_asset ON asset_balances(engagement_id, asset_id);
CREATE INDEX ix_reconciliation_records_engagement_date ON reconciliation_records(engagement_id, date);
CREATE INDEX ix_audit_logs_user_resource_action ON audit_logs(user_id, resource, action);
```

### 3. Redis

**Purpose**: Caching, Celery broker, pub/sub, session storage

**Configuration**:
```python
# backend/app/core/cache.py
import aioredis
from redis import Redis

class RedisConfig:
    REDIS_URL = "redis://localhost:6379"

    # Databases
    CACHE_DB = 0          # General cache
    CELERY_BROKER_DB = 1  # Celery task broker
    CELERY_RESULT_DB = 2  # Celery result backend
    SESSION_DB = 3        # Session storage

    # TTLs
    CACHE_TTL = 3600     # 1 hour
    SESSION_TTL = 86400  # 1 day
    TASK_TTL = 86400     # 1 day

    # Connection pooling
    CONNECTION_POOL_SIZE = 50

async def get_redis_cache():
    redis = await aioredis.create_redis_pool(
        RedisConfig.REDIS_URL,
        encoding="utf-8",
        maxsize=RedisConfig.CONNECTION_POOL_SIZE
    )
    return redis

# Caching decorator
def cached(ttl: int = 3600):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            redis = await get_redis_cache()

            # Try to get from cache
            cached_result = await redis.get(cache_key)
            if cached_result:
                return json.loads(cached_result)

            # Compute and cache result
            result = await func(*args, **kwargs)
            await redis.setex(cache_key, ttl, json.dumps(result))

            return result
        return wrapper
    return decorator

# Example: Cache blockchain balance verification results
@cached(ttl=300)  # 5 minutes
async def verify_balance(address: str, blockchain: str) -> Balance:
    # ... verification logic
    pass
```

**Redis Data Structures**:
```python
# Celery task queue
redis.push("celery:verification", task_data)  # Queue
redis.pop("celery:verification")              # Worker dequeue

# Pub/Sub for real-time alerts
redis.publish("alerts:critical", alert_message)
redis.subscribe("alerts:critical")

# Cache
redis.setex("balance:0x123:eth", 300, "5000")
redis.get("balance:0x123:eth")

# Session storage
redis.setex(f"session:{session_id}", 86400, session_data)
```

---

## Integration Health Checks

**Monitoring Script**:
```python
# backend/app/tasks/health_check_task.py

async def check_blockchain_health():
    """Check all blockchain provider health."""
    providers = {
        "bitcoin": BlockstreamAPI,
        "ethereum": InfuraAPI,
        "solana": SolanaRPC,
        "xrp": XRPLedgerAPI
    }

    results = {}
    for name, provider in providers.items():
        try:
            response = await provider.health_check()
            results[name] = {
                "status": "healthy" if response.ok else "degraded",
                "latency_ms": response.elapsed.total_seconds() * 1000,
                "timestamp": datetime.utcnow()
            }
        except Exception as e:
            results[name] = {
                "status": "down",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }

    return results

# Health check endpoints
@app.get("/health/dependencies")
async def health_check():
    """Return health status of all integrations."""
    return {
        "blockchain": await check_blockchain_health(),
        "database": await check_database_health(),
        "redis": await check_redis_health(),
        "s3": await check_s3_health(),
        "email": await check_email_health(),
        "timestamp": datetime.utcnow()
    }
```

---

## Integration Testing

**Test Fixtures**:
```python
# backend/tests/conftest.py

@pytest.fixture
def mock_blockstream():
    """Mock Blockstream API responses."""
    with patch("app.services.blockchain.bitcoin_adapter.blockstream_api") as mock:
        mock.get_address.return_value = {
            "chain_stats": {
                "funded_txo_sum": 500000000,
                "spent_txo_sum": 250000000
            }
        }
        yield mock

@pytest.fixture
def mock_infura():
    """Mock Infura JSON-RPC responses."""
    with patch("app.services.blockchain.ethereum_adapter.web3") as mock:
        mock.eth.get_balance.return_value = 5000000000000000000  # 5 ETH
        yield mock

# Integration tests
@pytest.mark.asyncio
async def test_bitcoin_balance_verification(mock_blockstream):
    adapter = BitcoinAdapter()
    balance = await adapter.verify_balance("bc1qz3khxnyq05...")

    assert balance.balance == Decimal("250")  # (500M - 250M) / 1e8
    assert balance.blockchain == "Bitcoin"
```

---

## Summary

This integrations catalog provides:
- Complete list of all blockchain providers (Bitcoin, Ethereum, Solana, XRP, BNB, L2s)
- DeFi protocol integration methods (Aave, Compound, Uniswap, Lido)
- Third-party custodian adapter patterns (Fireblocks, BitGo, Copper)
- Notification channels (Email, SMS, Slack, WebSocket)
- Monitoring and observability tools (OpenTelemetry, Prometheus, Grafana, PagerDuty)
- Storage solutions (S3, PostgreSQL, Redis)
- Configuration examples and error handling patterns
- Health check procedures and testing approaches

Teams can use this document to:
- Understand how external systems are integrated
- Add new blockchain providers or custodians
- Configure API keys and endpoints
- Set up monitoring and alerts
- Test integrations in CI/CD pipeline
- Troubleshoot integration issues

