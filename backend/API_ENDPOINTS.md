# SimplyFI POR Platform - Complete API Endpoint Reference

## Base URL
```
/api/v1
```

---

## Authentication Endpoints
**Path**: `/auth`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/login` | User login with optional MFA | ❌ |
| POST | `/register` | Register new user | ❌ |
| POST | `/refresh` | Refresh access token | ❌ |
| POST | `/logout` | Logout user | ✅ |
| POST | `/mfa/setup` | Setup MFA for user | ✅ |
| POST | `/mfa/verify` | Verify MFA token | ✅ |

**Payloads**:
```json
// POST /login
{
  "email": "user@example.com",
  "password": "password123",
  "mfa_token": "123456"  // Optional
}

// POST /register
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "password123",
  "tenant_id": "tenant-uuid"
}

// POST /refresh
{
  "refresh_token": "jwt-token"
}

// POST /mfa/verify
{
  "token": "123456"
}
```

---

## User Management Endpoints
**Path**: `/users`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| GET | `/me` | Get current user profile | ✅ | User |
| PUT | `/me` | Update current user | ✅ | User |
| POST | `/me/change-password` | Change password | ✅ | User |
| GET | `` | List tenant users | ✅ | Admin |
| GET | `/{user_id}` | Get user by ID | ✅ | Admin |
| PUT | `/{user_id}` | Update user | ✅ | Admin |
| DELETE | `/{user_id}` | Delete user | ✅ | Admin |
| POST | `/{user_id}/roles` | Assign role to user | ✅ | Admin |

**Query Parameters**:
- `skip` (int, default=0)
- `limit` (int, default=100, max=1000)

**Payloads**:
```json
// PUT /me
{
  "full_name": "John Doe",
  "is_active": true
}

// POST /me/change-password
{
  "current_password": "old_password",
  "new_password": "new_password"
}

// POST /{user_id}/roles
{
  "role_id": "role-uuid",
  "engagement_id": "engagement-uuid"  // Optional
}
```

---

## Tenant Management Endpoints
**Path**: `/tenants`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| POST | `` | Create tenant | ✅ | Superadmin |
| GET | `` | List all tenants | ✅ | Admin |
| GET | `/{tenant_id}` | Get tenant details | ✅ | Admin |
| PUT | `/{tenant_id}` | Update tenant | ✅ | Admin |
| DELETE | `/{tenant_id}` | Delete tenant | ✅ | Admin |
| GET | `/{tenant_id}/members` | List tenant members | ✅ | User |
| PUT | `/{tenant_id}/settings` | Update tenant settings | ✅ | Admin |

**Payloads**:
```json
// POST /
{
  "name": "Acme Auditors",
  "type": "AUDITOR",  // AUDITOR, VASP, REGULATOR, CUSTOMER
  "vara_license_number": "VARA-123-456",
  "settings_json": {}
}

// PUT /{tenant_id}
{
  "name": "Acme Auditors",
  "settings_json": {}
}

// PUT /{tenant_id}/settings
{
  "key": "value"
}
```

---

## Engagement Management Endpoints
**Path**: `/engagements`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| POST | `` | Create engagement | ✅ | Auditor |
| GET | `` | List engagements | ✅ | User |
| GET | `/{engagement_id}` | Get engagement details | ✅ | User |
| PUT | `/{engagement_id}` | Update engagement | ✅ | Auditor |
| PUT | `/{engagement_id}/status` | Update status | ✅ | Auditor |
| DELETE | `/{engagement_id}` | Delete engagement | ✅ | Auditor |
| POST | `/{engagement_id}/assets` | Bulk add assets | ✅ | Auditor |
| GET | `/{engagement_id}/timeline` | Get timeline | ✅ | User |
| POST | `/{engagement_id}/timeline` | Add timeline phase | ✅ | Auditor |

**Status Values**: `PLANNING`, `DATA_COLLECTION`, `VERIFICATION`, `REPORTING`, `COMPLETED`

**Payloads**:
```json
// POST /
{
  "name": "Q4 2024 Audit",
  "client_tenant_id": "client-uuid",
  "auditor_tenant_id": "auditor-uuid",
  "reporting_date": "2024-12-31T23:59:59Z",
  "settings_json": {}
}

// PUT /{engagement_id}/status
{
  "status": "VERIFICATION"
}

// POST /{engagement_id}/assets
{
  "assets": [
    {
      "asset_symbol": "BTC",
      "asset_name": "Bitcoin",
      "tier": 1,
      "contract_addresses_json": {},
      "blockchains_json": ["bitcoin"]
    }
  ]
}

