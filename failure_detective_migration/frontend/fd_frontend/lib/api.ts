export const API_BASE = (process.env.NEXT_PUBLIC_API_BASE_URL || 'https://failure-detection-agent.onrender.com').replace(/\/$/, '');
export type SessionInfo = { session_id: string; mode: 'guest' | 'authenticated'; guest_token?: string };
export type ChatResult = { reply: string; model?: string; tool_calls?: Array<Record<string, unknown>>; memory_mode?: string; session_id?: string; tool_limit_reached?: boolean; token_efficiency?: Record<string, unknown> };

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { ...init, headers: { 'Content-Type': 'application/json', ...(init?.headers || {}) }, cache: 'no-store' });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail || data);
    throw new Error(`${res.status}: ${detail || res.statusText}`);
  }
  return data as T;
}

export async function createGuestSession(): Promise<SessionInfo> {
  const session = await request<SessionInfo>('/api/auth/guest-session', { method: 'POST' });
  sessionStorage.setItem('fd_session', JSON.stringify(session));
  return session;
}
export async function createUserSession(accessToken: string): Promise<SessionInfo> {
  const session = await request<SessionInfo>('/api/auth/user-session', { method: 'POST', headers: { Authorization: `Bearer ${accessToken}` } });
  sessionStorage.setItem('fd_session', JSON.stringify(session));
  return session;
}
export function readSession(): SessionInfo | null {
  try { const raw = sessionStorage.getItem('fd_session'); return raw ? JSON.parse(raw) as SessionInfo : null; } catch { return null; }
}
export async function sendChat(message: string, history: Array<{role:'user'|'assistant';content:string}>, session: SessionInfo, accessToken?: string): Promise<ChatResult> {
  const headers: Record<string,string> = {};
  if (session.guest_token) headers['X-Guest-Token'] = session.guest_token;
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  return request<ChatResult>('/api/agent/chat', { method: 'POST', headers, body: JSON.stringify({ message, history, session_id: session.session_id }) });
}
export async function investigateWithSensor(message: string, file: File, session: SessionInfo, accessToken?: string): Promise<ChatResult> {
  const form = new FormData(); form.append('message', message); form.append('history', '[]'); form.append('session_id', session.session_id); form.append('file', file);
  const headers: Record<string,string> = {};
  if (session.guest_token) headers['X-Guest-Token'] = session.guest_token;
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  const res = await fetch(`${API_BASE}/api/agent/investigate-with-sensor`, { method: 'POST', headers, body: form });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) { const detail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail || data); throw new Error(`${res.status}: ${detail || res.statusText}`); }
  return data as ChatResult;
}
export async function getHealth() { return request<{status:string;service:string;version:string}>('/api/health'); }

export async function generateReport(payload: { machine: string; operating_conditions?: Record<string, unknown>; symptoms?: string[]; findings?: string[]; ranked_faults?: Array<Record<string, unknown>>; sensor_findings?: string[]; recommended_actions?: string[]; limitations?: string[] }, session: SessionInfo, accessToken?: string): Promise<{report_markdown:string; format:string}> {
  const headers: Record<string,string> = {};
  if (session.guest_token) headers['X-Guest-Token'] = session.guest_token;
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  return request('/api/reports/generate', { method: 'POST', headers, body: JSON.stringify(payload) });
}
