import React, { useState, useEffect } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, TrendingUp, Shield, CheckCircle, Plus, FileText, Zap } from 'lucide-react';
import Card from '../../components/common/Card';
import StatCard from '../../components/common/StatCard';
import StatusBadge from '../../components/common/StatusBadge';
import Button from '../../components/common/Button';
import DataTable from '../../components/common/DataTable';
import VerificationTimeline from '../../components/audit/VerificationTimeline';
import ComplianceScorecard from '../../components/audit/ComplianceScorecard';

const AuditorDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data for reserve health
  const reserveHealthData = [
    { asset: 'Bitcoin (BTC)', reserves: 15420, liabilities: 15200, ratio: 101.4 },
    { asset: 'Ethereum (ETH)', reserves: 8945, liabilities: 8850, ratio: 101.1 },
    { asset: 'USDC', reserves: 12560, liabilities: 12500, ratio: 100.5 },
    { asset: 'USDT', reserves: 18900, liabilities: 18750, ratio: 100.8 },
    { asset: 'Solana (SOL)', reserves: 5420, liabilities: 5300, ratio: 102.3 },
    { asset: 'Cardano (ADA)', reserves: 3200, liabilities: 3150, ratio: 101.6 },
    { asset: 'Ripple (XRP)', reserves: 4100, liabilities: 4000, ratio: 102.5 },
    { asset: 'Polkadot (DOT)', reserves: 2800, liabilities: 2750, ratio: 101.8 },
    { asset: 'Polygon (MATIC)', reserves: 6340, liabilities: 6200, ratio: 102.3 },
    { asset: 'Cosmos (ATOM)', reserves: 1980, liabilities: 1920, ratio: 103.1 },
    { asset: 'Litecoin (LTC)', reserves: 3450, liabilities: 3400, ratio: 101.5 },
    { asset: 'Chainlink (LINK)', reserves: 2890, liabilities: 2800, ratio: 103.2 },
    { asset: 'Uniswap (UNI)', reserves: 2340, liabilities: 2300, ratio: 101.7 },
    { asset: 'Aave (AAVE)', reserves: 1950, liabilities: 1900, ratio: 102.6 },
    { asset: 'Curve (CRV)', reserves: 1650, liabilities: 1620, ratio: 101.8 },
    { asset: 'Lido (LDO)', reserves: 2100, liabilities: 2050, ratio: 102.4 },
    { asset: 'Convex (CVX)', reserves: 890, liabilities: 850, ratio: 104.7 },
    { asset: 'Yearn (YFI)', reserves: 1240, liabilities: 1200, ratio: 103.3 },
    { asset: 'MakerDAO (MKR)', reserves: 1560, liabilities: 1520, ratio: 102.6 },
    { asset: 'Compound (COMP)', reserves: 1320, liabilities: 1280, ratio: 103.1 },
  ];

  // Mock active engagements
  const activeEngagements = [
    {
      id: 1,
      client: 'Crypto Exchange Inc.',
      status: 'in_progress',
      assets: 47,
      dueDate: '2024-03-15',
      progress: 68,
    },
    {
      id: 2,
      client: 'Digital Assets Fund',
      status: 'in_progress',
      assets: 23,
      dueDate: '2024-03-22',
      progress: 45,
    },
    {
      id: 3,
      client: 'Decentralized Exchange Ltd',
      status: 'in_progress',
      assets: 34,
      dueDate: '2024-04-01',
      progress: 32,
    },
    {
      id: 4,
      client: 'Custody Platform Corp',
      status: 'pending',
      assets: 28,
      dueDate: '2024-04-10',
      progress: 5,
    },
  ];

  // Mock verification activity
  const verificationActivity = [
    {
      id: 1,
      timestamp: '2024-01-15T14:32:00Z',
      type: 'on_chain',
      asset: 'Bitcoin (BTC)',
      status: 'verified',
      details: 'Verified 1,245 BTC across 8 addresses',
    },
    {
      id: 2,
      timestamp: '2024-01-15T13:18:00Z',
      type: 'custodian',
      asset: 'Ethereum (ETH)',
      status: 'verified',
      details: 'Custodian confirmation received from Coinbase Custody',
    },
    {
      id: 3,
      timestamp: '2024-01-15T11:45:00Z',
      type: 'on_chain',
      asset: 'USDC',
      status: 'verified',
      details: 'Verified 12.5M USDC across Ethereum and Polygon',
    },
    {
      id: 4,
      timestamp: '2024-01-15T10:22:00Z',
      type: 'defi',
      asset: 'Lido stETH',
      status: 'verified',
      details: 'Verified 2,340 stETH in Curve pool',
    },
    {
      id: 5,
      timestamp: '2024-01-14T16:55:00Z',
      type: 'on_chain',
      asset: 'Solana (SOL)',
      status: 'verified',
      details: 'Verified 5,420 SOL on Solana mainnet',
    },
  ];

  // VARA Compliance data
  const complianceData = [
    { name: 'Compliant', value: 38, color: '#10b981' },
    { name: 'Non-Compliant', value: 4, color: '#ef4444' },
    { name: 'Partial', value: 8, color: '#f59e0b' },
  ];

  const handleStartEngagement = () => {
    console.log('Starting new engagement...');
  };

  const handleGenerateReport = () => {
    console.log('Generating report...');
  };

  const handleRunVerification = () => {
    console.log('Running verification...');
  };

  return (
    <div className="space-y-6">
      {/* Summary Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          label="Active Engagements"
          value="12"
          icon={Activity}
          color="navy"
          trend="up"
          trendValue="+2"
        />
        <StatCard
          label="Assets Under Audit"
          value="1,253"
          icon={TrendingUp}
          color="emerald"
          trend="up"
          trendValue="+145"
        />
        <StatCard
          label="Total Reserves Verified"
          value="$2.4B"
          icon={Shield}
          color="gold"
          trend="up"
          trendValue="+8.3"
        />
        <StatCard
          label="Compliance Score"
          value="94.2%"
          icon={CheckCircle}
          color="emerald"
          trend="up"
          trendValue="+1.2"
        />
      </div>

      {/* Reserve Health Overview */}
      <Card className="p-6">
        <div className="mb-6">
          <h2 className="text-xl font-bold text-simplyfi-navy mb-1">Reserve Health Overview</h2>
          <p className="text-simplyfi-text-muted text-sm">Top 20 Assets - Reserves vs Liabilities</p>
        </div>
        <div className="w-full h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={reserveHealthData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="asset" angle={-45} textAnchor="end" height={120} fontSize={12} />
              <YAxis />
              <Tooltip
                formatter={(value) => `$${(value / 1000).toFixed(1)}K`}
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Bar dataKey="reserves" fill="#10b981" radius={[8, 8, 0, 0]} />
              <Bar dataKey="liabilities" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Engagements Table */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <div className="mb-6">
              <h2 className="text-xl font-bold text-simplyfi-navy">Active Engagements</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-simplyfi-border-light">
                    <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Client</th>
                    <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Status</th>
                    <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Assets</th>
                    <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Due Date</th>
                    <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Progress</th>
                  </tr>
                </thead>
                <tbody>
                  {activeEngagements.map((engagement) => (
                    <tr key={engagement.id} className="border-b border-simplyfi-border-light hover:bg-simplyfi-neutral-bg">
                      <td className="py-4 px-4 font-medium text-simplyfi-navy">{engagement.client}</td>
                      <td className="py-4 px-4">
                        <StatusBadge
                          status={engagement.status === 'in_progress' ? 'info' : 'pending'}
                          size="sm"
                        >
                          {engagement.status === 'in_progress' ? 'In Progress' : 'Pending'}
                        </StatusBadge>
                      </td>
                      <td className="py-4 px-4 text-simplyfi-text-muted">{engagement.assets}</td>
                      <td className="py-4 px-4 text-simplyfi-text-muted text-sm">
                        {new Date(engagement.dueDate).toLocaleDateString()}
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-simplyfi-neutral-bg rounded-full h-2">
                            <div
                              className="bg-simplyfi-emerald h-2 rounded-full transition-all"
                              style={{ width: `${engagement.progress}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium text-simplyfi-text-muted min-w-12">
                            {engagement.progress}%
                          </span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </div>

        {/* VARA Compliance Summary */}
        <Card className="p-6">
          <div className="mb-6">
            <h2 className="text-xl font-bold text-simplyfi-navy">VARA Compliance</h2>
          </div>
          <div className="w-full h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={complianceData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {complianceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-6 space-y-3">
            {complianceData.map((item) => (
              <div key={item.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-sm text-simplyfi-text-muted">{item.name}</span>
                </div>
                <span className="font-semibold text-simplyfi-navy">{item.value}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Recent Verification Activity */}
      <VerificationTimeline events={verificationActivity} />

      {/* Quick Actions */}
      <Card className="p-6">
        <h2 className="text-xl font-bold text-simplyfi-navy mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Button
            variant="primary"
            size="lg"
            className="flex items-center justify-center gap-2"
            onClick={handleStartEngagement}
          >
            <Plus className="w-5 h-5" />
            Start New Engagement
          </Button>
          <Button
            variant="secondary"
            size="lg"
            className="flex items-center justify-center gap-2"
            onClick={handleGenerateReport}
          >
            <FileText className="w-5 h-5" />
            Generate Report
          </Button>
          <Button
            variant="secondary"
            size="lg"
            className="flex items-center justify-center gap-2"
            onClick={handleRunVerification}
          >
            <Zap className="w-5 h-5" />
            Run Verification
          </Button>
        </div>
      </Card>

      {/* VARA Compliance Scorecard */}
      <ComplianceScorecard />
    </div>
  );
};

export default AuditorDashboard;
