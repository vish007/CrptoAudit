import { useSelector, useDispatch } from 'react-redux';
import { useCallback, useEffect } from 'react';
import {
  fetchEngagements,
  fetchEngagementById,
  createEngagement,
  updateEngagement,
  deleteEngagement,
  selectEngagements,
  selectCurrentEngagement,
  selectEngagementIsLoading,
  selectEngagementError,
  selectEngagementFilters,
  selectEngagementPagination,
  setCurrentEngagement,
  setFilters,
  setPagination,
} from '../store/slices/engagementSlice';

/**
 * Custom hook for engagement state and actions
 * @returns {Object} Engagement state and methods
 */
export const useEngagement = () => {
  const dispatch = useDispatch();

  const engagements = useSelector(selectEngagements);
  const currentEngagement = useSelector(selectCurrentEngagement);
  const isLoading = useSelector(selectEngagementIsLoading);
  const error = useSelector(selectEngagementError);
  const filters = useSelector(selectEngagementFilters);
  const pagination = useSelector(selectEngagementPagination);

  const getEngagements = useCallback(
    (params = {}) => {
      return dispatch(fetchEngagements(params));
    },
    [dispatch]
  );

  const getEngagementById = useCallback(
    (id) => {
      return dispatch(fetchEngagementById(id));
    },
    [dispatch]
  );

  const createNewEngagement = useCallback(
    (engagementData) => {
      return dispatch(createEngagement(engagementData));
    },
    [dispatch]
  );

  const updateCurrentEngagement = useCallback(
    (id, engagementData) => {
      return dispatch(updateEngagement({ id, data: engagementData }));
    },
    [dispatch]
  );

  const deleteCurrentEngagement = useCallback(
    (id) => {
      return dispatch(deleteEngagement(id));
    },
    [dispatch]
  );

  const setCurrentEngagementData = useCallback(
    (engagement) => {
      dispatch(setCurrentEngagement(engagement));
    },
    [dispatch]
  );

  const updateFilters = useCallback(
    (newFilters) => {
      dispatch(setFilters(newFilters));
    },
    [dispatch]
  );

  const updatePagination = useCallback(
    (paginationData) => {
      dispatch(setPagination(paginationData));
    },
    [dispatch]
  );

  const getFilteredAndPaginatedEngagements = useCallback(
    async (filterParams = {}) => {
      const params = {
        ...filterParams,
        ...filters,
        page: pagination.page,
        pageSize: pagination.pageSize,
      };
      await dispatch(fetchEngagements(params));
    },
    [dispatch, filters, pagination]
  );

  // Auto-fetch engagements when filters or pagination change
  useEffect(() => {
    const params = {
      ...filters,
      page: pagination.page,
      pageSize: pagination.pageSize,
    };
    dispatch(fetchEngagements(params));
  }, [dispatch, filters, pagination]);

  return {
    engagements,
    currentEngagement,
    isLoading,
    error,
    filters,
    pagination,
    getEngagements,
    getEngagementById,
    createNewEngagement,
    updateCurrentEngagement,
    deleteCurrentEngagement,
    setCurrentEngagementData,
    updateFilters,
    updatePagination,
    getFilteredAndPaginatedEngagements,
  };
};

export default useEngagement;
