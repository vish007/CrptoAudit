import React from 'react';
import Card from './Card';
import clsx from 'clsx';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({
  label = '',
  value = '',
  unit = '',
  trend = null,
  trendValue = null,
  icon: Icon = null,
  color = 'navy',
  backgroundColor = null,
  onClick = null,
  loading = false,
}) => {
  const colorClasses = {
    navy: { bg: 'bg-simplyfi-navy/10', text: 'text-simplyfi-navy' },
    gold: { bg: 'bg-simplyfi-gold/10', text: 'text-simplyfi-gold' },
    emerald: { bg: 'bg-simplyfi-emerald/10', text: 'text-simplyfi-emerald' },
    red: { bg: 'bg-simplyfi-red-warning/10', text: 'text-simplyfi-red-warning' },
  };

  const colorConfig = colorClasses[color] || colorClasses.navy;
  const bgClass = backgroundColor || colorConfig.bg;

  return (
    <Card
      shadow="md"
      padding="md"
      className={clsx(
        onClick && 'cursor-pointer hover:shadow-lg',
        'transition-all duration-300'
      )}
      onClick={onClick}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-simplyfi-text-muted text-sm font-medium mb-1">{label}</p>
          <div className="flex items-baseline gap-2">
            <p className={clsx('text-3xl font-bold', colorConfig.text)}>
              {loading ? '-' : value}
            </p>
            {unit && <span className="text-simplyfi-text-muted text-sm">{unit}</span>}
          </div>

          {trend && trendValue !== null && (
            <div className="mt-3 flex items-center gap-1">
              {trend === 'up' ? (
                <TrendingUp className="w-4 h-4 text-simplyfi-emerald" />
              ) : (
                <TrendingDown className="w-4 h-4 text-simplyfi-red-warning" />
              )}
              <span
                className={clsx(
                  'text-sm font-medium',
                  trend === 'up' ? 'text-simplyfi-emerald' : 'text-simplyfi-red-warning'
                )}
              >
                {trendValue > 0 ? '+' : ''}
                {trendValue}%
              </span>
            </div>
          )}
        </div>

        {Icon && (
          <div className={clsx('p-3 rounded-lg', bgClass)}>
            <Icon className={clsx('w-6 h-6', colorConfig.text)} />
          </div>
        )}
      </div>
    </Card>
  );
};

export default StatCard;
