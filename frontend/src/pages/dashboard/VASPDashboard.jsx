import React, { useState } from 'react';
import { TrendingUp, AlertTriangle, CheckCircle2, Clock } from 'lucide-react';
import Card from '../../components/common/Card';
import StatCard from '../../components/common/StatCard';
import StatusBadge from '../../components/common/StatusBadge';
import ReserveRatioChart from '../../components/dashboard/ReserveRatioChart';

const VASPDashboard = () => {
  const [sortBy, setSortBy] = useState('ratio');

  // Mock asset breakdown data
  const assetBreakdown = [
    {
      id: 1,
      asset: 'Bitcoin (BTC)',
      symbol: 'BTC',
      reserves: 1245.32,
      liabilities: 1230.15,
      ratio: 101.24,
      status: 'compliant',
      trend: 'up',
    },
    {
      id: 2,
      asset: 'Ethereum (ETH)',
      symbol: 'ETH',
      reserves: 8945.67,
      liabilities: 8850.44,
      ratio: 101.08,
      status: 'compliant',
      trend: 'up',
    },
    {
      id: 3,
      asset: 'USDC',
      symbol: 'USDC',
      reserves: 12560000,
      liabilities: 12500000,
      ratio: 100.48,
      status: 'compliant',
      trend: 'stable',
    },
    {
      id: 4,
      asset: 'USDT',
      symbol: 'USDT',
      reserves: 18900000,
      liabilities: 18750000,
      ratio: 100.8,
      status: 'compliant',
      trend: 'up',
    },
    {
      id: 5,
      asset: 'Solana (SOL)',
      symbol: 'SOL',
      reserves: 5420.12,
      liabilities: 5300.99,
      ratio: 102.24,
      status: 'compliant',
      trend: 'up',
    },
    {
      id: 6,
      asset: 'Polkadot (DOT)',
      symbol: 'DOT',
      reserves: 2800.45,
      liabilities: 2825.67,
      ratio: 99.1,
      status: 'under_reserved',
      trend: 'down',
    },
    {
      id: 7,
      asset: 'Cardano (ADA)',
      symbol: 'ADA',
      reserves: 3200.0,
      liabilities: 3150.0,
      ratio: 101.59,
      status: 'compliant',
      trend: 'stable',
    },
    {
      id: 8,
      asset: 'Ripple (XRP)',
      symbol: 'XRP',
      reserves: 4100.55,
      liabilities: 4000.12,
      ratio: 102.51,
      status: 'compliant',
      trend: 'up',
    },
  ];

  // Mock reconciliation status
  const lastReconciliation = {
    date: '2024-01-15T10:30:00Z',
    status: 'completed',
    assetsVerified: 8,
    discrepancies: 1,
    nextScheduled: '2024-01-22T10:30:00Z',
  };

  // Mock upcoming audits
  const upcomingAudits = [
    {
      id: 1,
      auditType: 'Quarterly PoR',
      status: 'scheduled',
      dueDate: '2024-02-15',
      daysRemaining: 31,
    },
    {
      id: 2,
      auditType: 'VARA Compliance Review',
      status: 'scheduled',
      dueDate: '2024-03-01',
      daysRemaining: 45,
    },
    {
      id: 3,
      auditType: 'DeFi Position Audit',
      status: 'in_progress',
      dueDate: '2024-01-25',
      daysRemaining: 10,
    },
  ];

  // Alerts for under-reserved assets
  const alerts = assetBreakdown.filter((a) => a.status === 'under_reserved');

  const getStatusIcon = (status) => {
    if (status === 'compliant') return <CheckCircle2 className="w-5 h-5 text-simplyfi-emerald" />;
    if (status === 'under_reserved') return <AlertTriangle className="w-5 h-5 text-simplyfi-red-warning" />;
    return <Clock className="w-5 h-5 text-simplyfi-gold" />;
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    if (num >= 1000) return `$${(num / 1000).toFixed(2)}K`;
    return `$${num.toFixed(2)}`;
  };

  return (
    <div className="space-y-6">
      {/* Reserve Ratio Overview */}
      <Card className="p-8 bg-gradient-to-br from-simplyfi-navy/5 to-simplyfi-emerald/5">
        <div className="text-center">
          <p className="text-simplyfi-text-muted text-lg mb-2">Overall Reserve Status</p>
          <div className="flex items-baseline justify-center gap-3">
            <span className="text-6xl font-bold text-simplyfi-navy">100.2%</span>
            <span className="text-2xl font-semibold text-simplyfi-emerald">Fully Reserved</span>
          </div>
          <div className="mt-4 flex items-center justify-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-simplyfi-emerald" />
            <p className="text-simplyfi-emerald font-medium">All assets are properly reserved</p>
          </div>
        </div>
      </Card>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          label="Total Assets"
          value={assetBreakdown.length.toString()}
          icon={TrendingUp}
          color="navy"
        />
        <StatCard
          label="Compliant Assets"
          value={assetBreakdown.filter((a) => a.status === 'compliant').length.toString()}
          icon={CheckCircle2}
          color="emerald"
        />
        <StatCard
          label="Under-Reserved"
          value={alerts.length.toString()}
          icon={AlertTriangle}
          color="navy"
          backgroundColor="bg-simplyfi-red-warning/10"
        />
      </div>

      {/* Asset Breakdown Table */}
      <Card className="p-6">
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-xl font-bold text-simplyfi-navy">Asset Reserve Ratios</h2>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 border border-simplyfi-border-light rounded-lg text-simplyfi-text-muted focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
          >
            <option value="ratio">Sort by Ratio</option>
            <option value="asset">Sort by Asset</option>
            <option value="status">Sort by Status</option>
          </select>
        </div>
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
              {assetBreakdown.map((asset) => (
                <tr key={asset.id} className="border-b border-simplyfi-border-light hover:bg-simplyfi-neutral-bg transition-colors">
                  <td className="py-4 px-4">
                    <div>
                      <p className="font-semibold text-simplyfi-navy">{asset.asset}</p>
                      <p className="text-sm text-simplyfi-text-muted">{asset.symbol}</p>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-right text-simplyfi-navy font-medium">
                    {asset.reserves < 1000000
                      ? asset.reserves.toLocaleString(undefined, { maximumFractionDigits: 2 })
                      : formatNumber(asset.reserves)}
                  </td>
                  <td className="py-4 px-4 text-right text-simplyfi-text-muted">
                    {asset.liabilities < 1000000
                      ? asset.liabilities.toLocaleString(undefined, { maximumFractionDigits: 2 })
                      : formatNumber(asset.liabilities)}
                  </td>
                  <td className="py-4 px-4 text-right">
                    <span
                      className={`inline-block px-3 py-1 rounded-lg font-semibold text-sm ${
                        asset.ratio >= 100
                          ? 'bg-simplyfi-emerald/10 text-simplyfi-emerald'
                          : 'bg-simplyfi-red-warning/10 text-simplyfi-red-warning'
                      }`}
                    >
                      {asset.ratio.toFixed(2)}%
                    </span>
                  </td>
                  <td className="py-4 px-4 text-center">
                    <div className="flex justify-center">
                      {getStatusIcon(asset.status)}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Alerts Section */}
      {alerts.length > 0 && (
        <Card className="p-6 border-l-4 border-simplyfi-red-warning bg-simplyfi-red-warning/5">
          <div className="flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-simplyfi-red-warning flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h3 className="font-bold text-simplyfi-red-warning mb-3">Under-Reserved Assets Alert</h3>
              <div className="space-y-2">
                {alerts.map((alert) => (
                  <div key={alert.id} className="flex items-center justify-between p-3 bg-white rounded-lg border border-simplyfi-red-warning/20">
                    <div>
                      <p className="font-medium text-simplyfi-navy">{alert.asset}</p>
                      <p className="text-sm text-simplyfi-text-muted">Current ratio: {alert.ratio.toFixed(2)}%</p>
                    </div>
                    <button className="px-4 py-2 bg-simplyfi-red-warning/10 text-simplyfi-red-warning rounded-lg font-medium hover:bg-simplyfi-red-warning/20 transition-colors">
                      Action Required
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Latest Reconciliation Status */}
        <Card className="p-6">
          <h2 className="text-xl font-bold text-simplyfi-navy mb-6">Latest Reconciliation</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center pb-4 border-b border-simplyfi-border-light">
              <span className="text-simplyfi-text-muted">Last Updated</span>
              <span className="font-semibold text-simplyfi-navy">
                {new Date(lastReconciliation.date).toLocaleDateString()} at{' '}
                {new Date(lastReconciliation.date).toLocaleTimeString()}
              </span>
            </div>
            <div className="flex justify-between items-center pb-4 border-b border-simplyfi-border-light">
              <span className="text-simplyfi-text-muted">Status</span>
              <StatusBadge status="success">Completed</StatusBadge>
            </div>
            <div className="flex justify-between items-center pb-4 border-b border-simplyfi-border-light">
              <span className="text-simplyfi-text-muted">Assets Verified</span>
              <span className="font-semibold text-simplyfi-navy">{lastReconciliation.assetsVerified}</span>
            </div>
            <div className="flex justify-between items-center pb-4 border-b border-simplyfi-border-light">
              <span className="text-simplyfi-text-muted">Discrepancies Found</span>
              <span className="font-semibold text-simplyfi-navy">{lastReconciliation.discrepancies}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-simplyfi-text-muted">Next Scheduled</span>
              <span className="font-semibold text-simplyfi-navy">
                {new Date(lastReconciliation.nextScheduled).toLocaleDateString()}
              </span>
            </div>
          </div>
        </Card>

        {/* Upcoming Audits */}
        <Card className="p-6">
          <h2 className="text-xl font-bold text-simplyfi-navy mb-6">Upcoming Audits</h2>
          <div className="space-y-3">
            {upcomingAudits.map((audit) => (
              <div
                key={audit.id}
                className="p-4 border border-simplyfi-border-light rounded-lg hover:border-simplyfi-gold/50 transition-colors"
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-semibold text-simplyfi-navy">{audit.auditType}</h3>
                  <StatusBadge
                    status={audit.status === 'scheduled' ? 'pending' : 'info'}
                    size="sm"
                  >
                    {audit.status === 'scheduled' ? 'Scheduled' : 'In Progress'}
                  </StatusBadge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-simplyfi-text-muted">
                    Due: {new Date(audit.dueDate).toLocaleDateString()}
                  </span>
                  <span className={`text-sm font-medium ${
                    audit.daysRemaining <= 7 ? 'text-simplyfi-red-warning' : 'text-simplyfi-text-muted'
                  }`}>
                    {audit.daysRemaining} days
                  </span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default VASPDashboard;
