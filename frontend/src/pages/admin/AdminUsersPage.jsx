import React from 'react';
import Card from '../../components/common/Card';
import DataTable from '../../components/common/DataTable';

const AdminUsersPage = () => {
  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'email', label: 'Email' },
    { key: 'role', label: 'Role' },
    { key: 'status', label: 'Status' },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">User Management</h1>
      <Card>
        <DataTable columns={columns} data={[]} emptyMessage="No users found" />
      </Card>
    </div>
  );
};

export default AdminUsersPage;
