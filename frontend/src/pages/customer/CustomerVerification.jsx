import React, { useState } from 'react';
import { Search, CheckCircle2, AlertCircle, Shield, Lock, ExternalLink } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';

const CustomerVerification = () => {
  const [verificationId, setVerificationId] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleVerify = () => {
    if (!verificationId.trim()) return;

    setIsLoading(true);
    setTimeout(() => {
      // Simulate verification
      setVerificationResult({
        success: Math.random() > 0.1,
        userId: 'user_' + verificationId.substring(0, 8),
        verificationId: verificationId,
        assets: [
          { asset: 'Bitcoin', amount: 2.45, percentage: 35 },
          { asset: 'Ethereum', amount: 25.8, percentage: 40 },
          { asset: 'USDC', amount: 8500, percentage: 25 },
        ],
        totalValue: '$142,350.25',
        auditDate: '2024-01-15',
        nextAuditDate: '2024-04-15',
        rootHash: 'ca978112ca1bbdc16f7a08a27516ba5e4c614aca3a374760c4cc61f2a2f',
        merkleProofPath: [
          '0xabc123def456...',
          '0x789ghi012jkl...',
          '0xmnopqr345stu...',
        ],
        verificationTimestamp: new Date().toISOString(),
      });
      setIsLoading(false);
    }, 1500);
  };

  const trustIndicators = [
    { icon: Shield, label: 'VARA Regulated', status: 'verified' },
    { icon: Lock, label: 'Independent Audited', status: 'verified' },
    { icon: CheckCircle2, label: 'Cryptographically Verified', status: 'verified' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-simplyfi-navy/5 to-simplyfi-emerald/5">
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-simplyfi-navy mb-3">
            Verify Your Proof of Reserves
          </h1>
          <p className="text-lg text-simplyfi-text-muted">
            Independently verify your asset balances are included in our audited reserves
          </p>
        </div>

        {/* Verification Panel */}
        <Card className="p-8 border-2 border-simplyfi-emerald/30">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-simplyfi-navy mb-3">
                Enter Your Verification ID
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={verificationId}
                  onChange={(e) => setVerificationId(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleVerify()}
                  placeholder="e.g., 0x1a2b3c4d5e6f7g8h9i0j..."
                  className="flex-1 px-4 py-4 border-2 border-simplyfi-border-light rounded-xl text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy focus:border-transparent placeholder-simplyfi-text-muted"
                />
                <Button
                  variant="primary"
                  size="lg"
                  className="flex items-center gap-2 px-6"
                  onClick={handleVerify}
                  disabled={isLoading || !verificationId.trim()}
                >
                  <Search className="w-5 h-5" />
                  {isLoading ? 'Verifying...' : 'Verify'}
                </Button>
              </div>
              <p className="text-xs text-simplyfi-text-muted mt-2">
                Your verification ID was provided to you when you set up your account
              </p>
            </div>
          </div>
        </Card>

        {/* Trust Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {trustIndicators.map((indicator, idx) => {
            const Icon = indicator.icon;
            return (
              <Card key={idx} className="p-4 text-center">
                <div className="flex justify-center mb-3">
                  <Icon className="w-8 h-8 text-simplyfi-emerald" />
                </div>
                <p className="font-medium text-simplyfi-navy">{indicator.label}</p>
              </Card>
            );
          })}
        </div>

        {/* Results */}
        {verificationResult && (
          <div className="space-y-6 animate-fadeIn">
            {verificationResult.success ? (
              <>
                {/* Success Banner */}
                <Card className="p-8 bg-simplyfi-emerald/10 border-2 border-simplyfi-emerald">
                  <div className="flex items-start gap-4">
                    <CheckCircle2 className="w-12 h-12 text-simplyfi-emerald flex-shrink-0 mt-1" />
                    <div>
                      <h2 className="text-2xl font-bold text-simplyfi-emerald mb-2">
                        Verification Successful!
                      </h2>
                      <p className="text-simplyfi-emerald mb-3">
                        Your assets are included in our audited Proof of Reserves.
                      </p>
                      <p className="text-sm text-simplyfi-text-muted">
                        Verified on {new Date(verificationResult.verificationTimestamp).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </Card>

                {/* Asset Summary */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold text-simplyfi-navy mb-4">Your Assets</h3>
                  <div className="space-y-4">
                    {verificationResult.assets.map((asset, idx) => (
                      <div key={idx} className="pb-4 border-b border-simplyfi-border-light last:border-0">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-semibold text-simplyfi-navy">{asset.asset}</h4>
                          <span className="font-bold text-simplyfi-navy">{asset.amount.toLocaleString()}</span>
                        </div>
                        <div className="w-full bg-simplyfi-neutral-bg rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-simplyfi-navy to-simplyfi-emerald h-2 rounded-full"
                            style={{ width: `${asset.percentage}%` }}
                          />
                        </div>
                        <p className="text-xs text-simplyfi-text-muted mt-1">{asset.percentage}% of total</p>
                      </div>
                    ))}
                  </div>
                  <div className="mt-6 pt-4 border-t border-simplyfi-border-light">
                    <div className="flex items-center justify-between">
                      <span className="text-simplyfi-text-muted font-medium">Total Verified Value</span>
                      <span className="text-2xl font-bold text-simplyfi-navy">
                        {verificationResult.totalValue}
                      </span>
                    </div>
                  </div>
                </Card>

                {/* Merkle Proof Details */}
                <Card className="p-6 bg-simplyfi-navy/5 border-2 border-simplyfi-navy/20">
                  <h3 className="text-lg font-bold text-simplyfi-navy mb-4">Cryptographic Proof</h3>
                  <div className="space-y-4">
                    <div>
                      <p className="text-xs text-simplyfi-text-muted mb-2 font-semibold">Root Hash (Proof of Reserves)</p>
                      <div className="p-3 bg-white rounded-lg border border-simplyfi-border-light">
                        <p className="font-mono text-xs text-simplyfi-navy break-all">
                          {verificationResult.rootHash}
                        </p>
                      </div>
                    </div>

                    <div>
                      <p className="text-xs text-simplyfi-text-muted mb-2 font-semibold">
                        Your Merkle Proof Path ({verificationResult.merkleProofPath.length} steps)
                      </p>
                      <div className="space-y-2">
                        {verificationResult.merkleProofPath.map((hash, idx) => (
                          <div key={idx} className="flex items-center gap-2">
                            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-simplyfi-emerald/10 border border-simplyfi-emerald flex items-center justify-center">
                              <span className="text-xs font-bold text-simplyfi-emerald">{idx + 1}</span>
                            </div>
                            <div className="flex-1 p-2 bg-white rounded border border-simplyfi-border-light">
                              <p className="font-mono text-xs text-simplyfi-navy truncate">{hash}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="pt-4 border-t border-simplyfi-border-light">
                      <p className="text-xs text-simplyfi-text-muted mb-2">
                        This proof can be independently verified against the root hash published on-chain.
                      </p>
                    </div>
                  </div>
                </Card>

                {/* Audit Schedule */}
                <Card className="p-6">
                  <h3 className="text-lg font-bold text-simplyfi-navy mb-4">Audit Schedule</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-simplyfi-emerald/5 rounded-lg border border-simplyfi-emerald/20">
                      <span className="text-simplyfi-text-muted">Last Verification</span>
                      <span className="font-bold text-simplyfi-navy">
                        {new Date(verificationResult.auditDate).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-simplyfi-gold/5 rounded-lg border border-simplyfi-gold/20">
                      <span className="text-simplyfi-text-muted">Next Scheduled Audit</span>
                      <span className="font-bold text-simplyfi-navy">
                        {new Date(verificationResult.nextAuditDate).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </Card>
              </>
            ) : (
              <Card className="p-8 bg-simplyfi-red-warning/10 border-2 border-simplyfi-red-warning">
                <div className="flex items-start gap-4">
                  <AlertCircle className="w-12 h-12 text-simplyfi-red-warning flex-shrink-0 mt-1" />
                  <div>
                    <h2 className="text-2xl font-bold text-simplyfi-red-warning mb-2">
                      Verification Failed
                    </h2>
                    <p className="text-simplyfi-red-warning">
                      We could not find your verification ID in our records. Please check that you entered it correctly.
                    </p>
                  </div>
                </div>
              </Card>
            )}
          </div>
        )}

        {/* FAQ / Explainer */}
        {!verificationResult && (
          <Card className="p-6">
            <h3 className="text-lg font-bold text-simplyfi-navy mb-4">What is Proof of Reserves?</h3>
            <div className="space-y-3 text-simplyfi-text-muted">
              <p>
                Proof of Reserves is a cryptographic method that allows us to demonstrate that we hold sufficient customer assets to cover all customer liabilities, without revealing individual account details.
              </p>
              <p>
                Using Merkle tree technology, we can include your assets in a verifiable structure where you can confirm your balances are part of our total reserves.
              </p>
              <div className="mt-4 pt-4 border-t border-simplyfi-border-light">
                <h4 className="font-semibold text-simplyfi-navy mb-2">How it works:</h4>
                <ol className="list-decimal list-inside space-y-2 text-sm">
                  <li>Your assets are hashed and combined into a Merkle tree</li>
                  <li>The tree is independently audited by external auditors</li>
                  <li>The root hash is published on-chain for public verification</li>
                  <li>You can use your verification ID to confirm your inclusion</li>
                </ol>
              </div>
            </div>
          </Card>
        )}

        {/* Footer Info */}
        <div className="text-center text-sm text-simplyfi-text-muted border-t border-simplyfi-border-light pt-6">
          <p>
            SimplyFI is regulated by VARA and conducts quarterly independent audits.
            <br />
            Learn more about our security practices and audit reports.
          </p>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

export default CustomerVerification;
