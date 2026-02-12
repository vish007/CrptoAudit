import React from 'react';
import clsx from 'clsx';
import { AlertCircle, CheckCircle, Clock, XCircle, Info } from 'lucide-react';

const StatusBadge = ({ status = '', variant = 'default', size = 'md', icon = true, children }) => {
  const statusConfig = {
    success: {
      bg: 'bg-emerald-100',
      text: 'text-emerald-800',
      icon: CheckCircle,
    },
    error: {
      bg: 'bg-red-100',
      text: 'text-red-800',
      icon: XCircle,
    },
    warning: {
      bg: 'bg-orange-100',
      text: 'text-orange-800',
      icon: AlertCircle,
    },
    info: {
      bg: 'bg-blue-100',
      text: 'text-blue-800',
      icon: Info,
    },
    pending: {
      bg: 'bg-gray-100',
      text: 'text-gray-800',
      icon: Clock,
    },
  };

  const variantConfig = {
    default: { bg: 'bg-gray-100', text: 'text-gray-700' },
    primary: { bg: 'bg-simplyfi-navy/10', text: 'text-simplyfi-navy' },
    accent: { bg: 'bg-simplyfi-gold/10', text: 'text-simplyfi-gold' },
  };

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs gap-1',
    md: 'px-3 py-1.5 text-sm gap-1.5',
    lg: 'px-4 py-2 text-base gap-2',
  };

  const config = statusConfig[status] || variantConfig[variant];
  const Icon = config.icon;

  const badgeClasses = clsx(
    'inline-flex items-center rounded-full font-medium',
    config.bg,
    config.text,
    sizeClasses[size] || sizeClasses.md
  );

  return (
    <span className={badgeClasses}>
      {icon && Icon && <Icon className="w-4 h-4 flex-shrink-0" />}
      {children || status}
    </span>
  );
};

export default StatusBadge;
