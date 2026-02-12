import React, { useState } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Search, CheckCircle2, Clock, AlertCircle, ExternalLink, Zap } from 'lucide-react';
import Card from '../../components/common/Card';
import StatusBadge from '../../components/common/StatusBadge';
import Button from '../../components/common/Button';

const BlockchainExplorer = () => {
  const [selectedChain, setSelectedChain] = useState('ethereum');
  const [addressInput, setAddressInput] = useState('');
  const [txHashInput, setTxHashInput] = useState('');
  const [addressResult, setAddressResult] = useState(null);
  const [txResult, setTxResult] = useState(null);

  const chains = [
    { id: 'bitcoin', name: 'Bitcoin', symbol: 'BTC', color: '#F7931A' },
    { id: 'ethereum', name: 'Ethereum', symbol: 'ETH', color: '#627EEA' },
    { id: 'solana', name: 'Solana', symbol: 'SOL', color: '#14F195' },
    { id: 'polygon', name: 'Polygon', symbol: 'MATIC', color: '#8247E5' },
    { id: 'cardano', name: 'Cardano', symbol: 'ADA', color: '#0033AD' },
  ];

  // Mock bulk verification data
  const bulkVerifications = [
    { id: 1, address: '1A1z7agoat2YLZW51Bc7M7kMccKzd6Zdbf', chain: 'Bitcoin', status: 'completed', progress: 100, balance: 45.32 },
    { id: 2, address: '0x742d35Cc6634C0532925a3b844Bc9e7595f1234A', chain: 'Ethereum', status: 'completed', progress: 100, balance: 8945.67 },
    { id: 3, address: 'So11111111111111111111111111111111111111112', chain: 'Solana', status: 'in_progress', progress: 67, balance: 5420.12 },
    { id: 4, address: '0x1111111254fb6c44bac0bed2854e76f90643097d', chain: 'Ethereum', status: 'in_progress', progress: 45, balance: 12500000 },
    { id: 5, address: 'addr1w90pxkl8e6xk7m6xz', chain: 'Cardano', status: 'pending', progress: 5, balance: 3200 },
  ];

  // Mock on-chain vs reported data
  const balanceComparisonData = [
    { asset: 'Bitcoin', onChain: 1245, reported: 1230, variance: 15 },
    { asset: 'Ethereum', onChain: 8945, reported: 8850, variance: 95 },
    { asset: 'USDC', onChain: 12560, reported: 12500, variance: 60 },
    { asset: 'USDT', onChain: 18900, reported: 18750, variance: 150 },
    { asset: 'Solana', onChain: 5420, reported: 5300, variance: 120 },
  ];

  // Mock transaction history for verification progress
  const transactionHistory = [
    { timestamp: '2024-01-15T14:32:00Z', txHash: '0xabc123def456', status: 'confirmed', blocks: 12 },
    { timestamp: '2024-01-15T13:18:00Z', txHash: '0xdef789ghi012', status: 'confirmed', blocks: 24 },
    { timestamp: '2024-01-15T11:45:00Z', txHash: '0xghi345jkl678', status: 'pending', blocks: 0 },
  ];

  const handleVerifyAddress = () => {
    if (!addressInput.trim()) {
      setAddressResult(null);
      return;
    }

    const mockResult = {
      address: addressInput,
      chain: selectedChain,
      balance: (Math.random() * 100000).toFixed(2),
      verified: true,
      verifiedAt: new Date().toISOString(),
      transactions: Math.floor(Math.random() * 500),
      status: Math.random() > 0.1 ? 'verified' : 'unverified',
    };

    setAddressResult(mockResult);
  };

  const handleVerifyTransaction = () => {
    if (!txHashInput.trim()) {
      setTxResult(null);
      return;
    }

    const mockTxResult = {
      txHash: txHashInput,
      status: Math.random() > 0.2 ? 'confirmed' : 'pending',
      confirmations: Math.floor(Math.random() * 100),
      blockNumber: Math.floor(Math.random() * 19000000),
      from: '0x742d35Cc6634C0532925a3b844Bc9e7595f1234A',
      to: '0x1111111254fb6c44bac0bed2854e76f90643097d',
      value: (Math.random() * 100).toFixed(4),
      gasUsed: (Math.random() * 100000).toFixed(0),
      gasPrice: (Math.random() * 100).toFixed(2),
      timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString(),
    };

    setTxResult(mockTxResult);
  };

  const currentChain = chains.find((c) => c.id === selectedChain);

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="p-6">
        <h1 className="text-3xl font-bold text-simplyfi-navy mb-2">Blockchain Verification</h1>
        <p className="text-simplyfi-text-muted">On-chain verification of cryptocurrency addresses and transactions</p>
      </Card>

      {/* Chain Selector */}
      <Card className="p-6">
        <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Select Blockchain</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {chains.map((chain) => (
            <button
              key={chain.id}
              onClick={() => setSelectedChain(chain.id)}
              className={`p-4 rounded-lg border-2 transition-all ${
                selectedChain === chain.id
                  ? 'border-simplyfi-navy bg-simplyfi-navy/5'
                  : 'border-simplyfi-border-light hover:border-simplyfi-navy'
              }`}
            >
              <div className="text-center">
                <div
                  className="w-8 h-8 rounded-full mx-auto mb-2"
                  style={{ backgroundColor: chain.color }}
                />
                <p className="font-semibold text-simplyfi-navy text-sm">{chain.name}</p>
                <p className="text-xs text-simplyfi-text-muted">{chain.symbol}</p>
              </div>
            </button>
          ))}
        </div>
      </Card>

      {/* Address Verification Panel */}
      <Card className="p-6 border-l-4" style={{ borderLeftColor: currentChain?.color }}>
        <h2 className="text-lg font-bold text-simplyfi-navy mb-4 flex items-center gap-2">
          <Search className="w-5 h-5" />
          Address Verification
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-simplyfi-navy mb-2">
              {currentChain?.name} Address
            </label>
            <input
              type="text"
              value={addressInput}
              onChange={(e) => setAddressInput(e.target.value)}
              placeholder={`Enter ${currentChain?.name} address...`}
              className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
            />
          </div>

          <Button
            variant="primary"
            className="w-full"
            onClick={handleVerifyAddress}
          >
            Verify Address
          </Button>

          {addressResult && (
            <div className={`p-4 rounded-lg border-2 ${
              addressResult.status === 'verified'
                ? 'bg-simplyfi-emerald/10 border-simplyfi-emerald'
                : 'bg-simplyfi-red-warning/10 border-simplyfi-red-warning'
            }`}>
              <div className="flex items-start gap-3">
                {addressResult.status === 'verified' ? (
                  <CheckCircle2 className="w-6 h-6 text-simplyfi-emerald flex-shrink-0 mt-1" />
                ) : (
                  <AlertCircle className="w-6 h-6 text-simplyfi-red-warning flex-shrink-0 mt-1" />
                )}
                <div className="flex-1">
                  <h3 className={`font-bold mb-3 ${
                    addressResult.status === 'verified' ? 'text-simplyfi-emerald' : 'text-simplyfi-red-warning'
                  }`}>
                    {addressResult.status === 'verified' ? 'Verified' : 'Not Verified'}
                  </h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-simplyfi-text-muted">Balance:</span>
                      <span className="font-medium text-simplyfi-navy">{addressResult.balance} {currentChain?.symbol}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-simplyfi-text-muted">Transactions:</span>
                      <span className="font-medium text-simplyfi-navy">{addressResult.transactions}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-simplyfi-text-muted">Verified At:</span>
                      <span className="font-medium text-simplyfi-navy">
                        {new Date(addressResult.verifiedAt).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Bulk Verification Status */}
      <Card className="p-6">
        <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Bulk Verification Status</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-simplyfi-border-light">
                <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Address</th>
                <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Chain</th>
                <th className="text-right py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Balance</th>
                <th className="text-center py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Status</th>
                <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">Progress</th>
              </tr>
            </thead>
            <tbody>
              {bulkVerifications.map((verification) => (
                <tr key={verification.id} className="border-b border-simplyfi-border-light hover:bg-simplyfi-neutral-bg">
                  <td className="py-4 px-4 font-mono text-sm text-simplyfi-navy truncate">{verification.address}</td>
                  <td className="py-4 px-4 text-simplyfi-text-muted">{verification.chain}</td>
                  <td className="py-4 px-4 text-right font-medium text-simplyfi-navy">
                    {verification.balance.toLocaleString()}
                  </td>
                  <td className="py-4 px-4 text-center">
                    <StatusBadge
                      status={
                        verification.status === 'completed'
                          ? 'success'
                          : verification.status === 'in_progress'
                          ? 'info'
                          : 'pending'
                      }
                      size="sm"
                    >
                      {verification.status === 'completed'
                        ? 'Verified'
                        : verification.status === 'in_progress'
                        ? 'In Progress'
                        : 'Pending'}
                    </StatusBadge>
                  </td>
                  <td className="py-4 px-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-simplyfi-neutral-bg rounded-full h-2">
                        <div
                          className="bg-simplyfi-emerald h-2 rounded-full transition-all"
                          style={{ width: `${verification.progress}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-simplyfi-text-muted min-w-10">
                        {verification.progress}%
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Balance Comparison Chart */}
      <Card className="p-6">
        <h2 className="text-lg font-bold text-simplyfi-navy mb-4">On-Chain vs Reported Balance Comparison</h2>
        <div className="w-full h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={balanceComparisonData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="asset" />
              <YAxis />
              <Tooltip
                formatter={(value) => `$${value.toLocaleString()}`}
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Bar dataKey="onChain" fill="#10b981" name="On-Chain Verified" radius={[8, 8, 0, 0]} />
              <Bar dataKey="reported" fill="#3b82f6" name="Reported Amount" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-6 p-4 bg-simplyfi-emerald/10 rounded-lg border border-simplyfi-emerald/30">
          <p className="text-sm text-simplyfi-emerald font-medium">
            All verified balances match reported amounts within acceptable variance (&lt; 0.2%)
          </p>
        </div>
      </Card>

      {/* Transaction Verification */}
      <Card className="p-6">
        <h2 className="text-lg font-bold text-simplyfi-navy mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5" />
          Transaction Verification
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-simplyfi-navy mb-2">Transaction Hash</label>
            <input
              type="text"
              value={txHashInput}
              onChange={(e) => setTxHashInput(e.target.value)}
              placeholder="0x1234567890abcdef..."
              className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
            />
          </div>

          <Button
            variant="primary"
            className="w-full"
            onClick={handleVerifyTransaction}
          >
            Verify Transaction
          </Button>

          {txResult && (
            <div className={`p-4 rounded-lg border-2 ${
              txResult.status === 'confirmed'
                ? 'bg-simplyfi-emerald/10 border-simplyfi-emerald'
                : 'bg-simplyfi-gold/10 border-simplyfi-gold'
            }`}>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Transaction Hash:</span>
                  <span className="font-mono text-xs text-simplyfi-navy truncate">{txResult.txHash}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Status:</span>
                  <StatusBadge
                    status={txResult.status === 'confirmed' ? 'success' : 'info'}
                    size="sm"
                  >
                    {txResult.status === 'confirmed' ? 'Confirmed' : 'Pending'}
                  </StatusBadge>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Confirmations:</span>
                  <span className="font-medium text-simplyfi-navy">{txResult.confirmations}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Block Number:</span>
                  <span className="font-medium text-simplyfi-navy">{txResult.blockNumber.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Value:</span>
                  <span className="font-medium text-simplyfi-navy">{txResult.value} ETH</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Gas Used:</span>
                  <span className="font-medium text-simplyfi-navy">{txResult.gasUsed}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Recent Transactions */}
      <Card className="p-6">
        <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Recent Verifications</h2>
        <div className="space-y-3">
          {transactionHistory.map((tx, idx) => (
            <div key={idx} className="p-4 border border-simplyfi-border-light rounded-lg hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    {tx.status === 'confirmed' ? (
                      <CheckCircle2 className="w-5 h-5 text-simplyfi-emerald" />
                    ) : (
                      <Clock className="w-5 h-5 text-simplyfi-gold" />
                    )}
                    <span className="font-mono text-sm text-simplyfi-navy">{tx.txHash}</span>
                  </div>
                  <p className="text-xs text-simplyfi-text-muted">
                    {new Date(tx.timestamp).toLocaleString()}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-simplyfi-navy mb-1">
                    {tx.blocks} blocks
                  </p>
                  <p className="text-xs text-simplyfi-text-muted">
                    {tx.status === 'confirmed' ? 'Confirmed' : 'Pending'}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default BlockchainExplorer;
