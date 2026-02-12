import React from 'react';
import clsx from 'clsx';
import { Loader } from 'lucide-react';

const LoadingSpinner = ({
  size = 'md',
  variant = 'primary',
  fullScreen = false,
  message = '',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24',
  };

  const variantClasses = {
    primary: 'text-simplyfi-navy',
    accent: 'text-simplyfi-gold',
    white: 'text-white',
  };

  const spinnerClasses = clsx(
    'animate-spin',
    sizeClasses[size] || sizeClasses.md,
    variantClasses[variant] || variantClasses.primary,
    className
  );

  const container = fullScreen ? (
    <div className="fixed inset-0 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm z-50">
      <Loader className={spinnerClasses} />
      {message && <p className="mt-4 text-simplyfi-text-dark text-center">{message}</p>}
    </div>
  ) : (
    <div className="flex flex-col items-center justify-center">
      <Loader className={spinnerClasses} />
      {message && <p className="mt-3 text-simplyfi-text-dark text-sm">{message}</p>}
    </div>
  );

  return container;
};

export default LoadingSpinner;
