import React from 'react';
import usePermissions from '../../hooks/usePermissions';

const PermissionGate = ({
  children,
  permission = null,
  permissions = null,
  role = null,
  roles = null,
  requireAll = false,
  fallback = null,
  mode = 'permission',
}) => {
  const {
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    hasRole,
    hasAnyRole,
  } = usePermissions();

  let hasAccess = false;

  if (mode === 'permission') {
    if (permission) {
      hasAccess = hasPermission(permission);
    } else if (permissions) {
      hasAccess = requireAll
        ? hasAllPermissions(permissions)
        : hasAnyPermission(permissions);
    }
  } else if (mode === 'role') {
    if (role) {
      hasAccess = hasRole(role);
    } else if (roles) {
      hasAccess = hasAnyRole(roles);
    }
  }

  return hasAccess ? children : fallback;
};

export default PermissionGate;
