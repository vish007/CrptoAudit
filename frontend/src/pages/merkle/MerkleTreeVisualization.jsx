import React, { useState, useRef, useEffect } from 'react';
import { ZoomIn, ZoomOut, Search, CheckCircle2, AlertCircle } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import StatusBadge from '../../components/common/StatusBadge';

const MerkleTreeVisualization = () => {
  const [zoom, setZoom] = useState(1);
  const [selectedLeaf, setSelectedLeaf] = useState(null);
  const [verificationInput, setVerificationInput] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const svgRef = useRef(null);

  // Generate mock Merkle tree data
  const generateMerkleTree = () => {
    const tree = {};
    const depth = 10; // 2^10 = 1024 leaves
    const leaves = Array.from({ length: 1000 }, (_, i) => ({
      id: i,
      hash: `leaf_${Math.random().toString(36).substring(7)}`,
      status: ['verified', 'pending', 'unverified'][Math.floor(Math.random() * 3)],
      proof: `0x${Math.random().toString(16).substring(2)}`,
      data: {
        userId: `user_${i}`,
        amount: (Math.random() * 100000).toFixed(2),
        timestamp: new Date(Date.now() - Math.random() * 86400000).toISOString(),
      },
    }));

    tree.leaves = leaves;
    tree.depth = depth;
    tree.totalLeaves = leaves.length;
    tree.rootHash = `0x${Math.random().toString(16).substring(2)}`;
    tree.generatedAt = new Date().toISOString();
    tree.hashAlgorithm = 'SHA-256';

    return tree;
  };

  const merkleTree = generateMerkleTree();

  // Generate SVG tree visualization
  const generateTreeSVG = () => {
    const width = 1400;
    const height = 600;
    const nodeRadius = 12;
    const levelHeight = height / 6; // 6 levels visible
    const nodeSpacing = 60;

    let svg = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg" style="border: 1px solid #e5e7eb; border-radius: 8px; background: white;">`;

    // Draw root node
    const rootX = width / 2;
    const rootY = 40;
    svg += `<circle cx="${rootX}" cy="${rootY}" r="${nodeRadius}" fill="#0a1628" stroke="#d4af37" stroke-width="2"/>`;
    svg += `<text x="${rootX}" y="${rootY + 25}" text-anchor="middle" font-size="10" fill="#6b7280" font-weight="bold">ROOT</text>`;

    // Draw lines and nodes for levels
    const getLevelNodes = (level) => {
      const maxNodesPerLevel = Math.min(Math.pow(2, level), 32); // Show max 32 nodes per level
      return maxNodesPerLevel;
    };

    let prevLevelX = [rootX];
    for (let level = 1; level <= 5; level++) {
      const nodesInLevel = getLevelNodes(level);
      const startX = (width - nodeSpacing * (nodesInLevel - 1)) / 2;
      const y = rootY + levelHeight * level;

      const levelXPositions = [];
      for (let i = 0; i < nodesInLevel; i++) {
        const x = startX + i * nodeSpacing;
        levelXPositions.push(x);

        // Draw lines from previous level
        if (level === 1) {
          svg += `<line x1="${prevLevelX[0]}" y1="${rootY + nodeRadius + 5}" x2="${x}" y2="${y - nodeRadius - 5}" stroke="#e5e7eb" stroke-width="1"/>`;
        } else if (i % 2 === 0 && i / 2 < prevLevelX.length) {
          const parentX = prevLevelX[Math.floor(i / 2)];
          svg += `<line x1="${parentX}" y1="${y - levelHeight + nodeRadius + 5}" x2="${x}" y2="${y - nodeRadius - 5}" stroke="#e5e7eb" stroke-width="1"/>`;
        }

        // Determine node color
        const statusRandom = Math.random();
        let nodeColor = '#d1d5db'; // gray - unverified
        if (statusRandom < 0.6) nodeColor = '#10b981'; // green - verified
        else if (statusRandom < 0.85) nodeColor = '#fbbf24'; // yellow - pending

        svg += `<circle cx="${x}" cy="${y}" r="${nodeRadius}" fill="${nodeColor}" stroke="#ffffff" stroke-width="1.5" data-level="${level}" data-index="${i}"/>`;
      }
      prevLevelX = levelXPositions;
    }

    // Draw leaf layer indicator
    svg += `<text x="20" y="${rootY + levelHeight * 6 - 10}" font-size="12" fill="#6b7280" font-weight="bold">1,000 Leaves (truncated view)</text>`;

    svg += `</svg>`;
    return svg;
  };

  const handleVerifyProof = () => {
    if (!verificationInput.trim()) {
      setVerificationResult(null);
      return;
    }

    // Simulate proof verification
    const matchingLeaf = merkleTree.leaves.find(
      (leaf) => leaf.hash.includes(verificationInput.substring(0, 8))
    );

    if (matchingLeaf) {
      setVerificationResult({
        success: true,
        leaf: matchingLeaf,
        verificationPath: Array.from({ length: merkleTree.depth }, (_, i) =>
          `0x${Math.random().toString(16).substring(2)}`
        ),
      });
      setSelectedLeaf(matchingLeaf);
    } else {
      setVerificationResult({
        success: false,
        message: 'Proof not found in tree. Please check the hash.',
      });
    }
  };

  const handleZoom = (direction) => {
    const newZoom = direction === 'in' ? zoom + 0.2 : Math.max(0.4, zoom - 0.2);
    setZoom(newZoom);
  };

  const stats = [
    { label: 'Total Leaves', value: merkleTree.totalLeaves.toLocaleString() },
    { label: 'Tree Depth', value: merkleTree.depth },
    { label: 'Hash Algorithm', value: merkleTree.hashAlgorithm },
    { label: 'Generated', value: new Date(merkleTree.generatedAt).toLocaleDateString() },
  ];

  const statusCounts = {
    verified: merkleTree.leaves.filter((l) => l.status === 'verified').length,
    pending: merkleTree.leaves.filter((l) => l.status === 'pending').length,
    unverified: merkleTree.leaves.filter((l) => l.status === 'unverified').length,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-simplyfi-navy mb-2">Merkle Tree Visualization</h1>
            <p className="text-simplyfi-text-muted">Interactive tree structure with {merkleTree.totalLeaves} customer leaves</p>
          </div>
          <StatusBadge status="success" size="lg">
            Generated
          </StatusBadge>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stats.map((stat, idx) => (
            <div key={idx} className="p-3 bg-simplyfi-neutral-bg rounded-lg">
              <p className="text-simplyfi-text-muted text-xs mb-1">{stat.label}</p>
              <p className="text-lg font-bold text-simplyfi-navy">{stat.value}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Root Hash Display */}
      <Card className="p-6 bg-simplyfi-navy/5 border-2 border-simplyfi-navy">
        <p className="text-simplyfi-text-muted text-sm mb-2 font-semibold">Root Hash (on-chain verification)</p>
        <p className="font-mono text-sm text-simplyfi-navy break-all font-bold">{merkleTree.rootHash}</p>
      </Card>

      {/* Tree Visualization */}
      <Card className="p-6">
        <div className="mb-4 flex justify-between items-center">
          <h2 className="text-xl font-bold text-simplyfi-navy">Tree Structure (5 visible levels)</h2>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              className="flex items-center gap-2"
              onClick={() => handleZoom('in')}
            >
              <ZoomIn className="w-4 h-4" />
              Zoom In
            </Button>
            <Button
              variant="secondary"
              size="sm"
              className="flex items-center gap-2"
              onClick={() => handleZoom('out')}
            >
              <ZoomOut className="w-4 h-4" />
              Zoom Out
            </Button>
          </div>
        </div>

        <div className="overflow-x-auto bg-white rounded-lg border border-simplyfi-border-light" style={{ transform: `scale(${zoom})`, transformOrigin: 'top left' }}>
          <div dangerouslySetInnerHTML={{ __html: generateTreeSVG() }} />
        </div>

        <div className="mt-4 p-4 bg-simplyfi-neutral-bg rounded-lg">
          <p className="text-sm text-simplyfi-text-muted">
            <strong>Green nodes:</strong> Verified leaves | <strong>Yellow nodes:</strong> Pending verification | <strong>Gray nodes:</strong> Unverified
          </p>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Status Summary */}
        <Card className="p-6">
          <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Verification Status</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-simplyfi-emerald/10 rounded-lg">
              <span className="text-simplyfi-emerald font-medium">Verified</span>
              <span className="text-lg font-bold text-simplyfi-emerald">{statusCounts.verified}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-simplyfi-gold/10 rounded-lg">
              <span className="text-simplyfi-gold font-medium">Pending</span>
              <span className="text-lg font-bold text-simplyfi-gold">{statusCounts.pending}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-100 rounded-lg">
              <span className="text-gray-600 font-medium">Unverified</span>
              <span className="text-lg font-bold text-gray-600">{statusCounts.unverified}</span>
            </div>
          </div>

          <div className="mt-6 p-4 bg-simplyfi-navy/5 rounded-lg border border-simplyfi-navy/20">
            <p className="text-sm text-simplyfi-navy font-semibold">
              {((statusCounts.verified / merkleTree.totalLeaves) * 100).toFixed(1)}% Complete
            </p>
            <div className="w-full bg-simplyfi-border-light rounded-full h-2 mt-2">
              <div
                className="bg-simplyfi-emerald h-2 rounded-full transition-all"
                style={{ width: `${(statusCounts.verified / merkleTree.totalLeaves) * 100}%` }}
              />
            </div>
          </div>
        </Card>

        {/* Verify My Proof Section */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6 border-2 border-simplyfi-gold/30 bg-simplyfi-gold/5">
            <h2 className="text-xl font-bold text-simplyfi-navy mb-4 flex items-center gap-2">
              <Search className="w-6 h-6" />
              Verify My Proof
            </h2>
            <p className="text-simplyfi-text-muted text-sm mb-4">
              Enter your leaf hash to verify your inclusion in the Merkle tree
            </p>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-simplyfi-navy mb-2">Leaf Hash</label>
                <input
                  type="text"
                  value={verificationInput}
                  onChange={(e) => setVerificationInput(e.target.value)}
                  placeholder="0x1a2b3c4d5e6f7g8h9i0j..."
                  className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                />
              </div>

              <Button
                variant="primary"
                className="w-full"
                onClick={handleVerifyProof}
              >
                Verify Proof
              </Button>

              {verificationResult && (
                <div
                  className={`p-4 rounded-lg border-2 ${
                    verificationResult.success
                      ? 'bg-simplyfi-emerald/10 border-simplyfi-emerald'
                      : 'bg-simplyfi-red-warning/10 border-simplyfi-red-warning'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    {verificationResult.success ? (
                      <CheckCircle2 className="w-6 h-6 text-simplyfi-emerald flex-shrink-0 mt-1" />
                    ) : (
                      <AlertCircle className="w-6 h-6 text-simplyfi-red-warning flex-shrink-0 mt-1" />
                    )}
                    <div>
                      {verificationResult.success ? (
                        <>
                          <h3 className="font-bold text-simplyfi-emerald mb-2">Proof Verified!</h3>
                          <div className="space-y-2 text-sm">
                            <p className="text-simplyfi-text-muted">
                              <strong>User:</strong> {verificationResult.leaf.data.userId}
                            </p>
                            <p className="text-simplyfi-text-muted">
                              <strong>Amount:</strong> ${verificationResult.leaf.data.amount}
                            </p>
                            <p className="text-simplyfi-text-muted">
                              <strong>Verification Path Depth:</strong> {verificationResult.verificationPath.length}
                            </p>
                          </div>
                        </>
                      ) : (
                        <>
                          <h3 className="font-bold text-simplyfi-red-warning mb-1">Verification Failed</h3>
                          <p className="text-sm text-simplyfi-red-warning">{verificationResult.message}</p>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </Card>

          {/* Selected Leaf Details */}
          {selectedLeaf && (
            <Card className="p-6 border-2 border-simplyfi-emerald/30">
              <h3 className="text-lg font-bold text-simplyfi-navy mb-4">Leaf Details</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Leaf Hash:</span>
                  <span className="font-mono text-sm text-simplyfi-navy">{selectedLeaf.hash}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">User ID:</span>
                  <span className="font-medium text-simplyfi-navy">{selectedLeaf.data.userId}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Amount:</span>
                  <span className="font-medium text-simplyfi-navy">${selectedLeaf.data.amount}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-simplyfi-text-muted">Status:</span>
                  <StatusBadge
                    status={selectedLeaf.status === 'verified' ? 'success' : selectedLeaf.status === 'pending' ? 'info' : 'pending'}
                    size="sm"
                  >
                    {selectedLeaf.status.charAt(0).toUpperCase() + selectedLeaf.status.slice(1)}
                  </StatusBadge>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default MerkleTreeVisualization;
