import React, { useMemo } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  Cell,
} from 'recharts';
import clsx from 'clsx';

const ReserveRatioChart = ({
  data = [],
  height = 400,
  showLegend = true,
  responsive = true,
  className = '',
  onBarClick = null,
}) => {
  // Calculate colors based on ratio
  const getBarColor = (ratio) => {
    if (ratio >= 100) return '#10b981'; // Green for compliant
    if (ratio >= 95) return '#fbbf24'; // Yellow for warning
    return '#ef4444'; // Red for non-compliant
  };

  const chartData = useMemo(() => {
    return data.map((item) => ({
      ...item,
      color: getBarColor(item.ratio || 100),
    }));
  }, [data]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-simplyfi-border-light">
          <p className="font-semibold text-simplyfi-navy text-sm">{data.asset || label}</p>
          <div className="space-y-1 mt-2 text-xs">
            {payload.map((entry, index) => (
              <p key={index} style={{ color: entry.color }}>
                <span className="text-simplyfi-text-muted">{entry.name}: </span>
                <span className="font-semibold">
                  {typeof entry.value === 'number' ? `$${entry.value.toLocaleString()}` : entry.value}
                </span>
              </p>
            ))}
            {data.ratio && (
              <p className="text-simplyfi-gold font-semibold mt-2">
                Ratio: {data.ratio.toFixed(2)}%
              </p>
            )}
          </div>
        </div>
      );
    }
    return null;
  };

  const containerClasses = clsx(
    'w-full',
    className
  );

  if (data.length === 0) {
    return (
      <div className={containerClasses} style={{ height: `${height}px` }}>
        <div className="flex items-center justify-center h-full bg-simplyfi-neutral-bg rounded-lg border border-dashed border-simplyfi-border-light">
          <p className="text-simplyfi-text-muted text-sm">No data available</p>
        </div>
      </div>
    );
  }

  const chartComponent = (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart
        data={chartData}
        margin={{ top: 20, right: 30, left: 0, bottom: 60 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" vertical={false} />
        <XAxis
          dataKey="asset"
          angle={-45}
          textAnchor="end"
          height={120}
          fontSize={12}
          tick={{ fill: '#6b7280' }}
        />
        <YAxis
          fontSize={12}
          tick={{ fill: '#6b7280' }}
          label={{ value: 'Amount ($)', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip content={<CustomTooltip />} />
        {showLegend && <Legend wrapperStyle={{ paddingTop: '20px' }} />}
        <ReferenceLine
          y={100}
          stroke="#0a1628"
          strokeDasharray="5 5"
          label={{
            value: '100% (Fully Reserved)',
            position: 'right',
            fill: '#0a1628',
            fontSize: 12,
          }}
        />
        {data.some((d) => d.reserves !== undefined) && (
          <Bar
            dataKey="reserves"
            name="Reserves"
            fill="#10b981"
            radius={[8, 8, 0, 0]}
            onClick={(data) => onBarClick?.(data, 'reserves')}
          />
        )}
        {data.some((d) => d.liabilities !== undefined) && (
          <Bar
            dataKey="liabilities"
            name="Liabilities"
            fill="#3b82f6"
            radius={[8, 8, 0, 0]}
            onClick={(data) => onBarClick?.(data, 'liabilities')}
          />
        )}
      </BarChart>
    </ResponsiveContainer>
  );

  return (
    <div className={clsx(containerClasses, 'bg-white rounded-lg')}>
      {chartComponent}
    </div>
  );
};

export default ReserveRatioChart;
