import React, { useState } from 'react';
import { ChevronDown, AlertCircle, CheckCircle2, AlertTriangle } from 'lucide-react';
import Card from '../common/Card';
import clsx from 'clsx';

const ComplianceScorecard = () => {
  const [expandedRequirement, setExpandedRequirement] = useState(null);

  // VARA compliance requirements
  const requirements = [
    {
      id: 1,
      name: 'Proof of Reserves',
      description: 'Regular verification of customer asset holdings',
      status: 'compliant',
      percentage: 100,
      details: 'All 153 assets audited and verified. Merkle tree generated and published on-chain.',
      recommendations: null,
    },
    {
      id: 2,
      name: 'Custody Controls',
      description: 'Secure storage and management of customer funds',
      status: 'compliant',
      percentage: 100,
      details: '5 custodians connected. Multi-sig wallets enforced. Cold storage for 85% of assets.',
      recommendations: null,
    },
    {
      id: 3,
      name: 'Reserve Ratio',
      description: 'Maintain minimum 100% reserve ratio',
      status: 'compliant',
      percentage: 100.2,
      details: 'Average reserve ratio: 100.2%. All assets above minimum requirement.',
      recommendations: null,
    },
    {
      id: 4,
      name: 'Operational Resilience',
      description: 'Disaster recovery and business continuity planning',
      status: 'partial',
      percentage: 75,
      details: 'DR plan in place. RTO: 2 hours, RPO: 15 minutes. Annual testing scheduled.',
      recommendations: 'Schedule quarterly DR testing instead of annual to align with VARA best practices.',
    },
    {
      id: 5,
      name: 'Audit Trail',
      description: 'Comprehensive logging of all transactions and access',
      status: 'compliant',
      percentage: 98,
      details: 'All transactions logged. Immutable audit logs maintained for 7 years.',
      recommendations: null,
    },
    {
      id: 6,
      name: 'Risk Management',
      description: 'Identification and mitigation of operational risks',
      status: 'partial',
      percentage: 82,
      details: 'Risk register maintained. Quarterly risk assessments completed.',
      recommendations: 'Implement real-time risk monitoring for DeFi positions and high-volatility assets.',
    },
    {
      id: 7,
      name: 'Customer Communication',
      description: 'Clear and timely disclosure to customers',
      status: 'compliant',
      percentage: 95,
      details: 'Quarterly reports issued. Merkle proofs provided to customers. Website transparency.',
      recommendations: null,
    },
    {
      id: 8,
      name: 'Data Protection',
      description: 'Customer data privacy and security',
      status: 'compliant',
      percentage: 100,
      details: 'AES-256 encryption. PII hashing. GDPR/CCPA compliant. Annual pen tests.',
      recommendations: null,
    },
  ];

  // Calculate overall compliance
  const overallScore = Math.round(
    requirements.reduce((sum, req) => sum + req.percentage, 0) / requirements.length
  );

  const compliantCount = requirements.filter((r) => r.status === 'compliant').length;
  const partialCount = requirements.filter((r) => r.status === 'partial').length;
  const nonCompliantCount = requirements.filter((r) => r.status === 'non_compliant').length;

  const getStatusIcon = (status) => {
    if (status === 'compliant') return <CheckCircle2 className="w-5 h-5 text-simplyfi-emerald" />;
    if (status === 'partial') return <AlertTriangle className="w-5 h-5 text-simplyfi-gold" />;
    return <AlertCircle className="w-5 h-5 text-simplyfi-red-warning" />;
  };

  const getStatusColor = (status) => {
    if (status === 'compliant') return 'text-simplyfi-emerald';
    if (status === 'partial') return 'text-simplyfi-gold';
    return 'text-simplyfi-red-warning';
  };

  const getProgressBarColor = (status) => {
    if (status === 'compliant') return 'bg-simplyfi-emerald';
    if (status === 'partial') return 'bg-simplyfi-gold';
    return 'bg-simplyfi-red-warning';
  };

  return (
    <Card className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-simplyfi-navy mb-2">VARA Compliance Scorecard</h2>
        <p className="text-simplyfi-text-muted">
          Current compliance status against Virtual Asset Reference Framework requirements
        </p>
      </div>

      {/* Overall Score */}
      <div className="mb-8 p-6 bg-gradient-to-br from-simplyfi-navy/5 to-simplyfi-emerald/5 rounded-xl border-2 border-simplyfi-navy/20">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-simplyfi-text-muted text-sm font-medium mb-2">Overall Compliance Score</p>
            <div className="flex items-baseline gap-2">
              <span className="text-5xl font-bold text-simplyfi-navy">{overallScore}%</span>
              <span className="text-lg text-simplyfi-emerald font-semibold">Compliant</span>
            </div>
          </div>

          {/* Score visualization */}
          <div className="relative w-24 h-24">
            <svg className="transform -rotate-90 w-24 h-24">
              <circle
                cx="48"
                cy="48"
                r="40"
                fill="none"
                stroke="#e5e7eb"
                strokeWidth="8"
              />
              <circle
                cx="48"
                cy="48"
                r="40"
                fill="none"
                stroke="#10b981"
                strokeWidth="8"
                strokeDasharray={`${(overallScore / 100) * 251} 251`}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl font-bold text-simplyfi-navy">{overallScore}</span>
            </div>
          </div>
        </div>

        {/* Status summary */}
        <div className="mt-6 grid grid-cols-3 gap-4 pt-6 border-t border-simplyfi-navy/20">
          <div className="text-center">
            <p className="text-2xl font-bold text-simplyfi-emerald">{compliantCount}</p>
            <p className="text-xs text-simplyfi-text-muted mt-1">Compliant</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-simplyfi-gold">{partialCount}</p>
            <p className="text-xs text-simplyfi-text-muted mt-1">Partial</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-simplyfi-red-warning">{nonCompliantCount}</p>
            <p className="text-xs text-simplyfi-text-muted mt-1">Non-Compliant</p>
          </div>
        </div>
      </div>

      {/* Requirements List */}
      <div className="space-y-3">
        {requirements.map((requirement) => (
          <div
            key={requirement.id}
            className="border border-simplyfi-border-light rounded-lg overflow-hidden hover:shadow-md transition-shadow"
          >
            <button
              onClick={() =>
                setExpandedRequirement(
                  expandedRequirement === requirement.id ? null : requirement.id
                )
              }
              className="w-full p-4 flex items-center justify-between hover:bg-simplyfi-neutral-bg transition-colors"
            >
              <div className="flex items-center gap-4 flex-1 text-left">
                {getStatusIcon(requirement.status)}
                <div className="flex-1">
                  <h3 className="font-semibold text-simplyfi-navy">{requirement.name}</h3>
                  <p className="text-sm text-simplyfi-text-muted">{requirement.description}</p>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className={clsx('font-bold', getStatusColor(requirement.status))}>
                    {requirement.percentage}%
                  </p>
                  <p className="text-xs text-simplyfi-text-muted capitalize">
                    {requirement.status.replace('_', ' ')}
                  </p>
                </div>
                <ChevronDown
                  className={clsx(
                    'w-5 h-5 text-simplyfi-text-muted transition-transform',
                    expandedRequirement === requirement.id && 'rotate-180'
                  )}
                />
              </div>
            </button>

            {/* Expanded Details */}
            {expandedRequirement === requirement.id && (
              <div className="p-4 border-t border-simplyfi-border-light bg-simplyfi-neutral-bg space-y-4">
                {/* Progress bar */}
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-simplyfi-navy">Compliance Progress</span>
                    <span className="text-sm font-bold text-simplyfi-navy">{requirement.percentage}%</span>
                  </div>
                  <div className="w-full bg-white rounded-full h-3 border border-simplyfi-border-light">
                    <div
                      className={clsx('h-3 rounded-full transition-all', getProgressBarColor(requirement.status))}
                      style={{ width: `${requirement.percentage}%` }}
                    />
                  </div>
                </div>

                {/* Details */}
                <div>
                  <p className="text-sm font-semibold text-simplyfi-navy mb-2">Details</p>
                  <p className="text-sm text-simplyfi-text-muted">{requirement.details}</p>
                </div>

                {/* Recommendations */}
                {requirement.recommendations && (
                  <div className="p-3 bg-simplyfi-gold/10 border border-simplyfi-gold/30 rounded-lg">
                    <div className="flex gap-2">
                      <AlertTriangle className="w-5 h-5 text-simplyfi-gold flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm font-semibold text-simplyfi-gold mb-1">Recommendation</p>
                        <p className="text-sm text-simplyfi-gold">
                          {requirement.recommendations}
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Action buttons */}
                <div className="flex gap-2 pt-2">
                  <button className="flex-1 px-3 py-2 text-sm font-medium text-simplyfi-navy bg-white border border-simplyfi-border-light rounded-lg hover:bg-simplyfi-neutral-bg transition-colors">
                    View Details
                  </button>
                  {requirement.recommendations && (
                    <button className="flex-1 px-3 py-2 text-sm font-medium text-simplyfi-emerald bg-simplyfi-emerald/10 border border-simplyfi-emerald/30 rounded-lg hover:bg-simplyfi-emerald/20 transition-colors">
                      Remediate
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Last Audit */}
      <div className="mt-6 pt-6 border-t border-simplyfi-border-light text-center text-sm text-simplyfi-text-muted">
        <p>Last compliance audit: January 15, 2024 • Next audit: April 15, 2024</p>
      </div>
    </Card>
  );
};

export default ComplianceScorecard;
