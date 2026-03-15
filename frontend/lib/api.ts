const API_BASE = '/api';

async function request(path: string, options?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `API Error: ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Dashboard
  getDashboardStats: () => request('/dashboard/stats'),

  // Data / Uploads
  uploadFile: async (file: File) => {
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(`${API_BASE}/data/upload`, { method: 'POST', body: form });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },
  getUploads: () => request('/data/uploads'),
  getUpload: (id: string) => request(`/data/uploads/${id}`),
  deleteUpload: (id: string) => request(`/data/uploads/${id}`, { method: 'DELETE' }),

  // Analysis
  getAgents: () => request('/analysis/agents'),
  runAgent: (agentName: string, uploadId: string, context?: object) =>
    request(`/analysis/run/${agentName}`, {
      method: 'POST',
      body: JSON.stringify({ upload_id: uploadId, context }),
    }),
  runPipeline: (uploadId: string, agents?: string[]) =>
    request('/analysis/pipeline', {
      method: 'POST',
      body: JSON.stringify({ upload_id: uploadId, agents }),
    }),
  getResults: (uploadId: string, agentName?: string) =>
    request(`/analysis/results/${uploadId}${agentName ? `?agent_name=${agentName}` : ''}`),

  // Chat
  sendMessage: (uploadId: string, message: string, sessionId?: string) =>
    request('/chat/send', {
      method: 'POST',
      body: JSON.stringify({ upload_id: uploadId, message, session_id: sessionId }),
    }),
  getChatHistory: (sessionId: string, uploadId?: string) =>
    request(`/chat/history/${sessionId}${uploadId ? `?upload_id=${uploadId}` : ''}`),
  clearChat: (sessionId: string) =>
    request(`/chat/history/${sessionId}`, { method: 'DELETE' }),
};
