import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDashboardData, selectDashboardStats, selectDashboardIsLoading } from '../../store/slices/dashboardSlice';
import Card from '../../components/common/Card';
import StatCard from '../../components/common/StatCard';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Briefcase, Coins, CheckCircle, AlertCircle } from 'lucide-react';

const DashboardPage = () => {
  const dispatch = useDispatch();
  const stats = useSelector(selectDashboardStats);
  const isLoading = useSelector(selectDashboardIsLoading);

  useEffect(() => {
    dispatch(fetchDashboardData());
  }, [dispatch]);

  if (isLoading && !stats) {
    return <LoadingSpinner message="Loading dashboard..." />;
  }

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          label="Active Engagements"
          value={stats?.activeEngagements || 0}
          icon={Briefcase}
          color="navy"
          trend="up"
          trendValue={12}
          loading={isLoading}
        />
        <StatCard
          label="Total Assets Under Audit"
          value={stats?.totalAssetsUnderAudit ? `$${stats.totalAssetsUnderAudit.toLocaleString()}` : '$0'}
          unit="USD"
          icon={Coins}
          color="gold"
          trend="up"
          trendValue={8}
          loading={isLoading}
        />
        <StatCard
          label="Completed Audits"
          value={stats?.completedAudits || 0}
          icon={CheckCircle}
          color="emerald"
          trend="up"
          trendValue={15}
          loading={isLoading}
        />
        <StatCard
          label="Compliance Score"
          value={stats?.complianceScore ? `${stats.complianceScore}%` : '0%'}
          icon={AlertCircle}
          color="gold"
          trend="down"
          trendValue={-2}
          loading={isLoading}
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Engagement Status" padding="lg">
          <div className="h-64 flex items-center justify-center text-simplyfi-text-muted">
            Chart placeholder
          </div>
        </Card>

        <Card title="Asset Breakdown" padding="lg">
          <div className="h-64 flex items-center justify-center text-simplyfi-text-muted">
            Chart placeholder
          </div>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card title="Recent Activity" padding="lg">
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium text-simplyfi-text-dark">Engagement created</p>
              <p className="text-xs text-simplyfi-text-muted">2 hours ago</p>
            </div>
            <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
              Created
            </span>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default DashboardPage;
