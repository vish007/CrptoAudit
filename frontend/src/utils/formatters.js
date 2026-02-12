import { format, formatDistance, parseISO } from 'date-fns';
import { CRYPTO_PRECISION, FIAT_PRECISION, DATE_FORMAT, DATETIME_FORMAT, TIME_FORMAT } from './constants';

export const formatDate = (date, formatStr = DATE_FORMAT) => {
  if (!date) return '-';
  try {
    const parsedDate = typeof date === 'string' ? parseISO(date) : date;
    return format(parsedDate, formatStr);
  } catch {
    return '-';
  }
};

export const formatDateTime = (date, formatStr = DATETIME_FORMAT) => {
  if (!date) return '-';
  try {
    const parsedDate = typeof date === 'string' ? parseISO(date) : date;
    return format(parsedDate, formatStr);
  } catch {
    return '-';
  }
};

export const formatTime = (date, formatStr = TIME_FORMAT) => {
  if (!date) return '-';
  try {
    const parsedDate = typeof date === 'string' ? parseISO(date) : date;
    return format(parsedDate, formatStr);
  } catch {
    return '-';
  }
};

export const formatRelativeTime = (date) => {
  if (!date) return '-';
  try {
    const parsedDate = typeof date === 'string' ? parseISO(date) : date;
    return formatDistance(parsedDate, new Date(), { addSuffix: true });
  } catch {
    return '-';
  }
};

export const formatNumber = (value, options = {}) => {
  const {
    decimals = 2,
    notation = 'standard',
    minimumFractionDigits = 0,
    maximumFractionDigits = decimals,
  } = options;

  if (value === null || value === undefined) return '-';

  try {
    return new Intl.NumberFormat('en-US', {
      style: 'decimal',
      notation,
      minimumFractionDigits,
      maximumFractionDigits,
    }).format(parseFloat(value));
  } catch {
    return '-';
  }
};

export const formatCurrency = (value, currency = 'USD', decimals = 2) => {
  if (value === null || value === undefined) return '-';

  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(parseFloat(value));
  } catch {
    return '-';
  }
};

export const formatCrypto = (value, decimals = CRYPTO_PRECISION) => {
  return formatNumber(value, { decimals, maximumFractionDigits: decimals });
};

export const formatPercentage = (value, decimals = 2) => {
  if (value === null || value === undefined) return '-';

  try {
    const numValue = parseFloat(value);
    return `${new Intl.NumberFormat('en-US', {
      style: 'decimal',
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(numValue)}%`;
  } catch {
    return '-';
  }
};

export const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';
  if (!bytes) return '-';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

export const formatCryptoAddress = (address, displayLength = 10) => {
  if (!address) return '-';
  if (address.length <= displayLength) return address;

  const start = address.substring(0, displayLength / 2);
  const end = address.substring(address.length - displayLength / 2);
  return `${start}...${end}`;
};

export const formatTxHash = (hash, displayLength = 10) => {
  return formatCryptoAddress(hash, displayLength);
};

export const formatBlockNumber = (blockNumber) => {
  if (!blockNumber) return '-';
  return `#${formatNumber(blockNumber, { decimals: 0, maximumFractionDigits: 0 })}`;
};

export const formatUSDValue = (value, decimals = FIAT_PRECISION) => {
  return formatCurrency(value, 'USD', decimals);
};

export const formatGasPrice = (gwei) => {
  if (!gwei) return '-';
  return `${formatNumber(gwei, { decimals: 2 })} Gwei`;
};

export const formatTimestamp = (timestamp) => {
  if (!timestamp) return '-';

  try {
    const date = new Date(timestamp * 1000);
    return formatDateTime(date);
  } catch {
    return '-';
  }
};

export const formatDuration = (milliseconds) => {
  if (!milliseconds) return '0s';

  const seconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (days > 0) return `${days}d ${hours % 24}h`;
  if (hours > 0) return `${hours}h ${minutes % 60}m`;
  if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
  return `${seconds}s`;
};

export const formatFileSize = (bytes) => {
  return formatBytes(bytes, 2);
};

export const formatUsername = (email) => {
  if (!email) return '-';
  return email.split('@')[0];
};

export const formatStatus = (status) => {
  if (!status) return '-';
  return status
    .toLowerCase()
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (char) => char.toUpperCase());
};

export const formatIPAddress = (ip) => {
  if (!ip) return '-';
  return ip;
};

export const formatCountdown = (seconds) => {
  if (!seconds || seconds <= 0) return 'Expired';

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (hours > 0) return `${hours}h ${minutes}m`;
  if (minutes > 0) return `${minutes}m ${secs}s`;
  return `${secs}s`;
};

export const formatMarketCap = (value) => {
  if (!value) return '-';

  const absValue = Math.abs(value);

  if (absValue >= 1e12) {
    return `$${(value / 1e12).toFixed(2)}T`;
  } else if (absValue >= 1e9) {
    return `$${(value / 1e9).toFixed(2)}B`;
  } else if (absValue >= 1e6) {
    return `$${(value / 1e6).toFixed(2)}M`;
  } else if (absValue >= 1e3) {
    return `$${(value / 1e3).toFixed(2)}K`;
  }

  return `$${value.toFixed(2)}`;
};
