import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle, X } from "lucide-react";
import { useState } from "react";
import type { Alert, NormalizedEvent } from "../types/domain";
import { Badge, riskBg } from "./ui";

export function DetailPanel({ item, onClose }: { item: Alert | NormalizedEvent | null; onClose: () => void }) {
  const [tab, setTab] = useState("summary");
  const isAlert = !!item && "alert_id" in item;

  return (
    <AnimatePresence>
      {item && (
        <>
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm" />
          <motion.aside initial={{ x: 440 }} animate={{ x: 0 }} exit={{ x: 440 }} transition={{ type: "spring", stiffness: 260, damping: 28 }} className="fixed right-0 top-0 z-50 h-full w-full max-w-[440px] border-l border-slate-800 bg-slate-950 shadow-2xl">
            <div className="flex h-20 items-center justify-between border-b border-slate-800 px-5">
              <div>
                <div className="text-sm font-medium text-slate-100">{isAlert ? "Alert Detail" : "Event Detail"}</div>
                <div className="mt-1 font-mono text-xs text-slate-500">{isAlert ? item.alert_id : item.eventID}</div>
              </div>
              <button onClick={onClose} className="rounded-xl border border-slate-800 bg-slate-900 p-2 text-slate-400 hover:text-white"><X size={18} /></button>
            </div>
            <div className="flex gap-2 border-b border-slate-800 p-4">
              {["summary", "json", "explanation"].map((name) => <button key={name} onClick={() => setTab(name)} className={`rounded-xl px-3 py-2 text-xs font-medium capitalize ${tab === name ? "bg-blue-500/15 text-blue-200" : "text-slate-500 hover:bg-slate-900 hover:text-slate-200"}`}>{name}</button>)}
            </div>
            <div className="h-[calc(100%-136px)] overflow-y-auto p-5">
              {tab === "summary" && isAlert && <AlertSummary alert={item} />}
              {tab === "summary" && !isAlert && <EventSummary event={item as NormalizedEvent} />}
              {tab === "json" && <pre className="overflow-auto rounded-2xl border border-slate-800 bg-slate-900/70 p-4 font-mono text-xs leading-5 text-slate-300">{JSON.stringify(item, null, 2)}</pre>}
              {tab === "explanation" && <Explanation item={item as any} isAlert={isAlert} />}
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}

function AlertSummary({ alert }: { alert: Alert }) {
  return <div className="space-y-4"><Badge className={riskBg(alert.risk_score)}>Risk {alert.risk_score}</Badge><div className="text-lg font-semibold text-slate-50">{alert.user_id}</div><div className="text-sm leading-6 text-slate-400">{alert.summary}</div><Info label="Rule" value={alert.rule_name || alert.rule_id || "unknown"} /><Info label="Related Events" value={alert.related_events.join(", ")} /></div>;
}

function EventSummary({ event }: { event: NormalizedEvent }) {
  return <div className="space-y-4"><div className="flex items-center justify-between"><div className="text-lg font-semibold text-slate-50">{event.eventName}</div><Badge className={riskBg(event.risk_score)}>Risk {event.risk_score}</Badge></div><Info label="Principal" value={event.principal} /><Info label="Source IP" value={event.sourceIPAddress} /><Info label="Region" value={event.awsRegion} /><Info label="User Agent" value={event.userAgent} />{event.anomaly_reason && <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-sm leading-6 text-red-100"><AlertTriangle size={16} className="mb-2" />{event.anomaly_reason}</div>}</div>;
}

function Explanation({ item, isAlert }: { item: any; isAlert: boolean }) {
  const evidence = isAlert ? item.evidence : [
    { feature: "eventName", value: item.eventName, importance: item.risk_score / 100 },
    { feature: "sourceIPAddress", value: item.sourceIPAddress, importance: item.risk_score > 70 ? 0.74 : 0.31 },
    { feature: "userAgent", value: item.userAgent, importance: 0.55 },
  ];
  return <div className="space-y-3">{evidence.map((ev: any) => <div key={ev.feature} className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4"><div className="mb-2 flex items-center justify-between"><div className="text-sm font-medium text-slate-100">{ev.feature}</div><Badge className={riskBg(ev.importance * 100)}>{Math.round(ev.importance * 100)}%</Badge></div><div className="break-words text-sm text-slate-400">{ev.value}</div></div>)}</div>;
}

function Info({ label, value }: { label: string; value: string }) {
  return <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-3"><div className="text-xs text-slate-500">{label}</div><div className="mt-1 break-words font-mono text-xs text-slate-200">{value}</div></div>;
}