// POST /{engagement_id}/timeline
{
  "phase": "Data Collection",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-15T23:59:59Z"
}
```

---

## Asset Management Endpoints
**Path**: `/assets`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| POST | `` | Create crypto asset | ✅ | Admin |
| GET | `` | List crypto assets | ✅ | User |
| GET | `/{asset_id}` | Get asset details | ✅ | User |
| GET | `/{asset_id}/wallets` | List wallets holding asset | ✅ | User |
| POST | `/{asset_id}/wallets` | Add wallet address | ✅ | Auditor |
| POST | `/{asset_id}/verify-balance` | Verify balance | ✅ | Auditor |
| POST | `/bulk-import` | Bulk import assets | ✅ | Admin |

**Query Parameters**:
- `asset_type` (COIN, TOKEN, STABLECOIN, NFT)
- `is_active` (boolean)
- `skip` (int)
- `limit` (int)

**Payloads**:
```json
// POST /
{
  "symbol": "BTC",
  "name": "Bitcoin",
  "asset_type": "COIN",
  "blockchains_json": ["bitcoin"],
  "contract_addresses_json": {},
  "decimals": 8
}

// POST /{asset_id}/wallets
{
  "address": "1A1z7agoat...",
  "blockchain": "bitcoin",
  "custody_type": "THIRD_PARTY_CUSTODIAN",
  "custodian_name": "Coinbase Custody",
  "wallet_type": "COLD"
}

// POST /{asset_id}/verify-balance
{
  "wallet_address": "1A1z7agoat...",
  "blockchain": "bitcoin",
  "asset_symbol": "BTC"
}
```

---

## Reserve Endpoints
**Path**: `/engagements/{engagement_id}/reserves`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| GET | `` | Get reserve summary | ✅ | User |
| POST | `/calculate` | Calculate ratios | ✅ | Auditor |
| GET | `/ratio-table` | Get ratio table | ✅ | User |
| POST | `/verify-segregation` | Verify segregation | ✅ | Auditor |
| GET | `/reconciliation` | Get reconciliation | ✅ | User |

**Response Example**:
```json
{
  "engagement_id": "uuid",
  "total_assets_usd": 2500000,
  "total_liabilities_usd": 2437500,
  "overall_ratio_pct": 102.5,
  "meets_requirement": true,
  "by_asset": [
    {
      "id": "uuid",
      "total_assets": "1.5",
      "total_liabilities": "1.4625",
      "ratio_percentage": "102.56",
      "meets_vara_requirement": true
    }
  ],
  "last_updated": "2024-01-15T12:00:00Z"
}
```

---

## Merkle Tree Endpoints
**Path**: `/engagements/{engagement_id}/merkle`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| POST | `/generate` | Generate merkle tree | ✅ | Auditor |
| GET | `/root` | Get merkle root | ✅ | User |
| POST | `/verify` | Verify proof (PUBLIC) | ❌ | N/A |
| GET | `/stats` | Get tree statistics | ✅ | User |

**Payloads**:
```json
// POST /generate
{
  "asset_symbol": "USDC",
  "algorithm": "SHA256"  // SHA256 or KECCAK256
}

// POST /verify (PUBLIC)
{
  "root_hash": "hash...",
  "leaf_hash": "hash...",
  "proof_path": [
    {
      "hash": "hash...",
      "direction": "left"  // or "right"
    }
  ],
  "leaf_index": 0
}
```

---

## Blockchain Endpoints
**Path**: `/blockchain`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/supported-chains` | List supported chains | ❌ |
| POST | `/verify-address` | Verify address | ✅ |
| POST | `/verify-balance` | Verify balance | ✅ |
| POST | `/verify-control` | Verify control | ✅ |
| POST | `/defi/verify-position` | Verify DeFi position | ✅ |

**Supported Chains**:
- Ethereum, Polygon, Bitcoin, Litecoin, Solana, XRP Ledger
- Cardano, Algorand, Polkadot, Avalanche, Arbitrum, Optimism

**Payloads**:
```json
// POST /verify-address
{
  "address": "0x1234...",
  "blockchain": "ethereum"
}

// POST /verify-balance
{
  "address": "0x1234...",
  "blockchain": "ethereum",
  "asset_symbol": "ETH"
}

// POST /verify-control
{
  "address": "0x1234...",
  "blockchain": "ethereum",
  "amount": 0.1
}

// POST /defi/verify-position
{
  "protocol_name": "Aave",
  "contract_address": "0x7...",
  "blockchain": "ethereum",
  "position_type": "LENDING",
  "wallet_address": "0x1234..."
}
```

---

## Report Endpoints
**Path**: `/engagements/{engagement_id}/reports`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| POST | `/por` | Generate PoR report | ✅ | Auditor |
| POST | `/assurance` | Generate assurance report | ✅ | Auditor |
| POST | `/management-letter` | Generate management letter | ✅ | Auditor |
| POST | `/customer-summary` | Generate customer summary | ✅ | Auditor |
| GET | `/../reports/{report_id}/download` | Download report | ✅ | User |

