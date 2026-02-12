import React from 'react';
import Card from '../../components/common/Card';
import DataTable from '../../components/common/DataTable';

const AdminAuditLogsPage = () => {
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'user', label: 'User' },
    { key: 'action', label: 'Action' },
    { key: 'resource', label: 'Resource' },
    { key: 'timestamp', label: 'Timestamp' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">Audit Logs</h1>
      <Card>
        <DataTable columns={columns} data={[]} emptyMessage="No audit logs found" />
      </Card>
    </div>
  );
};

export default AdminAuditLogsPage;
