const API_BASE = '/api';

export async function fetchScripts() {
  const res = await fetch(`${API_BASE}/scripts`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.scripts ?? [];
}

export async function uploadScript(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/scripts/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function deleteScript(filename) {
  const res = await fetch(`${API_BASE}/scripts/${encodeURIComponent(filename)}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Delete failed');
  return res.json();
}

export async function generateScript({ messages, pageCount }) {
  const res = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages, page_count: pageCount }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(err.error || 'Generation failed');
  }
  return res.json();
}

export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      return { connected: false, error: data.error || `Flask returned ${res.status}` };
    }
    const data = await res.json();
    if (data.status === 'connected') {
      return { connected: true, models: data.models || [] };
    }
    return { connected: false, error: data.error || 'LM Studio disconnected' };
  } catch (e) {
    return { connected: false, error: `Cannot reach Flask backend: ${e.message}` };
  }
}
