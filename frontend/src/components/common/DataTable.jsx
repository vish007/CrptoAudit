import React, { useMemo, useState } from 'react';
import { ChevronUp, ChevronDown, Search } from 'lucide-react';
import Card from './Card';
import Button from './Button';
import clsx from 'clsx';

const DataTable = ({
  columns = [],
  data = [],
  onRowClick = null,
  selectable = false,
  searchable = true,
  sortable = true,
  paginated = true,
  pageSize = 10,
  isLoading = false,
  emptyMessage = 'No data available',
}) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRows, setSelectedRows] = useState(new Set());
  const [currentPage, setCurrentPage] = useState(1);

  // Filter data by search term
  const filteredData = useMemo(() => {
    if (!searchTerm) return data;

    return data.filter((row) =>
      columns.some((col) => {
        const value = row[col.key];
        return value && value.toString().toLowerCase().includes(searchTerm.toLowerCase());
      })
    );
  }, [data, searchTerm, columns]);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortable || !sortConfig.key) return filteredData;

    const sorted = [...filteredData].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (aValue === null || aValue === undefined) return 1;
      if (bValue === null || bValue === undefined) return -1;

      if (typeof aValue === 'string') {
        return sortConfig.direction === 'asc'
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      }

      return sortConfig.direction === 'asc' ? aValue - bValue : bValue - aValue;
    });

    return sorted;
  }, [filteredData, sortConfig, sortable]);

  // Paginate data
  const paginatedData = useMemo(() => {
    if (!paginated) return sortedData;

    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    return sortedData.slice(start, end);
  }, [sortedData, currentPage, pageSize, paginated]);

  const totalPages = paginated ? Math.ceil(sortedData.length / pageSize) : 1;

  const handleSort = (key) => {
    if (!sortable) return;

    setSortConfig((prev) => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  const handleSelectAll = () => {
    if (selectedRows.size === paginatedData.length) {
      setSelectedRows(new Set());
    } else {
      const newSelected = new Set();
      paginatedData.forEach((row, idx) => newSelected.add(idx));
      setSelectedRows(newSelected);
    }
  };

  const handleSelectRow = (idx) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(idx)) {
      newSelected.delete(idx);
    } else {
      newSelected.add(idx);
    }
    setSelectedRows(newSelected);
  };

  if (isLoading) {
    return (
      <Card>
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin">
            <div className="w-8 h-8 border-4 border-simplyfi-gold border-t-transparent rounded-full" />
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card padding="none" className="overflow-hidden">
      {/* Search Bar */}
      {searchable && (
        <div className="p-4 border-b border-simplyfi-border-light">
          <div className="relative">
            <Search className="absolute left-3 top-3 w-4 h-4 text-simplyfi-text-muted" />
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full pl-10 pr-4 py-2 border border-simplyfi-border-light rounded-lg focus:outline-none focus:ring-2 focus:ring-simplyfi-gold"
            />
          </div>
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-simplyfi-text-dark">
          <thead>
            <tr className="bg-gray-50 border-b border-simplyfi-border-light">
              {selectable && (
                <th className="px-4 py-3 text-left">
                  <input
                    type="checkbox"
                    checked={
                      paginatedData.length > 0 &&
                      selectedRows.size === paginatedData.length
                    }
                    onChange={handleSelectAll}
                    className="rounded cursor-pointer"
                  />
                </th>
              )}
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  className={clsx(
                    'px-4 py-3 text-left font-semibold text-simplyfi-text-muted',
                    sortable && col.sortable !== false && 'cursor-pointer hover:bg-gray-100'
                  )}
                >
                  <div className="flex items-center gap-2">
                    {col.label}
                    {sortable && col.sortable !== false && (
                      <div className="w-4 h-4 flex items-center justify-center">
                        {sortConfig.key === col.key ? (
                          sortConfig.direction === 'asc' ? (
                            <ChevronUp className="w-4 h-4" />
                          ) : (
                            <ChevronDown className="w-4 h-4" />
                          )
                        ) : (
                          <div className="w-1 h-1 bg-gray-300 rounded-full" />
                        )}
                      </div>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.length === 0 ? (
              <tr>
                <td colSpan={columns.length + (selectable ? 1 : 0)} className="px-4 py-8 text-center text-simplyfi-text-muted">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              paginatedData.map((row, rowIdx) => (
                <tr
                  key={rowIdx}
                  className="table-row"
                  onClick={() => onRowClick?.(row, rowIdx)}
                >
                  {selectable && (
                    <td className="px-4 py-3">
                      <input
                        type="checkbox"
                        checked={selectedRows.has(rowIdx)}
                        onChange={() => handleSelectRow(rowIdx)}
                        onClick={(e) => e.stopPropagation()}
                        className="rounded cursor-pointer"
                      />
                    </td>
                  )}
                  {columns.map((col) => (
                    <td key={col.key} className="px-4 py-3">
                      {col.render
                        ? col.render(row[col.key], row, rowIdx)
                        : row[col.key]}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {paginated && totalPages > 1 && (
        <div className="px-4 py-4 border-t border-simplyfi-border-light flex items-center justify-between">
          <div className="text-sm text-simplyfi-text-muted">
            Showing {(currentPage - 1) * pageSize + 1} to{' '}
            {Math.min(currentPage * pageSize, sortedData.length)} of {sortedData.length}
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="sm"
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
            >
              Previous
            </Button>
            <span className="text-sm">
              Page {currentPage} of {totalPages}
            </span>
            <Button
              variant="ghost"
              size="sm"
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </Card>
  );
};

export default DataTable;