**Response Example**:
```json
{
  "report_id": "uuid",
  "engagement_id": "uuid",
  "type": "PROOF_OF_RESERVES",
  "status": "GENERATING",
  "created_at": "2024-01-15T12:00:00Z",
  "file_path": "s3://bucket/por/uuid.pdf"
}
```

---

## AI Analytics Endpoints
**Path**: `/ai`

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/analyze` | Analyze for anomalies | ✅ |
| POST | `/generate-narrative` | Generate report sections | ✅ |
| POST | `/compliance-check` | Check VARA compliance | ✅ |
| POST | `/chat` | Interactive assistant | ✅ |
| GET | `/insights/{engagement_id}` | Get insights | ✅ |

**Payloads**:
```json
// POST /analyze
{
  "engagement_id": "uuid",
  "analysis_type": "balances"  // or "transactions", "patterns"
}

// POST /generate-narrative
{
  "engagement_id": "uuid",
  "section": "executive_summary"  // or "findings", "conclusion"
}

// POST /compliance-check
{
  "engagement_id": "uuid"
}

// POST /chat
{
  "engagement_id": "uuid",
  "message": "What are the total reserves?"
}
```

---

## Admin Endpoints
**Path**: `/admin`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| GET | `/dashboard` | Dashboard stats | ✅ | Superadmin |
| POST | `/roles` | Create role | ✅ | Superadmin |
| GET | `/roles` | List roles | ✅ | Superadmin |
| GET | `/roles/{role_id}` | Get role | ✅ | Superadmin |
| PUT | `/roles/{role_id}` | Update role | ✅ | Superadmin |
| PUT | `/roles/{role_id}/permissions` | Set permissions | ✅ | Superadmin |
| DELETE | `/roles/{role_id}` | Delete role | ✅ | Superadmin |
| POST | `/permissions` | Create permission | ✅ | Superadmin |
| GET | `/permissions` | List permissions | ✅ | Superadmin |
| GET | `/audit-log` | Get audit logs | ✅ | Superadmin |

**Payloads**:
```json
// POST /roles
{
  "name": "Custom Auditor",
  "description": "Custom role for auditors",
  "permissions_json": ["uuid1", "uuid2"]
}

// PUT /roles/{role_id}/permissions
["uuid1", "uuid2", "uuid3"]

// POST /permissions
{
  "resource": "engagements",
  "action": "write",
  "description": "Can write engagements",
  "field_restrictions_json": {}
}

// GET /audit-log?resource=engagement&user_id=uuid&skip=0&limit=100
```

---

## Onboarding Endpoints
**Path**: `/onboarding`

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| POST | `/vasp` | Register VASP | ✅ | Superadmin |
| POST | `/{engagement_id}/import-assets` | Import assets | ✅ | Auditor |
| POST | `/{engagement_id}/import-wallets` | Import wallets | ✅ | Auditor |
| POST | `/{engagement_id}/import-liabilities` | Import liabilities | ✅ | Auditor |
| GET | `/{engagement_id}/status` | Get status | ✅ | User |
| POST | `/{engagement_id}/validate` | Validate data | ✅ | Auditor |

**Payloads**:
```json
// POST /vasp
{
  "name": "Crypto Exchange Inc",
  "vara_license_number": "VARA-2024-001",
  "settings": {}
}

// POST /{engagement_id}/import-assets
[
  {
    "symbol": "BTC",
    "name": "Bitcoin",
    "asset_type": "COIN",
    "blockchains": ["bitcoin"],
    "contract_addresses": {},
    "decimals": 8,
    "tier": 1
  }
]

// POST /{engagement_id}/import-wallets
[
  {
    "address": "1A1z7agoat...",
    "blockchain": "bitcoin",
    "asset_symbol": "BTC",
    "custody_type": "THIRD_PARTY_CUSTODIAN",
    "custodian_name": "Coinbase",
    "wallet_type": "COLD"
  }
]

// POST /{engagement_id}/import-liabilities
[
  {
    "anonymized_user_id": "hash123",
    "asset_symbol": "BTC",
    "balance": "0.5",
    "account_type": "SPOT"
  }
]
```

---

## Health Check Endpoints
**Path**: (root)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/health` | Health check | ❌ |
| GET | `/ready` | Readiness check | ❌ |
| GET | `/` | API info | ❌ |

---

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | Service unavailable |

---

## Authentication

All endpoints marked with ✅ require Bearer token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

---

## Pagination

List endpoints support:
- `skip` (default: 0)
- `limit` (default: 100, max: 1000)

Example:
```
GET /users?skip=0&limit=50
```

---

**Total Endpoints**: 60+
**Authentication Required**: 54+
**Public Endpoints**: 6
