import api from './api';

export const getMerkleTrees = async (params = {}) => {
  return api.get('/merkle', { params });
};

export const getMerkleTreeById = async (id) => {
  return api.get(`/merkle/${id}`);
};

export const createMerkleTree = async (merkleData) => {
  return api.post('/merkle', merkleData);
};

export const updateMerkleTree = async (id, merkleData) => {
  return api.put(`/merkle/${id}`, merkleData);
};

export const deleteMerkleTree = async (id) => {
  return api.delete(`/merkle/${id}`);
};

export const getMerkleRoot = async (id) => {
  return api.get(`/merkle/${id}/root`);
};

export const getMerkleProof = async (id, leafIndex) => {
  return api.get(`/merkle/${id}/proof/${leafIndex}`);
};

export const verifyMerkleProof = async (id, proofData) => {
  return api.post(`/merkle/${id}/verify-proof`, proofData);
};

export const verifyMerkleTree = async (id, verificationData) => {
  return api.post(`/merkle/${id}/verify`, verificationData);
};

export const rejectMerkleTree = async (id, reason) => {
  return api.post(`/merkle/${id}/reject`, { reason });
};

export const getMerkleTreeLeaves = async (id, params = {}) => {
  return api.get(`/merkle/${id}/leaves`, { params });
};

export const addMerkleTreeLeaves = async (id, leavesData) => {
  return api.post(`/merkle/${id}/leaves`, leavesData);
};

export const getMerkleTreePath = async (id, leafHash) => {
  return api.get(`/merkle/${id}/path/${leafHash}`);
};

export const getMerkleTreeStats = async (id) => {
  return api.get(`/merkle/${id}/stats`);
};

export const validateMerkleTree = async (id) => {
  return api.post(`/merkle/${id}/validate`);
};

export const generateMerkleTree = async (engagementId, assetsData) => {
  return api.post('/merkle/generate', { engagementId, assetsData });
};

export const exportMerkleTree = async (id, format = 'json') => {
  return api.get(`/merkle/${id}/export`, { params: { format }, responseType: 'blob' });
};

export const importMerkleTree = async (file, engagementId) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('engagementId', engagementId);
  return api.post('/merkle/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const compareMerkleTrees = async (tree1Id, tree2Id) => {
  return api.post('/merkle/compare', { tree1Id, tree2Id });
};

export const getMerkleTreeHistory = async (id, params = {}) => {
  return api.get(`/merkle/${id}/history`, { params });
};

export const recalculateMerkleTree = async (id) => {
  return api.post(`/merkle/${id}/recalculate`);
};
