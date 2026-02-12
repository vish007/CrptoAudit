import React, { useState, useMemo } from 'react';
import { CheckCircle2, Clock, AlertCircle, Zap, Link as LinkIcon } from 'lucide-react';
import Card from '../common/Card';
import StatusBadge from '../common/StatusBadge';

const VerificationTimeline = ({ events = [], autoScroll = true, filterable = true }) => {
  const [filterType, setFilterType] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  const eventTypes = [
    { id: 'on_chain', label: 'On-Chain', icon: LinkIcon, color: '#3b82f6' },
    { id: 'custodian', label: 'Custodian', icon: Clock, color: '#8b5cf6' },
    { id: 'defi', label: 'DeFi', icon: Zap, color: '#f59e0b' },
  ];

  const statusConfig = {
    verified: { icon: CheckCircle2, color: '#10b981', label: 'Verified' },
    pending: { icon: Clock, color: '#f59e0b', label: 'Pending' },
    failed: { icon: AlertCircle, color: '#ef4444', label: 'Failed' },
  };

  const filteredEvents = useMemo(() => {
    return events.filter((event) => {
      const typeMatch = filterType === 'all' || event.type === filterType;
      const statusMatch = filterStatus === 'all' || event.status === filterStatus;
      return typeMatch && statusMatch;
    });
  }, [events, filterType, filterStatus]);

  // Sort by timestamp (newest first)
  const sortedEvents = [...filteredEvents].sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
  );

  const getEventIcon = (type) => {
    const eventType = eventTypes.find((et) => et.id === type);
    const Icon = eventType?.icon || Clock;
    return <Icon className="w-5 h-5" style={{ color: eventType?.color }} />;
  };

  const getStatusIcon = (status) => {
    const config = statusConfig[status];
    const Icon = config?.icon || Clock;
    return <Icon className="w-5 h-5" style={{ color: config?.color }} />;
  };

  const getStatusBadge = (status) => {
    if (status === 'verified') return 'success';
    if (status === 'pending') return 'info';
    return 'error';
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <Card className="p-6">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-simplyfi-navy mb-4">Recent Verification Activity</h2>

        {filterable && (
          <div className="flex flex-wrap gap-3">
            {/* Type Filter */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-simplyfi-border-light rounded-lg text-sm text-simplyfi-text-muted focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
            >
              <option value="all">All Types</option>
              {eventTypes.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.label}
                </option>
              ))}
            </select>

            {/* Status Filter */}
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-2 border border-simplyfi-border-light rounded-lg text-sm text-simplyfi-text-muted focus:outline-none focus:ring-2 focus:ring-simplyfi-navy"
            >
              <option value="all">All Statuses</option>
              {Object.entries(statusConfig).map(([key, config]) => (
                <option key={key} value={key}>
                  {config.label}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Timeline */}
      {sortedEvents.length > 0 ? (
        <div className="space-y-4">
          {sortedEvents.map((event, idx) => {
            const eventType = eventTypes.find((et) => et.id === event.type);
            return (
              <div key={event.id || idx} className="relative pl-10">
                {/* Timeline dot and line */}
                <div className="absolute left-0 top-0 flex flex-col items-center">
                  <div className="w-5 h-5 rounded-full border-4 border-white flex items-center justify-center z-10" style={{ backgroundColor: eventType?.color }}>
                    {getEventIcon(event.type)}
                  </div>
                  {idx < sortedEvents.length - 1 && (
                    <div
                      className="w-0.5 h-12 mt-2"
                      style={{ backgroundColor: '#e5e7eb' }}
                    />
                  )}
                </div>

                {/* Event card */}
                <div className="p-4 border border-simplyfi-border-light rounded-lg hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 className="font-semibold text-simplyfi-navy">
                        {event.asset || 'Asset Verification'}
                      </h3>
                      <p className="text-xs text-simplyfi-text-muted mt-1">
                        {formatTime(event.timestamp)} • {eventType?.label}
                      </p>
                    </div>
                    <StatusBadge status={getStatusBadge(event.status)} size="sm">
                      {statusConfig[event.status]?.label}
                    </StatusBadge>
                  </div>

                  {event.details && (
                    <p className="text-sm text-simplyfi-text-muted mt-3">
                      {event.details}
                    </p>
                  )}

                  {event.metadata && (
                    <div className="mt-3 pt-3 border-t border-simplyfi-border-light space-y-2 text-xs">
                      {Object.entries(event.metadata).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-simplyfi-text-muted">{key}:</span>
                          <span className="text-simplyfi-navy font-medium">{value}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-12">
          <Clock className="w-12 h-12 text-simplyfi-border-light mx-auto mb-3" />
          <p className="text-simplyfi-text-muted">No verification events found</p>
        </div>
      )}

      {/* Summary Stats */}
      {events.length > 0 && (
        <div className="mt-6 pt-6 border-t border-simplyfi-border-light grid grid-cols-3 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-simplyfi-emerald">
              {events.filter((e) => e.status === 'verified').length}
            </p>
            <p className="text-xs text-simplyfi-text-muted mt-1">Verified</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-simplyfi-gold">
              {events.filter((e) => e.status === 'pending').length}
            </p>
            <p className="text-xs text-simplyfi-text-muted mt-1">Pending</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-simplyfi-red-warning">
              {events.filter((e) => e.status === 'failed').length}
            </p>
            <p className="text-xs text-simplyfi-text-muted mt-1">Failed</p>
          </div>
        </div>
      )}
    </Card>
  );
};

export default VerificationTimeline;
