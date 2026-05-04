import type { Alert, AttackGraph, DashboardSummary, NormalizedEvent, TimelineEvent } from "../types/domain";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  const json = await res.json();
  return json.data as T;
}

export const api = {
  getDashboard: () => request<DashboardSummary>("/api/dashboard/summary"),
  getEvents: (query = "") => request<NormalizedEvent[]>(`/api/events${query ? `?query=${encodeURIComponent(query)}` : ""}`),
  getAlerts: () => request<Alert[]>("/api/alerts"),
  updateAlertStatus: async (alertId: string, status: string) => request<Alert>(`/api/alerts/${alertId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  }),
  getTimeline: (userId: string) => request<{ user_id: string; events: TimelineEvent[] }>(`/api/timeline/${encodeURIComponent(userId)}`),
  getAttack: (alertId: string) => request<AttackGraph>(`/api/attack/${encodeURIComponent(alertId)}`),
  uploadCloudTrail: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<{ events: number; alerts: number }>("/api/events/upload", { method: "POST", body: form });
  },
  loadSample: () => request<{ events: number; alerts: number }>("/api/events/load-sample", { method: "POST" }),
};
