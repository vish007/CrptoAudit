import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Upload, Plus, Trash2, CheckCircle2 } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import StatusBadge from '../../components/common/StatusBadge';

const OnboardingWizard = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    companyName: '',
    varaLicense: '',
    contactEmail: '',
    contactPhone: '',
    selectedAssets: [],
    wallets: [],
    custodians: [],
    customerLiabilities: [],
  });

  const [walletInput, setWalletInput] = useState({
    address: '',
    chain: 'ethereum',
  });

  const [custodianInput, setCustodianInput] = useState({
    name: '',
    apiKey: '',
  });

  // Available assets
  const availableAssets = [
    { id: 'btc', name: 'Bitcoin', symbol: 'BTC', tier: 'tier1' },
    { id: 'eth', name: 'Ethereum', symbol: 'ETH', tier: 'tier1' },
    { id: 'usdc', name: 'USDC', symbol: 'USDC', tier: 'tier1' },
    { id: 'usdt', name: 'Tether', symbol: 'USDT', tier: 'tier1' },
    { id: 'sol', name: 'Solana', symbol: 'SOL', tier: 'tier2' },
    { id: 'bnb', name: 'Binance Coin', symbol: 'BNB', tier: 'tier2' },
    { id: 'xrp', name: 'Ripple', symbol: 'XRP', tier: 'tier2' },
    { id: 'ada', name: 'Cardano', symbol: 'ADA', tier: 'tier2' },
    { id: 'dot', name: 'Polkadot', symbol: 'DOT', tier: 'tier3' },
    { id: 'matic', name: 'Polygon', symbol: 'MATIC', tier: 'tier3' },
  ];

  const steps = [
    { number: 1, label: 'Company Info' },
    { number: 2, label: 'Asset Config' },
    { number: 3, label: 'Wallet Import' },
    { number: 4, label: 'Custody Setup' },
    { number: 5, label: 'Liabilities' },
    { number: 6, label: 'Review' },
  ];

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleAddWallet = () => {
    if (!walletInput.address.trim()) return;
    setFormData((prev) => ({
      ...prev,
      wallets: [...prev.wallets, walletInput],
    }));
    setWalletInput({ address: '', chain: 'ethereum' });
  };

  const handleRemoveWallet = (index) => {
    setFormData((prev) => ({
      ...prev,
      wallets: prev.wallets.filter((_, i) => i !== index),
    }));
  };

  const handleAddCustodian = () => {
    if (!custodianInput.name.trim()) return;
    setFormData((prev) => ({
      ...prev,
      custodians: [...prev.custodians, custodianInput],
    }));
    setCustodianInput({ name: '', apiKey: '' });
  };

  const handleRemoveCustodian = (index) => {
    setFormData((prev) => ({
      ...prev,
      custodians: prev.custodians.filter((_, i) => i !== index),
    }));
  };

  const handleToggleAsset = (assetId) => {
    setFormData((prev) => ({
      ...prev,
      selectedAssets: prev.selectedAssets.includes(assetId)
        ? prev.selectedAssets.filter((id) => id !== assetId)
        : [...prev.selectedAssets, assetId],
    }));
  };

  const validateStep = () => {
    switch (currentStep) {
      case 1:
        return formData.companyName.trim() && formData.contactEmail.trim();
      case 2:
        return formData.selectedAssets.length > 0;
      case 3:
        return formData.wallets.length > 0;
      case 4:
        return formData.custodians.length > 0;
      case 5:
        return true; // Optional
      default:
        return true;
    }
  };

  const canProceed = validateStep();

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-simplyfi-navy mb-2">
                Company Name *
              </label>
              <input
                type="text"
                value={formData.companyName}
                onChange={(e) => handleInputChange('companyName', e.target.value)}
                placeholder="Enter company name..."
                className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-simplyfi-navy mb-2">
                VARA License Number
              </label>
              <input
                type="text"
                value={formData.varaLicense}
                onChange={(e) => handleInputChange('varaLicense', e.target.value)}
                placeholder="e.g., VARA-2024-001234"
                className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-simplyfi-navy mb-2">
                  Contact Email *
                </label>
                <input
                  type="email"
                  value={formData.contactEmail}
                  onChange={(e) => handleInputChange('contactEmail', e.target.value)}
                  placeholder="contact@company.com"
                  className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-simplyfi-navy mb-2">
                  Contact Phone
                </label>
                <input
                  type="tel"
                  value={formData.contactPhone}
                  onChange={(e) => handleInputChange('contactPhone', e.target.value)}
                  placeholder="+1 (555) 000-0000"
                  className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                />
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-simplyfi-navy mb-4">
                Select Assets to Audit ({formData.selectedAssets.length} selected)
              </h3>

              <div className="space-y-3">
                {['tier1', 'tier2', 'tier3'].map((tier) => (
                  <div key={tier}>
                    <p className="text-sm font-semibold text-simplyfi-text-muted mb-2">
                      {tier === 'tier1' && 'Tier 1 - Major Assets (Required)'}
                      {tier === 'tier2' && 'Tier 2 - Mid-Cap Assets'}
                      {tier === 'tier3' && 'Tier 3 - Alternative Assets'}
                    </p>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                      {availableAssets
                        .filter((a) => a.tier === tier)
                        .map((asset) => (
                          <button
                            key={asset.id}
                            onClick={() => handleToggleAsset(asset.id)}
                            className={`p-4 rounded-lg border-2 transition-all text-center ${
                              formData.selectedAssets.includes(asset.id)
                                ? 'border-simplyfi-navy bg-simplyfi-navy/5'
                                : 'border-simplyfi-border-light hover:border-simplyfi-navy'
                            }`}
                          >
                            <p className="font-bold text-simplyfi-navy">{asset.symbol}</p>
                            <p className="text-xs text-simplyfi-text-muted mt-1">{asset.name}</p>
                          </button>
                        ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="p-4 bg-simplyfi-neutral-bg rounded-lg border-2 border-dashed border-simplyfi-border-light text-center cursor-pointer hover:border-simplyfi-navy transition-colors">
              <Upload className="w-8 h-8 text-simplyfi-text-muted mx-auto mb-2" />
              <p className="font-medium text-simplyfi-navy mb-1">Upload Wallet CSV</p>
              <p className="text-sm text-simplyfi-text-muted">or enter manually below</p>
            </div>

            <div className="space-y-3">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={walletInput.address}
                  onChange={(e) => setWalletInput({ ...walletInput, address: e.target.value })}
                  placeholder="Enter wallet address..."
                  className="flex-1 px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                />
                <select
                  value={walletInput.chain}
                  onChange={(e) => setWalletInput({ ...walletInput, chain: e.target.value })}
                  className="px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                >
                  <option value="ethereum">Ethereum</option>
                  <option value="bitcoin">Bitcoin</option>
                  <option value="solana">Solana</option>
                  <option value="polygon">Polygon</option>
                </select>
                <Button variant="secondary" onClick={handleAddWallet}>
                  <Plus className="w-5 h-5" />
                </Button>
              </div>

              {formData.wallets.length > 0 && (
                <div className="space-y-2">
                  <p className="font-medium text-simplyfi-navy">{formData.wallets.length} wallets added</p>
                  {formData.wallets.map((wallet, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-simplyfi-neutral-bg rounded-lg">
                      <div className="text-sm">
                        <p className="font-mono text-simplyfi-navy truncate">{wallet.address}</p>
                        <p className="text-xs text-simplyfi-text-muted">{wallet.chain}</p>
                      </div>
                      <button
                        onClick={() => handleRemoveWallet(idx)}
                        className="p-2 hover:bg-simplyfi-red-warning/10 rounded-lg transition-colors"
                      >
                        <Trash2 className="w-4 h-4 text-simplyfi-red-warning" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="p-4 bg-simplyfi-gold/10 border border-simplyfi-gold/30 rounded-lg">
              <p className="text-sm text-simplyfi-navy">
                Configure custodian connections. API keys are encrypted and stored securely.
              </p>
            </div>

            <div className="space-y-3">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={custodianInput.name}
                  onChange={(e) => setCustodianInput({ ...custodianInput, name: e.target.value })}
                  placeholder="Custodian name (e.g., Coinbase Custody)..."
                  className="flex-1 px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                />
              </div>

              <div className="flex gap-2">
                <input
                  type="password"
                  value={custodianInput.apiKey}
                  onChange={(e) => setCustodianInput({ ...custodianInput, apiKey: e.target.value })}
                  placeholder="API Key (will be encrypted)"
                  className="flex-1 px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                />
                <Button variant="secondary" onClick={handleAddCustodian}>
                  <Plus className="w-5 h-5" />
                </Button>
              </div>

              {formData.custodians.length > 0 && (
                <div className="space-y-2">
                  <p className="font-medium text-simplyfi-navy">{formData.custodians.length} custodians connected</p>
                  {formData.custodians.map((custodian, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-simplyfi-neutral-bg rounded-lg">
                      <div>
                        <p className="font-medium text-simplyfi-navy">{custodian.name}</p>
                        <p className="text-xs text-simplyfi-text-muted">API Key: ••••••••{custodian.apiKey.slice(-4)}</p>
                      </div>
                      <button
                        onClick={() => handleRemoveCustodian(idx)}
                        className="p-2 hover:bg-simplyfi-red-warning/10 rounded-lg transition-colors"
                      >
                        <Trash2 className="w-4 h-4 text-simplyfi-red-warning" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div className="p-4 bg-simplyfi-neutral-bg rounded-lg border-2 border-dashed border-simplyfi-border-light text-center cursor-pointer hover:border-simplyfi-navy transition-colors">
              <Upload className="w-8 h-8 text-simplyfi-text-muted mx-auto mb-2" />
              <p className="font-medium text-simplyfi-navy mb-1">Upload Customer Liabilities CSV</p>
              <p className="text-sm text-simplyfi-text-muted">Format: UserID, Asset, Amount, Timestamp</p>
            </div>

            <p className="text-sm text-simplyfi-text-muted">
              Customer liability data is encrypted and processed securely. Only hashed identifiers are stored.
            </p>
          </div>
        );

      case 6:
        return (
          <div className="space-y-6">
            <div className="space-y-4">
              <div className="p-4 border border-simplyfi-emerald rounded-lg bg-simplyfi-emerald/5">
                <div className="flex items-center gap-2 mb-3">
                  <CheckCircle2 className="w-5 h-5 text-simplyfi-emerald" />
                  <h3 className="font-bold text-simplyfi-emerald">Ready to Submit</h3>
                </div>
                <div className="space-y-2 text-sm text-simplyfi-navy">
                  <p>Company: <strong>{formData.companyName}</strong></p>
                  <p>Assets: <strong>{formData.selectedAssets.length}</strong></p>
                  <p>Wallets: <strong>{formData.wallets.length}</strong></p>
                  <p>Custodians: <strong>{formData.custodians.length}</strong></p>
                </div>
              </div>

              <div className="p-4 bg-simplyfi-navy/5 rounded-lg border border-simplyfi-navy/20">
                <p className="text-sm text-simplyfi-navy">
                  By submitting, you agree to our Terms of Service and Data Processing Agreement. Your information will be processed according to our Privacy Policy.
                </p>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Header */}
      <Card className="p-6">
        <h1 className="text-3xl font-bold text-simplyfi-navy mb-2">VASP Onboarding</h1>
        <p className="text-simplyfi-text-muted">Complete setup for Proof of Reserves auditing (Step {currentStep} of {steps.length})</p>
      </Card>

      {/* Progress Stepper */}
      <Card className="p-6">
        <div className="flex items-center justify-between">
          {steps.map((step, idx) => (
            <React.Fragment key={step.number}>
              <div className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-bold mb-2 transition-all ${
                    currentStep >= step.number
                      ? 'bg-simplyfi-navy text-white'
                      : 'bg-simplyfi-border-light text-simplyfi-text-muted'
                  }`}
                >
                  {currentStep > step.number ? <CheckCircle2 className="w-5 h-5" /> : step.number}
                </div>
                <p className="text-xs text-center text-simplyfi-text-muted">{step.label}</p>
              </div>
              {idx < steps.length - 1 && (
                <div
                  className={`flex-1 h-1 mx-2 mb-6 ${
                    currentStep > step.number ? 'bg-simplyfi-navy' : 'bg-simplyfi-border-light'
                  }`}
                />
              )}
            </React.Fragment>
          ))}
        </div>
      </Card>

      {/* Step Content */}
      <Card className="p-8">{renderStep()}</Card>

      {/* Navigation */}
      <Card className="p-6">
        <div className="flex items-center justify-between">
          <Button
            variant="secondary"
            onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
            disabled={currentStep === 1}
            className="flex items-center gap-2"
          >
            <ChevronLeft className="w-5 h-5" />
            Back
          </Button>

          <div className="text-sm text-simplyfi-text-muted">
            Step {currentStep} of {steps.length}
          </div>

          {currentStep === steps.length ? (
            <Button
              variant="primary"
              onClick={() => alert('Onboarding completed!')}
              className="flex items-center gap-2"
            >
              <CheckCircle2 className="w-5 h-5" />
              Complete Setup
            </Button>
          ) : (
            <Button
              variant="primary"
              onClick={() => setCurrentStep(Math.min(steps.length, currentStep + 1))}
              disabled={!canProceed}
              className="flex items-center gap-2"
            >
              Next
              <ChevronRight className="w-5 h-5" />
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
};

export default OnboardingWizard;
