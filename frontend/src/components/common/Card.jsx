import React from 'react';
import clsx from 'clsx';

const Card = React.forwardRef(
  (
    {
      className = '',
      children,
      padding = 'md',
      shadow = 'base',
      bordered = true,
      hover = false,
      ...props
    },
    ref
  ) => {
    const paddingClasses = {
      none: 'p-0',
      sm: 'p-3',
      md: 'p-6',
      lg: 'p-8',
    };

    const shadowClasses = {
      none: '',
      sm: 'shadow-sm',
      base: 'shadow-base',
      md: 'shadow-md',
      lg: 'shadow-lg',
    };

    const cardClasses = clsx(
      'bg-white rounded-xl overflow-hidden transition-all duration-300',
      paddingClasses[padding] || paddingClasses.md,
      shadowClasses[shadow] || shadowClasses.base,
      bordered && 'border border-simplyfi-border-light',
      hover && 'hover:shadow-md hover:border-simplyfi-gold/30 cursor-pointer',
      className
    );

    return (
      <div ref={ref} className={cardClasses} {...props}>
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

export default Card;
