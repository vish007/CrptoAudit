import React from 'react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';

const ProfileSettingsPage = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simplyfi-text-dark">Profile Settings</h1>

      <Card padding="lg">
        <h2 className="text-xl font-bold text-simplyfi-text-dark mb-6">Profile Information</h2>

        <form className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                First Name
              </label>
              <input type="text" className="form-input" />
            </div>

            <div>
              <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
                Last Name
              </label>
              <input type="text" className="form-input" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
              Email
            </label>
            <input type="email" className="form-input" disabled />
          </div>

          <div className="flex gap-4 pt-4">
            <Button variant="primary">Save Changes</Button>
            <Button variant="secondary">Cancel</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default ProfileSettingsPage;
