import React from 'react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';

const CreateEngagementPage = () => {
  return (
    <div className="space-y-6">
      <Card padding="lg">
        <h2 className="text-2xl font-bold text-simplyfi-text-dark mb-6">Create New Engagement</h2>

        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
              Engagement Name
            </label>
            <input type="text" placeholder="Enter engagement name" className="form-input" />
          </div>

          <div>
            <label className="block text-sm font-medium text-simplyfi-text-dark mb-2">
              Type
            </label>
            <select className="form-input">
              <option>Audit</option>
              <option>Review</option>
              <option>Assessment</option>
            </select>
          </div>

          <div className="flex gap-4 pt-4">
            <Button variant="primary">Create</Button>
            <Button variant="secondary">Cancel</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default CreateEngagementPage;
