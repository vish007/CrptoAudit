import React, { useState } from 'react';
import { Bell, Search, ChevronDown, LogOut, Settings, User } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import clsx from 'clsx';

const Header = ({ title = 'Dashboard', breadcrumbs = [] }) => {
  const { user, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  const handleLogout = async () => {
    await logout();
    window.location.href = '/auth/login';
  };

  return (
    <header className="bg-white border-b border-simplyfi-border-light sticky top-0 z-30">
      <div className="flex items-center justify-between h-16 px-6 gap-4">
        {/* Title and Breadcrumbs */}
        <div className="flex-1 min-w-0">
          <h1 className="text-2xl font-bold text-simplyfi-text-dark truncate">{title}</h1>
          {breadcrumbs.length > 0 && (
            <nav className="flex items-center gap-2 mt-1 text-xs text-simplyfi-text-muted">
              {breadcrumbs.map((crumb, idx) => (
                <React.Fragment key={idx}>
                  {idx > 0 && <span>/</span>}
                  <span>{crumb}</span>
                </React.Fragment>
              ))}
            </nav>
          )}
        </div>

        {/* Search Bar */}
        <div className="hidden md:flex flex-1 max-w-xs">
          <div className="relative w-full">
            <Search className="absolute left-3 top-3 w-4 h-4 text-simplyfi-text-muted" />
            <input
              type="text"
              placeholder="Search..."
              className="w-full pl-10 pr-4 py-2 border border-simplyfi-border-light rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-simplyfi-gold"
            />
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
            >
              <Bell className="w-5 h-5 text-simplyfi-text-muted" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-simplyfi-red-warning rounded-full" />
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white border border-simplyfi-border-light rounded-lg shadow-lg z-50">
                <div className="p-4 border-b border-simplyfi-border-light">
                  <h3 className="font-semibold text-simplyfi-text-dark">Notifications</h3>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  <div className="p-4 text-center text-simplyfi-text-muted text-sm">
                    No new notifications
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
            >
              <div className="w-8 h-8 bg-simplyfi-gold text-simplyfi-dark-navy rounded-lg flex items-center justify-center font-bold text-sm">
                {user?.firstName?.[0]}{user?.lastName?.[0]}
              </div>
              <div className="hidden sm:block text-left">
                <p className="text-sm font-medium text-simplyfi-text-dark">
                  {user?.firstName} {user?.lastName}
                </p>
                <p className="text-xs text-simplyfi-text-muted">{user?.role}</p>
              </div>
              <ChevronDown className="w-4 h-4 text-simplyfi-text-muted" />
            </button>

            {/* User Dropdown */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white border border-simplyfi-border-light rounded-lg shadow-lg z-50">
                <div className="p-4 border-b border-simplyfi-border-light">
                  <p className="text-sm font-medium text-simplyfi-text-dark">{user?.email}</p>
                </div>
                <nav className="p-2 space-y-1">
                  <a
                    href="/settings/profile"
                    className="flex items-center gap-3 px-3 py-2 text-sm text-simplyfi-text-dark hover:bg-gray-100 rounded-lg transition-colors duration-200"
                  >
                    <User className="w-4 h-4" />
                    Profile
                  </a>
                  <a
                    href="/settings"
                    className="flex items-center gap-3 px-3 py-2 text-sm text-simplyfi-text-dark hover:bg-gray-100 rounded-lg transition-colors duration-200"
                  >
                    <Settings className="w-4 h-4" />
                    Settings
                  </a>
                </nav>
                <div className="border-t border-simplyfi-border-light p-2">
                  <button
                    onClick={handleLogout}
                    className="flex items-center gap-3 px-3 py-2 w-full text-sm text-simplyfi-red-warning hover:bg-red-50 rounded-lg transition-colors duration-200"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
