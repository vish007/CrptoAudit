import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchEngagements, selectEngagements, selectEngagementIsLoading } from '../../store/slices/engagementSlice';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import DataTable from '../../components/common/DataTable';
import { Plus } from 'lucide-react';

const EngagementsPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const engagements = useSelector(selectEngagements);
  const isLoading = useSelector(selectEngagementIsLoading);

  useEffect(() => {
    dispatch(fetchEngagements());
  }, [dispatch]);

  const columns = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'status', label: 'Status', sortable: true },
    { key: 'type', label: 'Type', sortable: true },
    { key: 'startDate', label: 'Start Date', sortable: true },
    { key: 'progress', label: 'Progress', render: (value) => `${value || 0}%` },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-simplyfi-text-dark">Engagements</h1>
        <Button
          variant="primary"
          icon={Plus}
          onClick={() => navigate('/engagements/create')}
        >
          Create Engagement
        </Button>
      </div>

      <Card>
        <DataTable
          columns={columns}
          data={engagements}
          isLoading={isLoading}
          onRowClick={(row) => navigate(`/engagements/${row.id}`)}
          emptyMessage="No engagements found"
        />
      </Card>
    </div>
  );
};

export default EngagementsPage;
