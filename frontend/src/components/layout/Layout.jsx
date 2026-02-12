import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import { useSelector } from 'react-redux';
import { selectSidebarOpen } from '../../store/slices/uiSlice';
import clsx from 'clsx';

const Layout = ({ children, title = 'Dashboard', breadcrumbs = [] }) => {
  const sidebarOpen = useSelector(selectSidebarOpen);

  return (
    <div className="flex h-screen bg-simplyfi-neutral-bg overflow-hidden">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main
        className={clsx(
          'flex flex-col flex-1 transition-all duration-300',
          sidebarOpen ? 'md:ml-64' : 'md:ml-20'
        )}
      >
        {/* Header */}
        <Header title={title} breadcrumbs={breadcrumbs} />

        {/* Page Content */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-6 md:p-8 max-w-7xl mx-auto w-full">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Layout;
