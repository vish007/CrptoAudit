import React, { useState } from 'react';
import { AlertCircle, CheckCircle2, Clock, Download, Filter } from 'lucide-react';
import Card from '../../components/common/Card';
import StatusBadge from '../../components/common/StatusBadge';
import Button from '../../components/common/Button';
import ReserveRatioChart from '../../components/dashboard/ReserveRatioChart';

const EngagementDetail = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [filterStatus, setFilterStatus] = useState('all');

  // Mock engagement data
  const engagement = {
    id: 'ENG-001',
    client: 'Crypto Exchange Inc.',
    status: 'in_progress',
    startDate: '2024-01-01',
    endDate: '2024-03-15',
    manager: 'Sarah Johnson',
    auditType: 'PoR AUP',
    description: 'Annual Proof of Reserves audit for cryptocurrency exchange platform',
  };

  // Timeline data
  const timeline = [
    { phase: 'Scoping', status: 'completed', date: '2024-01-01' },
    { phase: 'Planning', status: 'completed', date: '2024-01-08' },
    { phase: 'Verification', status: 'in_progress', date: '2024-01-15' },
    { phase: 'Analysis', status: 'pending', date: '2024-02-15' },
    { phase: 'Reporting', status: 'pending', date: '2024-03-15' },
  ];

  // Mock assets data - 153 assets total (showing first 20)
  const allAssets = [
    { id: 1, name: 'Bitcoin (BTC)', status: 'verified', count: 1245, progress: 100 },
    { id: 2, name: 'Ethereum (ETH)', status: 'verified', count: 8945, progress: 100 },
    { id: 3, name: 'USDC', status: 'verified', count: 12500000, progress: 100 },
    { id: 4, name: 'USDT', status: 'verified', count: 18750000, progress: 100 },
    { id: 5, name: 'Solana (SOL)', status: 'verified', count: 5420, progress: 100 },
    { id: 6, name: 'Polkadot (DOT)', status: 'verified', count: 2800, progress: 100 },
    { id: 7, name: 'Cardano (ADA)', status: 'in_progress', count: 3200, progress: 75 },
    { id: 8, name: 'Ripple (XRP)', status: 'in_progress', count: 4100, progress: 65 },
    { id: 9, name: 'Polygon (MATIC)', status: 'pending', count: 6200, progress: 20 },
    { id: 10, name: 'Cosmos (ATOM)', status: 'pending', count: 1920, progress: 10 },
    { id: 11, name: 'Litecoin (LTC)', status: 'verified', count: 3450, progress: 100 },
    { id: 12, name: 'Chainlink (LINK)', status: 'verified', count: 2800, progress: 100 },
    { id: 13, name: 'Uniswap (UNI)', status: 'in_progress', count: 2300, progress: 55 },
    { id: 14, name: 'Aave (AAVE)', status: 'in_progress', count: 1900, progress: 45 },
    { id: 15, name: 'Curve (CRV)', status: 'pending', count: 1620, progress: 5 },
    { id: 16, name: 'Lido (LDO)', status: 'in_progress', count: 2050, progress: 70 },
    { id: 17, name: 'Convex (CVX)', status: 'pending', count: 850, progress: 0 },
    { id: 18, name: 'Yearn (YFI)', status: 'verified', count: 1200, progress: 100 },
    { id: 19, name: 'MakerDAO (MKR)', status: 'pending', count: 1520, progress: 15 },
    { id: 20, name: 'Compound (COMP)', status: 'verified', count: 1280, progress: 100 },
  ];

  // Mock wallets data
  const wallets = [
    { id: 1, address: '1A1z7agoat2YLZW51Bc7M7kMccKzd6Zdbf', chain: 'Bitcoin', balance: 1245.32, verified: true, verifiedDate: '2024-01-15' },
    { id: 2, address: '0x742d35Cc6634C0532925a3b844Bc9e7595f1234A', chain: 'Ethereum', balance: 8945.67, verified: true, verifiedDate: '2024-01-15' },
    { id: 3, address: '0x88D5E22Cd1C44C9D85D2Cc5a68DD8B41B6C1234B', chain: 'Ethereum', balance: 12500000, verified: true, verifiedDate: '2024-01-15' },
    { id: 4, address: 'So11111111111111111111111111111111111111112', chain: 'Solana', balance: 5420.12, verified: false, verifiedDate: null },
    { id: 5, address: '1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX', chain: 'Bitcoin', balance: 543.21, verified: true, verifiedDate: '2024-01-14' },
  ];

  // Mock reserve data
  const reserves = [
    { asset: 'Bitcoin (BTC)', ratio: 101.24, reserves: 1245.32, liabilities: 1230.15, status: 'compliant' },
    { asset: 'Ethereum (ETH)', ratio: 101.08, reserves: 8945.67, liabilities: 8850.44, status: 'compliant' },
    { asset: 'USDC', ratio: 100.48, reserves: 12500000, liabilities: 12500000, status: 'compliant' },
    { asset: 'USDT', ratio: 100.8, reserves: 18750000, liabilities: 18600000, status: 'compliant' },
    { asset: 'Solana (SOL)', ratio: 102.24, reserves: 5420.12, liabilities: 5300.99, status: 'compliant' },
    { asset: 'Polkadot (DOT)', ratio: 99.1, reserves: 2800.45, liabilities: 2825.67, status: 'non_compliant' },
  ];

  // Mock Merkle data
  const merkleData = {
    status: 'generated',
    rootHash: 'ca978112ca1bbdc16f7a08a27516ba5e4c614aca3a374760c4cc61f2a2f',
    treeDepth: 8,
    totalLeaves: 153,
    generatedAt: '2024-01-15T10:30:00Z',
    hashAlgorithm: 'SHA-256',
  };

  // Mock DeFi positions
  const defiPositions = [
    { id: 1, protocol: 'Aave', asset: 'USDC', amount: 2500000, riskScore: 'low', apy: '4.2%' },
    { id: 2, protocol: 'Curve', asset: 'stETH', amount: 340, riskScore: 'medium', apy: '3.8%' },
    { id: 3, protocol: 'Lido', asset: 'ETH', amount: 245, riskScore: 'low', apy: '3.2%' },
  ];

  // Mock reports
  const reports = [
    { id: 1, name: 'PoR AUP Report - Draft', type: 'PoR AUP', status: 'draft', createdAt: '2024-01-10', size: '2.4 MB' },
    { id: 2, name: 'Assurance Report - Q4 2023', type: 'Assurance', status: 'completed', createdAt: '2024-01-05', size: '3.1 MB' },
    { id: 3, name: 'Management Letter', type: 'Management Letter', status: 'completed', createdAt: '2023-12-28', size: '1.8 MB' },
  ];

  const filteredAssets = filterStatus === 'all'
    ? allAssets
    : allAssets.filter(a => a.status === filterStatus);

  const getStatusColor = (status) => {
    if (status === 'verified') return 'success';
    if (status === 'in_progress') return 'info';
    return 'pending';
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold text-simplyfi-navy mb-4">Engagement Information</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-simplyfi-text-muted">Client:</span>
                    <span className="font-medium text-simplyfi-navy">{engagement.client}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-simplyfi-text-muted">Audit Manager:</span>
                    <span className="font-medium text-simplyfi-navy">{engagement.manager}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-simplyfi-text-muted">Start Date:</span>
                    <span className="font-medium text-simplyfi-navy">{new Date(engagement.startDate).toLocaleDateString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-simplyfi-text-muted">Due Date:</span>
                    <span className="font-medium text-simplyfi-navy">{new Date(engagement.endDate).toLocaleDateString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-simplyfi-text-muted">Status:</span>
                    <StatusBadge status="info">In Progress</StatusBadge>
                  </div>
                </div>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-simplyfi-navy mb-4">Timeline & Phases</h3>
                <div className="space-y-2">
                  {timeline.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-3">
                      <div className="flex-shrink-0">
                        {item.status === 'completed' && <CheckCircle2 className="w-5 h-5 text-simplyfi-emerald" />}
                        {item.status === 'in_progress' && <Clock className="w-5 h-5 text-simplyfi-gold" />}
                        {item.status === 'pending' && <div className="w-5 h-5 rounded-full border-2 border-simplyfi-border-light" />}
                      </div>
                      <div className="flex-1">
                        <p className="font-medium text-simplyfi-navy">{item.phase}</p>
                      </div>
                      <span className="text-sm text-simplyfi-text-muted">{new Date(item.date).toLocaleDateString()}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        );

      case 'assets':
        return (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <p className="text-simplyfi-text-muted">Total: {allAssets.length} assets configured</p>
              <div className="flex gap-2">
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-3 py-2 border border-simplyfi-border-light rounded-lg text-simplyfi-text-muted focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                >
                  <option value="all">All Status</option>
                  <option value="verified">Verified</option>
                  <option value="in_progress">In Progress</option>
                  <option value="pending">Pending</option>
                </select>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredAssets.map((asset) => (
                <div key={asset.id} className="p-4 border border-simplyfi-border-light rounded-lg hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="font-semibold text-simplyfi-navy">{asset.name}</h4>
                    <StatusBadge status={getStatusColor(asset.status)} size="sm">
                      {asset.status.charAt(0).toUpperCase() + asset.status.slice(1).replace(/_/g, ' ')}
                    </StatusBadge>
                  </div>
                  <div className="mb-3">
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-simplyfi-text-muted">Progress</span>
                      <span className="font-medium text-simplyfi-navy">{asset.progress}%</span>
                    </div>
                    <div className="w-full bg-simplyfi-neutral-bg rounded-full h-2">
                      <div
                        className="bg-simplyfi-emerald h-2 rounded-full transition-all"
                        style={{ width: `${asset.progress}%` }}
                      />
                    </div>
                  </div>
                  <p className="text-sm text-simplyfi-text-muted">
                    {asset.count.toLocaleString()} units
                  </p>
                </div>
              ))}
            </div>
          </div>
        );

      case 'wallets':
        return (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-simplyfi-border-light">
                  <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Address</th>
                  <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Chain</th>
                  <th className="text-right py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Balance</th>
                  <th className="text-center py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Verified</th>
                </tr>
              </thead>
              <tbody>
                {wallets.map((wallet) => (
                  <tr key={wallet.id} className="border-b border-simplyfi-border-light hover:bg-simplyfi-neutral-bg">
                    <td className="py-4 px-4 font-mono text-sm text-simplyfi-navy truncate">{wallet.address}</td>
                    <td className="py-4 px-4 text-simplyfi-text-muted">{wallet.chain}</td>
                    <td className="py-4 px-4 text-right font-medium text-simplyfi-navy">{wallet.balance.toLocaleString()}</td>
                    <td className="py-4 px-4 text-center">
                      {wallet.verified ? (
                        <div className="flex justify-center">
                          <CheckCircle2 className="w-5 h-5 text-simplyfi-emerald" />
                        </div>
                      ) : (
                        <Clock className="w-5 h-5 text-simplyfi-gold mx-auto" />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );

      case 'reserves':
        return (
          <div className="space-y-6">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-simplyfi-border-light">
                    <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Asset</th>
                    <th className="text-right py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Reserves</th>
                    <th className="text-right py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Liabilities</th>
                    <th className="text-right py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Ratio</th>
                    <th className="text-center py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {reserves.map((reserve, idx) => (
                    <tr key={idx} className="border-b border-simplyfi-border-light hover:bg-simplyfi-neutral-bg">
                      <td className="py-4 px-4 font-medium text-simplyfi-navy">{reserve.asset}</td>
                      <td className="py-4 px-4 text-right text-simplyfi-navy">
                        {reserve.reserves < 1000 ? reserve.reserves.toFixed(2) : `${(reserve.reserves / 1000000).toFixed(2)}M`}
                      </td>
                      <td className="py-4 px-4 text-right text-simplyfi-text-muted">
                        {reserve.liabilities < 1000 ? reserve.liabilities.toFixed(2) : `${(reserve.liabilities / 1000000).toFixed(2)}M`}
                      </td>
                      <td className="py-4 px-4 text-right">
                        <span
                          className={`inline-block px-3 py-1 rounded-lg font-semibold text-sm ${
                            reserve.ratio >= 100
                              ? 'bg-simplyfi-emerald/10 text-simplyfi-emerald'
                              : 'bg-simplyfi-red-warning/10 text-simplyfi-red-warning'
                          }`}
                        >
                          {reserve.ratio.toFixed(2)}%
                        </span>
                      </td>
                      <td className="py-4 px-4 text-center">
                        <StatusBadge status={reserve.status === 'compliant' ? 'success' : 'error'} size="sm">
                          {reserve.status.charAt(0).toUpperCase() + reserve.status.slice(1).replace(/_/g, ' ')}
                        </StatusBadge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );

      case 'merkle':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 bg-simplyfi-neutral-bg rounded-lg">
                <p className="text-simplyfi-text-muted text-sm mb-1">Status</p>
                <p className="text-xl font-bold text-simplyfi-emerald">Generated</p>
              </div>
              <div className="p-4 bg-simplyfi-neutral-bg rounded-lg">
                <p className="text-simplyfi-text-muted text-sm mb-1">Total Leaves</p>
                <p className="text-xl font-bold text-simplyfi-navy">{merkleData.totalLeaves}</p>
              </div>
              <div className="p-4 bg-simplyfi-neutral-bg rounded-lg">
                <p className="text-simplyfi-text-muted text-sm mb-1">Tree Depth</p>
                <p className="text-xl font-bold text-simplyfi-navy">{merkleData.treeDepth}</p>
              </div>
              <div className="p-4 bg-simplyfi-neutral-bg rounded-lg">
                <p className="text-simplyfi-text-muted text-sm mb-1">Algorithm</p>
                <p className="text-xl font-bold text-simplyfi-navy">{merkleData.hashAlgorithm}</p>
              </div>
            </div>
            <div className="p-6 bg-simplyfi-navy/5 rounded-lg border border-simplyfi-border-light">
              <p className="text-simplyfi-text-muted text-sm mb-2">Root Hash</p>
              <p className="font-mono text-sm text-simplyfi-navy break-all">{merkleData.rootHash}</p>
            </div>
            <p className="text-sm text-simplyfi-text-muted">
              Generated: {new Date(merkleData.generatedAt).toLocaleString()}
            </p>
          </div>
        );

      case 'defi':
        return (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-simplyfi-border-light">
                  <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Protocol</th>
                  <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Asset</th>
                  <th className="text-right py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Amount</th>
                  <th className="text-center py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Risk</th>
                  <th className="text-right py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">APY</th>
                </tr>
              </thead>
              <tbody>
                {defiPositions.map((position) => (
                  <tr key={position.id} className="border-b border-simplyfi-border-light hover:bg-simplyfi-neutral-bg">
                    <td className="py-4 px-4 font-medium text-simplyfi-navy">{position.protocol}</td>
                    <td className="py-4 px-4 text-simplyfi-text-muted">{position.asset}</td>
                    <td className="py-4 px-4 text-right font-medium text-simplyfi-navy">
                      {position.amount.toLocaleString()}
                    </td>
                    <td className="py-4 px-4 text-center">
                      <span
                        className={`inline-block px-3 py-1 rounded-lg font-semibold text-sm ${
                          position.riskScore === 'low'
                            ? 'bg-simplyfi-emerald/10 text-simplyfi-emerald'
                            : position.riskScore === 'medium'
                            ? 'bg-simplyfi-gold/10 text-simplyfi-gold'
                            : 'bg-simplyfi-red-warning/10 text-simplyfi-red-warning'
                        }`}
                      >
                        {position.riskScore.charAt(0).toUpperCase() + position.riskScore.slice(1)}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-right text-simplyfi-navy font-medium">{position.apy}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );

      case 'reports':
        return (
          <div className="space-y-3">
            {reports.map((report) => (
              <div key={report.id} className="flex items-center justify-between p-4 border border-simplyfi-border-light rounded-lg hover:shadow-md transition-shadow">
                <div className="flex-1">
                  <h4 className="font-semibold text-simplyfi-navy mb-1">{report.name}</h4>
                  <div className="flex gap-4 text-sm text-simplyfi-text-muted">
                    <span>{report.type}</span>
                    <span>{new Date(report.createdAt).toLocaleDateString()}</span>
                    <span>{report.size}</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <StatusBadge
                    status={report.status === 'completed' ? 'success' : 'pending'}
                    size="sm"
                  >
                    {report.status.charAt(0).toUpperCase() + report.status.slice(1)}
                  </StatusBadge>
                  <button className="p-2 hover:bg-simplyfi-neutral-bg rounded-lg transition-colors">
                    <Download className="w-5 h-5 text-simplyfi-navy" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="p-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-simplyfi-navy mb-2">{engagement.client}</h1>
            <p className="text-simplyfi-text-muted">{engagement.auditType} Engagement</p>
          </div>
          <StatusBadge status="info" size="lg">
            In Progress
          </StatusBadge>
        </div>
      </Card>

      {/* Tabs */}
      <Card className="p-0">
        <div className="border-b border-simplyfi-border-light">
          <div className="flex flex-wrap overflow-x-auto">
            {[
              { key: 'overview', label: 'Overview' },
              { key: 'assets', label: 'Assets (153)' },
              { key: 'wallets', label: 'Wallets' },
              { key: 'reserves', label: 'Reserves' },
              { key: 'merkle', label: 'Merkle Tree' },
              { key: 'defi', label: 'DeFi Positions' },
              { key: 'reports', label: 'Reports' },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`px-6 py-4 font-medium border-b-2 transition-colors whitespace-nowrap ${
                  activeTab === tab.key
                    ? 'border-simplyfi-navy text-simplyfi-navy'
                    : 'border-transparent text-simplyfi-text-muted hover:text-simplyfi-navy'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
        <div className="p-6">
          {renderTabContent()}
        </div>
      </Card>
    </div>
  );
};

export default EngagementDetail;
