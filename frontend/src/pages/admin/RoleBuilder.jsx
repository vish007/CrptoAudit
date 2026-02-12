import React, { useState } from 'react';
import { Plus, Trash2, Save, Eye, Edit2, Lock, Share2 } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import StatusBadge from '../../components/common/StatusBadge';

const RoleBuilder = () => {
  const [roleName, setRoleName] = useState('');
  const [roleDescription, setRoleDescription] = useState('');
  const [selectedRole, setSelectedRole] = useState(null);
  const [showFieldRestrictions, setShowFieldRestrictions] = useState(false);

  const resources = [
    'Engagements',
    'Assets',
    'Wallets',
    'Reserves',
    'Merkle Trees',
    'Reports',
    'Users',
    'Tenants',
    'Audit Logs',
    'AI',
    'Blockchain',
    'DeFi',
  ];

  const actions = ['View', 'Create', 'Edit', 'Delete', 'Export'];

  const [permissions, setPermissions] = useState(() => {
    const initialPermissions = {};
    resources.forEach((resource) => {
      initialPermissions[resource] = {};
      actions.forEach((action) => {
        initialPermissions[resource][action] = false;
      });
    });
    return initialPermissions;
  });

  const existingRoles = [
    {
      id: 1,
      name: 'Auditor',
      description: 'Full audit access',
      permissionCount: 42,
      userCount: 5,
    },
    {
      id: 2,
      name: 'Client Manager',
      description: 'Manage client engagements',
      permissionCount: 24,
      userCount: 3,
    },
    {
      id: 3,
      name: 'Viewer',
      description: 'Read-only access',
      permissionCount: 12,
      userCount: 8,
    },
    {
      id: 4,
      name: 'Admin',
      description: 'Full system access',
      permissionCount: 60,
      userCount: 2,
    },
  ];

  const fieldRestrictions = {
    Wallets: [
      { field: 'Private Keys', role: 'Admin', status: 'restricted' },
      { field: 'Seed Phrases', role: 'Admin', status: 'restricted' },
      { field: 'API Keys', role: 'Auditor', status: 'restricted' },
      { field: 'Balances', role: 'All', status: 'visible' },
      { field: 'Addresses', role: 'All', status: 'visible' },
    ],
    Reports: [
      { field: 'Client Data', role: 'Assigned Auditor', status: 'restricted' },
      { field: 'Recommendations', role: 'All', status: 'visible' },
      { field: 'Financial Data', role: 'Auditor+', status: 'restricted' },
    ],
    Users: [
      { field: 'Email', role: 'All', status: 'visible' },
      { field: 'Password Hash', role: 'Admin', status: 'restricted' },
      { field: 'MFA Status', role: 'Admin', status: 'visible' },
      { field: 'Permissions', role: 'Admin', status: 'restricted' },
    ],
  };

  const togglePermission = (resource, action) => {
    setPermissions((prev) => ({
      ...prev,
      [resource]: {
        ...prev[resource],
        [action]: !prev[resource][action],
      },
    }));
  };

  const toggleAllPermissions = (resource) => {
    const allChecked = actions.every((action) => permissions[resource][action]);
    setPermissions((prev) => ({
      ...prev,
      [resource]: actions.reduce((acc, action) => {
        acc[action] = !allChecked;
        return acc;
      }, {}),
    }));
  };

  const getPermissionCount = () => {
    return Object.values(permissions).reduce((total, resourcePerms) => {
      return total + Object.values(resourcePerms).filter(Boolean).length;
    }, 0);
  };

  const handleSaveRole = () => {
    if (!roleName.trim()) {
      alert('Please enter a role name');
      return;
    }
    alert(`Role "${roleName}" saved successfully!`);
    setRoleName('');
    setRoleDescription('');
    resources.forEach((resource) => {
      actions.forEach((action) => {
        setPermissions((prev) => ({
          ...prev,
          [resource]: { ...prev[resource], [action]: false },
        }));
      });
    });
  };

  const getResourcePermissionCount = (resource) => {
    return Object.values(permissions[resource]).filter(Boolean).length;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="p-6">
        <h1 className="text-3xl font-bold text-simplyfi-navy mb-2">Role Builder</h1>
        <p className="text-simplyfi-text-muted">Create and manage custom roles with granular RBAC permissions</p>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Form Panel */}
        <div className="lg:col-span-3 space-y-6">
          {/* Basic Info */}
          <Card className="p-6">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Role Information</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-simplyfi-navy mb-2">
                  Role Name
                </label>
                <input
                  type="text"
                  value={roleName}
                  onChange={(e) => setRoleName(e.target.value)}
                  placeholder="e.g., Senior Auditor, Risk Manager"
                  className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-simplyfi-navy mb-2">
                  Description
                </label>
                <textarea
                  value={roleDescription}
                  onChange={(e) => setRoleDescription(e.target.value)}
                  placeholder="Brief description of this role's purpose and responsibilities..."
                  rows={3}
                  className="w-full px-4 py-3 border border-simplyfi-border-light rounded-lg text-simplyfi-navy focus:outline-none focus:ring-2 focus:ring-simplyfi-navy resize-none"
                />
              </div>
            </div>
          </Card>

          {/* Permission Matrix */}
          <Card className="p-6">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Permission Matrix</h2>
            <p className="text-sm text-simplyfi-text-muted mb-4">
              Select which resources and actions this role can access
            </p>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-simplyfi-border-light">
                    <th className="text-left py-3 px-4 font-semibold text-simplyfi-text-muted text-sm">
                      Resource
                    </th>
                    {actions.map((action) => (
                      <th
                        key={action}
                        className="text-center py-3 px-3 font-semibold text-simplyfi-text-muted text-sm"
                      >
                        {action}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {resources.map((resource) => (
                    <tr
                      key={resource}
                      className="border-b border-simplyfi-border-light hover:bg-simplyfi-neutral-bg"
                    >
                      <td className="py-4 px-4">
                        <div>
                          <p className="font-semibold text-simplyfi-navy">{resource}</p>
                          <p className="text-xs text-simplyfi-text-muted">
                            {getResourcePermissionCount(resource)}/{actions.length}
                          </p>
                        </div>
                      </td>
                      {actions.map((action) => (
                        <td key={`${resource}-${action}`} className="text-center py-4 px-3">
                          <input
                            type="checkbox"
                            checked={permissions[resource][action]}
                            onChange={() => togglePermission(resource, action)}
                            className="w-5 h-5 rounded border-simplyfi-border-light text-simplyfi-navy cursor-pointer"
                          />
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-4 p-4 bg-simplyfi-navy/5 rounded-lg">
              <p className="text-sm text-simplyfi-navy font-semibold">
                Total Permissions: {getPermissionCount()} / {resources.length * actions.length}
              </p>
            </div>
          </Card>

          {/* Field-Level Restrictions */}
          <Card className="p-6">
            <button
              onClick={() => setShowFieldRestrictions(!showFieldRestrictions)}
              className="w-full flex items-center justify-between mb-4 pb-4 border-b border-simplyfi-border-light hover:text-simplyfi-navy transition-colors"
            >
              <h2 className="text-lg font-bold text-simplyfi-navy">Field-Level Restrictions</h2>
              <span className={`transform transition-transform ${showFieldRestrictions ? 'rotate-180' : ''}`}>
                ▼
              </span>
            </button>

            {showFieldRestrictions && (
              <div className="space-y-6">
                {Object.entries(fieldRestrictions).map(([resource, fields]) => (
                  <div key={resource}>
                    <h3 className="font-semibold text-simplyfi-navy mb-3">{resource}</h3>
                    <div className="space-y-2">
                      {fields.map((field, idx) => (
                        <div
                          key={idx}
                          className="flex items-center justify-between p-3 bg-simplyfi-neutral-bg rounded-lg"
                        >
                          <div className="flex items-center gap-3">
                            {field.status === 'restricted' ? (
                              <Lock className="w-4 h-4 text-simplyfi-red-warning" />
                            ) : (
                              <Eye className="w-4 h-4 text-simplyfi-emerald" />
                            )}
                            <div>
                              <p className="font-medium text-simplyfi-navy">{field.field}</p>
                              <p className="text-xs text-simplyfi-text-muted">Allowed for: {field.role}</p>
                            </div>
                          </div>
                          <StatusBadge
                            status={field.status === 'restricted' ? 'error' : 'success'}
                            size="sm"
                          >
                            {field.status === 'restricted' ? 'Restricted' : 'Visible'}
                          </StatusBadge>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Save Button */}
          <Button
            variant="primary"
            size="lg"
            className="w-full flex items-center justify-center gap-2"
            onClick={handleSaveRole}
          >
            <Save className="w-5 h-5" />
            Save Role
          </Button>
        </div>

        {/* Summary Panel */}
        <div>
          <Card className="p-6 sticky top-6">
            <h2 className="text-lg font-bold text-simplyfi-navy mb-4">Role Summary</h2>

            {roleName ? (
              <div className="space-y-4">
                <div className="p-4 bg-simplyfi-navy/5 rounded-lg border border-simplyfi-navy/20">
                  <p className="text-xs text-simplyfi-text-muted mb-1">Name</p>
                  <p className="font-bold text-simplyfi-navy">{roleName}</p>
                </div>

                {roleDescription && (
                  <div className="p-4 bg-simplyfi-neutral-bg rounded-lg">
                    <p className="text-xs text-simplyfi-text-muted mb-1">Description</p>
                    <p className="text-sm text-simplyfi-navy">{roleDescription}</p>
                  </div>
                )}

                <div className="p-4 bg-simplyfi-emerald/10 rounded-lg border border-simplyfi-emerald/30">
                  <p className="text-xs text-simplyfi-text-muted mb-1">Permissions</p>
                  <p className="text-2xl font-bold text-simplyfi-emerald">{getPermissionCount()}</p>
                  <p className="text-xs text-simplyfi-text-muted mt-1">
                    {resources.length * actions.length} total available
                  </p>
                </div>

                <div className="pt-4 border-t border-simplyfi-border-light">
                  <h3 className="text-sm font-bold text-simplyfi-navy mb-3">Resources Included</h3>
                  <div className="space-y-2">
                    {resources.map((resource) => {
                      const count = getResourcePermissionCount(resource);
                      return (
                        count > 0 && (
                          <div key={resource} className="flex items-center justify-between text-sm">
                            <span className="text-simplyfi-text-muted">{resource}</span>
                            <span className="font-semibold text-simplyfi-navy">
                              {count}/{actions.length}
                            </span>
                          </div>
                        )
                      );
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-6">
                <Lock className="w-12 h-12 text-simplyfi-border-light mx-auto mb-3" />
                <p className="text-simplyfi-text-muted text-sm">
                  Enter role details to preview the configuration
                </p>
              </div>
            )}
          </Card>
        </div>
      </div>

      {/* Existing Roles */}
      <Card className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-simplyfi-navy">Existing Roles</h2>
          <span className="text-sm text-simplyfi-text-muted">{existingRoles.length} roles</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {existingRoles.map((role) => (
            <div
              key={role.id}
              className="p-4 border border-simplyfi-border-light rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-simplyfi-navy">{role.name}</h3>
                  <p className="text-sm text-simplyfi-text-muted">{role.description}</p>
                </div>
                <div className="flex gap-2">
                  <button className="p-2 hover:bg-simplyfi-neutral-bg rounded-lg transition-colors">
                    <Edit2 className="w-4 h-4 text-simplyfi-navy" />
                  </button>
                  <button className="p-2 hover:bg-simplyfi-neutral-bg rounded-lg transition-colors">
                    <Trash2 className="w-4 h-4 text-simplyfi-red-warning" />
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-simplyfi-border-light">
                <div className="space-y-1">
                  <div className="text-xs text-simplyfi-text-muted">
                    <p>{role.permissionCount} permissions</p>
                  </div>
                  <div className="text-xs text-simplyfi-text-muted">
                    <p>{role.userCount} users assigned</p>
                  </div>
                </div>
                <button className="px-3 py-1 bg-simplyfi-navy/10 text-simplyfi-navy rounded font-medium text-xs hover:bg-simplyfi-navy/20 transition-colors">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default RoleBuilder;
