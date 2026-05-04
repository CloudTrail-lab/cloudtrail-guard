import { useEffect, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import type { Alert, AttackGraph, DashboardSummary, NormalizedEvent, TimelineEvent } from "./types/domain";
import { api } from "./services/api";
import { Header, Sidebar } from "./components/Layout";
import { DetailPanel } from "./components/DetailPanel";
import { Card } from "./components/ui";
import { DashboardPage } from "./pages/DashboardPage";
import { EventExplorerPage } from "./pages/EventExplorerPage";
import { DetectionPage } from "./pages/DetectionPage";
import { TimelinePage } from "./pages/TimelinePage";
import { ReconstructionPage } from "./pages/ReconstructionPage";

export default function App() {
  const [page, setPage] = useState("dashboard");
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [dashboard, setDashboard] = useState<DashboardSummary | null>(null);
  const [events, setEvents] = useState<NormalizedEvent[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [timeline, setTimeline] = useState<TimelineEvent[]>([]);
  const [attackGraph, setAttackGraph] = useState<AttackGraph | null>(null);
  const [detailItem, setDetailItem] = useState<Alert | NormalizedEvent | null>(null);
  const [selectedUser, setSelectedUser] = useState("admin-role");
  const [selectedAlert, setSelectedAlert] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function refreshAll() {
    setError(null);
    try {
      const [dashboardData, eventData, alertData] = await Promise.all([
        api.getDashboard(),
        api.getEvents(query),
        api.getAlerts(),
      ]);
      setDashboard(dashboardData);
      setEvents(eventData);
      setAlerts(alertData);
      const firstAlert = alertData[0]?.alert_id || null;
      setSelectedAlert(firstAlert);
      const user = alertData[0]?.user_id || eventData[0]?.principal || "admin-role";
      setSelectedUser(user);
      const timelineData = await api.getTimeline(user);
      setTimeline(timelineData.events);
      if (firstAlert) setAttackGraph(await api.getAttack(firstAlert));
    } catch (e: any) {
      setError(e.message || "API request failed. Start backend on port 8000.");
    }
  }

  useEffect(() => { refreshAll(); }, []);

  useEffect(() => {
    const timer = setTimeout(() => api.getEvents(query).then(setEvents).catch(() => undefined), 300);
    return () => clearTimeout(timer);
  }, [query]);

  async function updateStatus(alertId: string, status: string) {
    await api.updateAlertStatus(alertId, status);
    const alertData = await api.getAlerts();
    setAlerts(alertData);
    setDashboard(await api.getDashboard());
  }

  async function openAlert(alert: Alert) {
    setDetailItem(alert);
    setSelectedUser(alert.user_id);
    setSelectedAlert(alert.alert_id);
    const timelineData = await api.getTimeline(alert.user_id);
    setTimeline(timelineData.events);
    setAttackGraph(await api.getAttack(alert.alert_id));
  }

  async function handleUpload(file: File) {
    await api.uploadCloudTrail(file);
    await refreshAll();
  }

  const openAlerts = useMemo(() => alerts.filter(a => a.status === "new").length, [alerts]);

  const renderPage = () => {
    if (error) return <Card className="p-8 text-red-200"><div className="mb-2 font-semibold">Backend connection failed</div><div className="text-sm text-red-100/80">{error}</div><div className="mt-4 font-mono text-xs text-slate-400">cd backend && uvicorn app.main:app --reload --port 8000</div></Card>;
    if (page === "dashboard") return <DashboardPage data={dashboard} setPage={setPage} />;
    if (page === "explorer") return <EventExplorerPage events={events} openEvent={setDetailItem} />;
    if (page === "timeline") return <TimelinePage userId={selectedUser} timeline={timeline} setPage={setPage} />;
    if (page === "detection") return <DetectionPage alerts={alerts} statusFilter={statusFilter} setStatusFilter={setStatusFilter} openAlert={openAlert} updateStatus={updateStatus} />;
    return <ReconstructionPage graph={attackGraph} openEvent={setDetailItem} events={events} />;
  };

  return <div className="min-h-screen bg-slate-950 text-slate-100">
    <Header openAlerts={openAlerts} />
    <div className="flex min-h-[calc(100vh-80px)]">
      <Sidebar page={page} setPage={setPage} query={query} setQuery={setQuery} setStatusFilter={setStatusFilter} />
      <main className="min-w-0 flex-1 overflow-x-hidden bg-[radial-gradient(circle_at_top_right,rgba(24,144,255,0.12),transparent_30%),linear-gradient(180deg,#020617,#0f172a)] p-4 md:p-6">
        <div className="mb-4 flex flex-wrap items-center gap-2">
          <button onClick={refreshAll} className="rounded-xl border border-slate-800 bg-slate-900 px-3 py-2 text-xs text-slate-300 hover:border-blue-500/40">Refresh API Data</button>
          <label className="cursor-pointer rounded-xl border border-blue-500/30 bg-blue-500/10 px-3 py-2 text-xs text-blue-200 hover:bg-blue-500/20">Upload CloudTrail JSON<input type="file" accept=".json,.gz" className="hidden" onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])} /></label>
          {selectedAlert && <span className="text-xs text-slate-500">Selected alert: {selectedAlert}</span>}
        </div>
        <AnimatePresence mode="wait"><motion.div key={page} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }}>{renderPage()}</motion.div></AnimatePresence>
      </main>
    </div>
    <DetailPanel item={detailItem} onClose={() => setDetailItem(null)} />
  </div>;
}
