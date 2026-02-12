import api from './api';

export const getBlockchainData = async (params = {}) => {
  return api.get('/blockchain', { params });
};

export const getBlockchainDataById = async (id) => {
  return api.get(`/blockchain/${id}`);
};

export const submitBlockchainData = async (blockchainData) => {
  return api.post('/blockchain', blockchainData);
};

export const updateBlockchainData = async (id, blockchainData) => {
  return api.put(`/blockchain/${id}`, blockchainData);
};

export const deleteBlockchainData = async (id) => {
  return api.delete(`/blockchain/${id}`);
};

export const verifyBlockchainData = async (id, verificationData) => {
  return api.post(`/blockchain/${id}/verify`, verificationData);
};

export const rejectBlockchainData = async (id, reason) => {
  return api.post(`/blockchain/${id}/reject`, { reason });
};

export const getBlockchainBalance = async (network, address) => {
  return api.get(`/blockchain/balance/${network}/${address}`);
};

export const getBlockchainTransactions = async (network, address, params = {}) => {
  return api.get(`/blockchain/transactions/${network}/${address}`, { params });
};

export const getBlockchainTransaction = async (network, txHash) => {
  return api.get(`/blockchain/transaction/${network}/${txHash}`);
};

export const getBlockchainBlock = async (network, blockNumber) => {
  return api.get(`/blockchain/block/${network}/${blockNumber}`);
};

export const validateBlockchainAddress = async (network, address) => {
  return api.post(`/blockchain/validate-address`, { network, address });
};

export const getNetworkStatus = async (network) => {
  return api.get(`/blockchain/network-status/${network}`);
};

export const getAllNetworkStatuses = async () => {
  return api.get('/blockchain/network-statuses');
};

export const getAddressHistory = async (id, params = {}) => {
  return api.get(`/blockchain/${id}/address-history`, { params });
};

export const verifyAddressOwnership = async (id, signatureData) => {
  return api.post(`/blockchain/${id}/verify-ownership`, signatureData);
};

export const getBlockchainStatistics = async (network) => {
  return api.get(`/blockchain/statistics/${network}`);
};

export const getAssetOnChainProof = async (id) => {
  return api.get(`/blockchain/${id}/proof`);
};

export const verifyOnChainProof = async (proofData) => {
  return api.post('/blockchain/verify-proof', proofData);
};

export const getBlockchainFees = async (network) => {
  return api.get(`/blockchain/fees/${network}`);
};

export const monitorAddress = async (id, network, address) => {
  return api.post(`/blockchain/${id}/monitor`, { network, address });
};

export const stopMonitoringAddress = async (id) => {
  return api.post(`/blockchain/${id}/stop-monitoring`);
};

export const getAddressMonitoringStatus = async (id) => {
  return api.get(`/blockchain/${id}/monitoring-status`);
};
