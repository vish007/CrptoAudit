import React from 'react';
import Card from '../../components/common/Card';
import DataTable from '../../components/common/DataTable';

const ReportsPage = () => {
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'title', label: 'Title' },
    { key: 'type', label: 'Type' },
    { key: 'status', label: 'Status' },
    { key: 'createdAt', label: 'Created' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">Reports</h1>
      <Card>
        <DataTable columns={columns} data={[]} emptyMessage="No reports found" />
      </Card>
    </div>
  );
};

export default ReportsPage;
