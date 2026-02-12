import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Briefcase,
  Coins,
  GitBranch,
  Blocks,
  FileText,
  Settings,
  Users,
  LogOut,
  Menu,
  X,
  ChevronDown,
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { usePermissions } from '../../hooks/usePermissions';
import { useDispatch, useSelector } from 'react-redux';
import { toggleSidebar, selectSidebarOpen } from '../../store/slices/uiSlice';
import clsx from 'clsx';

const Sidebar = () => {
  const location = useLocation();
  const dispatch = useDispatch();
  const sidebarOpen = useSelector(selectSidebarOpen);
  const { user, logout } = useAuth();
  const { hasPermission } = usePermissions();
  const [expandedMenus, setExpandedMenus] = useState({});

  const menuItems = [
    {
      label: 'Dashboard',
      icon: LayoutDashboard,
      path: '/dashboard',
      requiredPermission: null,
    },
    {
      label: 'Engagements',
      icon: Briefcase,
      path: '/engagements',
      requiredPermission: 'view_assignments',
      submenu: [
        { label: 'All Engagements', path: '/engagements' },
        { label: 'Create Engagement', path: '/engagements/create' },
        { label: 'My Assignments', path: '/engagements/assignments' },
      ],
    },
    {
      label: 'Assets',
      icon: Coins,
      path: '/assets',
      requiredPermission: 'view_assets',
      submenu: [
        { label: 'Asset Management', path: '/assets' },
        { label: 'Import Assets', path: '/assets/import' },
        { label: 'Verification', path: '/assets/verification' },
      ],
    },
    {
      label: 'Merkle Trees',
      icon: GitBranch,
      path: '/merkle',
      requiredPermission: 'manage_merkle',
      submenu: [
        { label: 'Merkle Trees', path: '/merkle' },
        { label: 'Create Tree', path: '/merkle/create' },
        { label: 'Verification', path: '/merkle/verification' },
      ],
    },
    {
      label: 'Blockchain',
      icon: Blocks,
      path: '/blockchain',
      requiredPermission: 'view_blockchain_data',
      submenu: [
        { label: 'On-Chain Data', path: '/blockchain' },
        { label: 'Address Monitor', path: '/blockchain/monitor' },
        { label: 'Verification', path: '/blockchain/verification' },
      ],
    },
    {
      label: 'Reports',
      icon: FileText,
      path: '/reports',
      requiredPermission: 'view_reports',
      submenu: [
        { label: 'Reports', path: '/reports' },
        { label: 'Generate Report', path: '/reports/generate' },
        { label: 'Templates', path: '/reports/templates' },
      ],
    },
    {
      label: 'Administration',
      icon: Users,
      path: '/admin',
      requiredPermission: 'manage_users',
      submenu: [
        { label: 'User Management', path: '/admin/users' },
        { label: 'Tenant Management', path: '/admin/tenants' },
        { label: 'Audit Logs', path: '/admin/audit-logs' },
        { label: 'Settings', path: '/admin/settings' },
      ],
    },
    {
      label: 'Settings',
      icon: Settings,
      path: '/settings',
      requiredPermission: null,
      submenu: [
        { label: 'Profile', path: '/settings/profile' },
        { label: 'Security', path: '/settings/security' },
        { label: 'Preferences', path: '/settings/preferences' },
      ],
    },
  ];

  const filteredMenuItems = menuItems.filter(
    (item) => !item.requiredPermission || hasPermission(item.requiredPermission)
  );

  const toggleSubmenu = (label) => {
    setExpandedMenus((prev) => ({
      ...prev,
      [label]: !prev[label],
    }));
  };

  const isActive = (path) => location.pathname.startsWith(path);

  const handleLogout = async () => {
    await logout();
    window.location.href = '/auth/login';
  };

  return (
    <>
      {/* Mobile Toggle */}
      <button
        onClick={() => dispatch(toggleSidebar())}
        className="fixed top-4 left-4 z-50 md:hidden p-2 rounded-lg bg-simplyfi-navy text-white"
      >
        {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      {/* Sidebar */}
      <aside
        className={clsx(
          'fixed left-0 top-0 h-screen bg-simplyfi-dark-navy text-white transition-all duration-300 z-40',
          sidebarOpen ? 'w-64' : 'w-20'
        )}
      >
        {/* Logo */}
        <div className="flex items-center justify-center h-16 border-b border-simplyfi-gold/20">
          <Link to="/dashboard" className="flex items-center gap-2 px-4">
            {sidebarOpen ? (
              <>
                <div className="w-8 h-8 bg-simplyfi-gold rounded-lg flex items-center justify-center font-bold text-simplyfi-dark-navy">
                  SF
                </div>
                <span className="font-bold text-lg">SimplyFI</span>
              </>
            ) : (
              <div className="w-8 h-8 bg-simplyfi-gold rounded-lg flex items-center justify-center font-bold text-simplyfi-dark-navy text-sm">
                SF
              </div>
            )}
          </Link>
        </div>

        {/* Menu */}
        <nav className="flex-1 overflow-y-auto py-4">
          {filteredMenuItems.map((item) => (
            <div key={item.label}>
              {item.submenu ? (
                <>
                  <button
                    onClick={() => toggleSubmenu(item.label)}
                    className={clsx(
                      'w-full flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors duration-200 hover:bg-simplyfi-navy/50',
                      expandedMenus[item.label] && 'bg-simplyfi-navy/50'
                    )}
                  >
                    <item.icon className="w-5 h-5 flex-shrink-0" />
                    {sidebarOpen && (
                      <>
                        <span>{item.label}</span>
                        <ChevronDown
                          className={clsx(
                            'w-4 h-4 ml-auto transition-transform',
                            expandedMenus[item.label] && 'rotate-180'
                          )}
                        />
                      </>
                    )}
                  </button>

                  {/* Submenu */}
                  {sidebarOpen && expandedMenus[item.label] && (
                    <div className="bg-simplyfi-navy/30">
                      {item.submenu.map((subitem) => (
                        <Link
                          key={subitem.path}
                          to={subitem.path}
                          className={clsx(
                            'flex items-center gap-3 px-4 py-2 text-xs font-medium text-white/70 hover:text-white hover:bg-simplyfi-navy/50 transition-colors duration-200 ml-8'
                          )}
                        >
                          {subitem.label}
                        </Link>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <Link
                  to={item.path}
                  className={clsx(
                    'flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors duration-200',
                    isActive(item.path)
                      ? 'bg-simplyfi-gold/20 text-simplyfi-gold border-l-4 border-simplyfi-gold'
                      : 'hover:bg-simplyfi-navy/50'
                  )}
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  {sidebarOpen && <span>{item.label}</span>}
                </Link>
              )}
            </div>
          ))}
        </nav>

        {/* User Profile */}
        <div className="border-t border-simplyfi-gold/20 p-4">
          {sidebarOpen ? (
            <div className="space-y-3">
              <div className="text-sm">
                <p className="font-medium text-simplyfi-gold truncate">{user?.firstName} {user?.lastName}</p>
                <p className="text-xs text-white/60 truncate">{user?.email}</p>
              </div>
              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-2 px-3 py-2 text-sm font-medium bg-simplyfi-red-warning/20 hover:bg-simplyfi-red-warning/30 text-simplyfi-red-warning rounded-lg transition-colors duration-200"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            </div>
          ) : (
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center p-2 text-simplyfi-red-warning hover:bg-simplyfi-red-warning/20 rounded-lg transition-colors duration-200"
              title="Logout"
            >
              <LogOut className="w-5 h-5" />
            </button>
          )}
        </div>
      </aside>

      {/* Backdrop for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => dispatch(toggleSidebar())}
        />
      )}
    </>
  );
};

export default Sidebar;
