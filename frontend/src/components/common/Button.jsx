import React from 'react';
import { Loader } from 'lucide-react';
import clsx from 'clsx';

const Button = React.forwardRef(
  (
    {
      variant = 'primary',
      size = 'md',
      disabled = false,
      isLoading = false,
      icon: Icon = null,
      iconPosition = 'left',
      fullWidth = false,
      className = '',
      children,
      onClick,
      type = 'button',
      ...props
    },
    ref
  ) => {
    const baseClasses = 'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2';

    const variantClasses = {
      primary: 'bg-simplyfi-navy text-white hover:bg-simplyfi-dark-navy shadow-md hover:shadow-lg focus:ring-simplyfi-navy',
      secondary: 'bg-gray-200 text-simplyfi-text-dark hover:bg-gray-300 focus:ring-gray-400',
      accent: 'bg-simplyfi-gold text-simplyfi-dark-navy hover:bg-simplyfi-light-gold shadow-md hover:shadow-lg focus:ring-simplyfi-gold',
      danger: 'bg-simplyfi-red-warning text-white hover:bg-red-600 focus:ring-simplyfi-red-warning',
      ghost: 'bg-transparent text-simplyfi-navy hover:bg-gray-100 focus:ring-simplyfi-navy',
      success: 'bg-simplyfi-emerald text-white hover:bg-emerald-700 focus:ring-simplyfi-emerald',
    };

    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
      xl: 'px-8 py-4 text-lg',
    };

    const buttonClasses = clsx(
      baseClasses,
      variantClasses[variant] || variantClasses.primary,
      sizeClasses[size] || sizeClasses.md,
      fullWidth && 'w-full',
      isLoading && 'opacity-75',
      className
    );

    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled || isLoading}
        onClick={onClick}
        className={buttonClasses}
        {...props}
      >
        {isLoading ? (
          <>
            <Loader className="w-4 h-4 animate-spin" />
            {children}
          </>
        ) : (
          <>
            {Icon && iconPosition === 'left' && <Icon className="w-4 h-4" />}
            {children}
            {Icon && iconPosition === 'right' && <Icon className="w-4 h-4" />}
          </>
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
