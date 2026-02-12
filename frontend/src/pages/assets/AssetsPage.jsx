import React from 'react';
import Card from '../../components/common/Card';
import DataTable from '../../components/common/DataTable';

const AssetsPage = () => {
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    { key: 'type', label: 'Type' },
    { key: 'quantity', label: 'Quantity' },
    { key: 'value', label: 'Value' },
    { key: 'status', label: 'Status' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">Assets</h1>
      <Card>
        <DataTable columns={columns} data={[]} emptyMessage="No assets found" />
      </Card>
    </div>
  );
};

export default AssetsPage;
