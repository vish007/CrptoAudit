import React from 'react';
import Card from '../../components/common/Card';

const AdminSettingsPage = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">System Settings</h1>
      <Card padding="lg">
        <div className="text-center text-simplyfi-text-muted">
          <p>System settings page content goes here</p>
        </div>
      </Card>
    </div>
  );
};

export default AdminSettingsPage;
