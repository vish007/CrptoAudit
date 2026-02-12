import React, { useState } from 'react';
import { Download, FileText, Plus, Trash2, CheckCircle2 } from 'lucide-react';
import Card from '../../components/common/Card';
import StatusBadge from '../../components/common/StatusBadge';
import Button from '../../components/common/Button';

const ReportBuilder = () => {
  const [reportType, setReportType] = useState('por_aup');
  const [selectedEngagement, setSelectedEngagement] = useState('');
  const [useAI, setUseAI] = useState(false);
  const [selectedSections, setSelectedSections] = useState({
    executive_summary: true,
    scope: true,
    procedures: true,
    findings: true,
    recommendations: true,
    appendix: false,
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [generateProgress, setGenerateProgress] = useState(0);
  const [showPreview, setShowPreview] = useState(false);

  const reportTypes = [
    {
      id: 'por_aup',
      name: 'PoR AUP Report',
      description: 'Attestation of Proof of Reserves with Agreed-Upon Procedures',
      sections: 5,
    },
    {
      id: 'assurance',
      name: 'Assurance Report',
      description: 'SOC 2 Type II Compliance Report',
      sections: 6,
    },
    {
      id: 'management_letter',
      name: 'Management Letter',
      description: 'Internal control observations and recommendations',
      sections: 4,
    },
    {
      id: 'customer_summary',
      name: 'Customer Summary',
      description: 'Simplified proof of reserves for customers',
      sections: 3,
    },
    {
      id: 'vara_quarterly',
      name: 'VARA Quarterly Report',
      description: 'Virtual Asset Reference Framework quarterly compliance',
      sections: 7,
    },
  ];

  const sections = {
    executive_summary: 'Executive Summary',
    scope: 'Scope & Objectives',
    procedures: 'Audit Procedures',
    findings: 'Findings & Results',
    recommendations: 'Recommendations',
    appendix: 'Technical Appendix',
    compliance: 'Compliance Framework',
    defi_analysis: 'DeFi Risk Analysis',
  };

  const engagements = [
    { id: 1, name: 'Crypto Exchange Inc. - Q1 2024' },
    { id: 2, name: 'Digital Assets Fund - Annual 2024' },
    { id: 3, name: 'Decentralized Exchange Ltd - Q4 2023' },
    { id: 4, name: 'Custody Platform Corp - Annual 2024' },
  ];

  const previousReports = [
    {
      id: 1,
      name: 'PoR AUP Report - Q4 2023',
      type: 'PoR AUP',
      engagement: 'Crypto Exchange Inc.',
      date: '2024-01-10',
      size: '2.4 MB',
      status: 'completed',
    },
    {
      id: 2,
      name: 'Management Letter - 2023',
      type: 'Management Letter',
      engagement: 'Digital Assets Fund',
      date: '2024-01-05',
      size: '1.8 MB',
      status: 'completed',
    },
    {
      id: 3,
      name: 'Assurance Report - Annual',
      type: 'Assurance',
      engagement: 'Decentralized Exchange Ltd',
      date: '2023-12-28',
      size: '3.1 MB',
      status: 'completed',
    },
    {
      id: 4,
      name: 'PoR Summary - Draft',
      type: 'Customer Summary',
      engagement: 'Custody Platform Corp',
      date: '2023-12-15',
      size: '0.8 MB',
      status: 'draft',
    },
  ];

  const handleGenerateReport = () => {
    if (!selectedEngagement) {
      alert('Please select an engagement');
      return;
    }

    setIsGenerating(true);
    setGenerateProgress(0);

    // Simulate report generation progress
    const interval = setInterval(() => {
      setGenerateProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsGenerating(false);
          return 100;
        }
        return prev + Math.random() * 25;
      });
    }, 800);
  };

  const currentReportType = reportTypes.find((rt) => rt.id === reportType);
  const availableSections = Object.entries(sections).slice(0, currentReportType?.sections);

  const toggleSection = (sectionKey) => {
    setSelectedSections((prev) => ({
      ...prev,
      [sectionKey]: !prev[sectionKey],
    }));
  };

  const selectedCount = Object.values(selectedSections).filter(Boolean).length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="p-6">
        <h1 className="text-3xl font-bold text-simplyfi-navy mb-2">Report Builder</h1>
        <p className="text-simplyfi-text-muted">
          Create custom audit reports with AI-assisted narrative generation
        </p>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration Panel */}
        <div className="lg:col-span-2 space-y-6">
          {/* Report Type Selection */}
          <Card className="p-6">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">1. Select Report Type</h2>
            <div className="grid grid-cols-1 gap-3">
              {reportTypes.map((type) => (
                <button
                  key={type.id}
                  onClick={() => setReportType(type.id)}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    reportType === type.id
                      ? 'border-simplyfi-navy bg-simplyfi-navy/5'
                      : 'border-simplyfi-border-light hover:border-simplyfi-navy'
                  }`}
                >
                  <h3 className="font-semibold text-simplyfi-navy mb-1">{type.name}</h3>
                  <p className="text-sm text-simplyfi-text-muted mb-2">{type.description}</p>
                  <span className="text-xs text-simplyfi-gold font-medium">
                    {type.sections} sections included
                  </span>
                </button>
              ))}
            </div>
          </Card>

          {/* Engagement Selection */}
          <Card className="p-6">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">2. Select Engagement</h2>
            <select
              value={selectedEngagement}
              onChange={(e) => setSelectedEngagement(e.target.value)}
              className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
            >
              <option value="">Choose an engagement...</option>
              {engagements.map((eng) => (
                <option key={eng.id} value={eng.id}>
                  {eng.name}
                </option>
              ))}
            </select>
          </Card>

          {/* Section Checklist */}
          <Card className="p-6">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">
              3. Include Report Sections
            </h2>
            <p className="text-sm text-simplyfi-text-muted mb-4">
              Selected: {selectedCount} / {availableSections.length}
            </p>
            <div className="space-y-3">
              {availableSections.map(([key, label]) => (
                <label key={key} className="flex items-center gap-3 p-3 hover:bg-simplyfi-neutral-bg rounded-lg cursor-pointer transition-colors">
                  <input
                    type="checkbox"
                    checked={selectedSections[key] || false}
                    onChange={() => toggleSection(key)}
                    className="w-4 h-4 rounded border-simplyfi-border-light text-simplyfi-navy cursor-pointer"
                  />
                  <span className="font-medium text-simplyfi-navy">{label}</span>
                </label>
              ))}
            </div>
          </Card>

          {/* AI Narrative Toggle */}
          <Card className="p-6 bg-simplyfi-gold/5 border-simplyfi-gold/30 border-2">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">4. AI-Assisted Narrative</h2>
            <label className="flex items-start gap-4 cursor-pointer">
              <div className="flex items-center mt-1">
                <input
                  type="checkbox"
                  checked={useAI}
                  onChange={(e) => setUseAI(e.target.checked)}
                  className="w-5 h-5 rounded border-simplyfi-border-light text-simplyfi-navy cursor-pointer"
                />
              </div>
              <div>
                <p className="font-semibold text-simplyfi-navy">Enable AI-Assisted Narratives</p>
                <p className="text-sm text-simplyfi-text-muted mt-1">
                  Use Claude AI to generate professional findings and recommendations narratives
                  based on audit data and procedures
                </p>
              </div>
            </label>
          </Card>

          {/* Generate Button */}
          <Button
            variant="primary"
            size="lg"
            className="w-full flex items-center justify-center gap-2"
            onClick={handleGenerateReport}
            disabled={isGenerating || !selectedEngagement}
          >
            <FileText className="w-5 h-5" />
            {isGenerating ? 'Generating Report...' : 'Generate Report'}
          </Button>

          {/* Progress Indicator */}
          {isGenerating && (
            <Card className="p-6">
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-simplyfi-navy">
                    Processing...
                  </span>
                  <span className="text-sm font-bold text-simplyfi-navy">
                    {Math.round(generateProgress)}%
                  </span>
                </div>
                <div className="w-full bg-simplyfi-neutral-bg rounded-full h-3">
                  <div
                    className="bg-gradient-to-r from-simplyfi-navy to-simplyfi-gold h-3 rounded-full transition-all"
                    style={{ width: `${generateProgress}%` }}
                  />
                </div>
              </div>
            </Card>
          )}
        </div>

        {/* Preview Panel */}
        <div>
          <Card className="p-6 sticky top-6">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Report Preview</h2>

            {/* Report Details */}
            <div className="space-y-4 mb-6 pb-6 border-b border-simplyfi-border-light">
              <div>
                <p className="text-xs text-simplyfi-text-muted mb-1">Report Type</p>
                <p className="font-semibold text-simplyfi-navy">{currentReportType?.name}</p>
              </div>

              <div>
                <p className="text-xs text-simplyfi-text-muted mb-1">Engagement</p>
                <p className="font-semibold text-simplyfi-navy">
                  {engagements.find((e) => e.id === +selectedEngagement)?.name || 'Not selected'}
                </p>
              </div>

              <div>
                <p className="text-xs text-simplyfi-text-muted mb-1">Sections</p>
                <p className="font-semibold text-simplyfi-navy">{selectedCount} included</p>
              </div>

              <div>
                <p className="text-xs text-simplyfi-text-muted mb-1">AI Narrative</p>
                <StatusBadge status={useAI ? 'success' : 'pending'} size="sm">
                  {useAI ? 'Enabled' : 'Disabled'}
                </StatusBadge>
              </div>
            </div>

            {/* Report Status */}
            <div>
              <p className="text-xs text-simplyfi-text-muted mb-3 font-semibold">Estimated Size</p>
              <div className="p-3 bg-simplyfi-neutral-bg rounded-lg text-center">
                <p className="text-2xl font-bold text-simplyfi-navy">
                  {(2.5 + selectedCount * 0.3 + (useAI ? 0.5 : 0)).toFixed(1)} MB
                </p>
                <p className="text-xs text-simplyfi-text-muted mt-1">
                  {selectedCount * 8 + (useAI ? 12 : 0)} pages
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Previously Generated Reports */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-simplyfi-navy">Previously Generated Reports</h2>
          <span className="text-sm text-simplyfi-text-muted">{previousReports.length} reports</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {previousReports.map((report) => (
            <div
              key={report.id}
              className="p-4 border border-simplyfi-border-light rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-start gap-3 flex-1">
                  <FileText className="w-6 h-6 text-simplyfi-gold flex-shrink-0 mt-1" />
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-simplyfi-navy truncate">{report.name}</h3>
                    <p className="text-xs text-simplyfi-text-muted mt-1">{report.engagement}</p>
                  </div>
                </div>
                <StatusBadge
                  status={report.status === 'completed' ? 'success' : 'pending'}
                  size="sm"
                >
                  {report.status === 'completed' ? 'Complete' : 'Draft'}
                </StatusBadge>
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-simplyfi-border-light">
                <div className="text-xs text-simplyfi-text-muted">
                  <p>{report.type}</p>
                  <p className="mt-1">
                    {new Date(report.date).toLocaleDateString()} • {report.size}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button className="p-2 hover:bg-simplyfi-neutral-bg rounded-lg transition-colors">
                    <Download className="w-4 h-4 text-simplyfi-navy" />
                  </button>
                  <button className="p-2 hover:bg-simplyfi-neutral-bg rounded-lg transition-colors">
                    <Trash2 className="w-4 h-4 text-simplyfi-red-warning" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default ReportBuilder;
