import { useSelector } from 'react-redux';
import { selectUserRole, selectUserPermissions } from '../store/slices/authSlice';
import { ROLE_PERMISSIONS } from '../utils/constants';

/**
 * Custom hook for checking user permissions
 * @returns {Object} Permission checking methods
 */
export const usePermissions = () => {
  const userRole = useSelector(selectUserRole);
  const userPermissions = useSelector(selectUserPermissions);

  /**
   * Check if user has a specific permission
   * @param {string} permission - Permission to check
   * @returns {boolean} Whether user has permission
   */
  const hasPermission = (permission) => {
    if (!userRole || !userPermissions) return false;
    return userPermissions.includes(permission);
  };

  /**
   * Check if user has any of the specified permissions
   * @param {string[]} permissions - Permissions to check
   * @returns {boolean} Whether user has any permission
   */
  const hasAnyPermission = (permissions) => {
    if (!userRole || !userPermissions) return false;
    return permissions.some((perm) => userPermissions.includes(perm));
  };

  /**
   * Check if user has all of the specified permissions
   * @param {string[]} permissions - Permissions to check
   * @returns {boolean} Whether user has all permissions
   */
  const hasAllPermissions = (permissions) => {
    if (!userRole || !userPermissions) return false;
    return permissions.every((perm) => userPermissions.includes(perm));
  };

  /**
   * Check if user has a specific role
   * @param {string} role - Role to check
   * @returns {boolean} Whether user has role
   */
  const hasRole = (role) => {
    return userRole === role;
  };

  /**
   * Check if user has any of the specified roles
   * @param {string[]} roles - Roles to check
   * @returns {boolean} Whether user has any role
   */
  const hasAnyRole = (roles) => {
    return roles.includes(userRole);
  };

  /**
   * Get all permissions for current role
   * @returns {string[]} Array of permissions for role
   */
  const getRolePermissions = () => {
    if (!userRole) return [];
    return ROLE_PERMISSIONS[userRole] || [];
  };

  /**
   * Check if user is admin
   * @returns {boolean} Whether user is admin
   */
  const isAdmin = () => {
    return userRole === 'SuperAdmin';
  };

  /**
   * Check if user is auditor
   * @returns {boolean} Whether user is auditor
   */
  const isAuditor = () => {
    return userRole === 'Auditor';
  };

  /**
   * Check if user is VASP admin
   * @returns {boolean} Whether user is VASP admin
   */
  const isVASPAdmin = () => {
    return userRole === 'VASP_Admin';
  };

  /**
   * Check if user can edit resource
   * @returns {boolean} Whether user can edit
   */
  const canEdit = () => {
    return hasAnyPermission(['manage_engagement', 'manage_assets', 'manage_users']);
  };

  /**
   * Check if user can delete resource
   * @returns {boolean} Whether user can delete
   */
  const canDelete = () => {
    return hasPermission('manage_system_settings') || isAdmin();
  };

  /**
   * Check if user can approve resources
   * @returns {boolean} Whether user can approve
   */
  const canApprove = () => {
    return hasPermission('approve_assets') || hasPermission('approve_reports') || isAdmin();
  };

  return {
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    hasRole,
    hasAnyRole,
    getRolePermissions,
    isAdmin,
    isAuditor,
    isVASPAdmin,
    canEdit,
    canDelete,
    canApprove,
    userRole,
    userPermissions,
  };
};

export default usePermissions;
