import React from 'react';
import Card from '../../components/common/Card';
import DataTable from '../../components/common/DataTable';

const MerkleTreesPage = () => {
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'root', label: 'Root Hash' },
    { key: 'leaves', label: 'Leaves' },
    { key: 'status', label: 'Status' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">Merkle Trees</h1>
      <Card>
        <DataTable columns={columns} data={[]} emptyMessage="No merkle trees found" />
      </Card>
    </div>
  );
};

export default MerkleTreesPage;
