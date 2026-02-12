import React from 'react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';

const SecuritySettingsPage = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">Security Settings</h1>

      <Card padding="lg">
        <h2 className="text-xl font-bold text-simplyfi-text-dark mb-6">Change Password</h2>

        <form className="space-y-4 max-w-md">
          <div>
            <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
              Current Password
            </label>
            <input type="password" className="form-input" />
          </div>

          <div>
            <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
              New Password
            </label>
            <input type="password" className="form-input" />
          </div>

          <div>
            <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
              Confirm Password
            </label>
            <input type="password" className="form-input" />
          </div>

          <div className="flex gap-4 pt-4">
            <Button variant="primary">Update Password</Button>
            <Button variant="secondary">Cancel</Button>
          </div>
        </form>
      </Card>

      <Card padding="lg">
        <h2 className="text-xl font-bold text-simplyfi-text-dark mb-6">Two-Factor Authentication</h2>
        <p className="text-simplyfi-text-muted mb-4">
          Secure your account with two-factor authentication
        </p>
        <Button variant="accent">Enable 2FA</Button>
      </Card>
    </div>
  );
};

export default SecuritySettingsPage;
