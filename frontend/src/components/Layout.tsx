import { Bell, ChevronRight, Clock, Filter, GitBranch, LayoutDashboard, Search, Shield, ShieldAlert, User } from "lucide-react";
import { Badge } from "./ui";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "explorer", label: "Event Explorer", icon: Search },
  { id: "timeline", label: "User Timeline", icon: Clock },
  { id: "detection", label: "Detection Center", icon: ShieldAlert },
  { id: "reconstruction", label: "Attack Reconstruction", icon: GitBranch },
];

export function Header({ openAlerts }: { openAlerts: number }) {
  return (
    <header className="flex h-20 items-center justify-between border-b border-slate-800 bg-slate-950/95 px-6 backdrop-blur">
      <div className="flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-500/15 text-blue-300 ring-1 ring-blue-500/30"><Shield size={24} /></div>
        <div>
          <div className="text-lg font-semibold tracking-tight text-white">CloudTrace-Guard</div>
          <div className="text-xs text-slate-500">CloudTrail Behavior Analytics Console</div>
        </div>
      </div>
      <div className="hidden items-center gap-3 lg:flex">
        <Badge className="border-emerald-500/30 bg-emerald-500/10 text-emerald-200"><span className="mr-2 h-2 w-2 rounded-full bg-emerald-400" /> API Connected</Badge>
        <Badge className="border-slate-700 bg-slate-900 text-slate-300"><Clock size={13} className="mr-2" /> Last 24h</Badge>
        <Badge className="border-red-500/30 bg-red-500/10 text-red-200"><Bell size={13} className="mr-2" /> {openAlerts} New Alerts</Badge>
      </div>
      <div className="flex h-10 w-10 items-center justify-center rounded-full border border-slate-800 bg-slate-900 text-slate-300"><User size={18} /></div>
    </header>
  );
}

export function Sidebar({ page, setPage, query, setQuery, setStatusFilter }: any) {
  return (
    <aside className="hidden w-[280px] shrink-0 border-r border-slate-800 bg-slate-950/80 p-4 lg:block">
      <div className="relative mb-4">
        <Search className="absolute left-3 top-2.5 text-slate-500" size={16} />
        <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search eventName, user, IP..." className="w-full rounded-xl border border-slate-800 bg-slate-900 py-2 pl-9 pr-3 text-sm text-slate-200 outline-none placeholder:text-slate-600 focus:border-blue-500/60" />
      </div>
      <div className="space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = page === item.id;
          return (
            <button key={item.id} onClick={() => setPage(item.id)} className={`flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-left text-sm transition ${active ? "bg-blue-500/15 text-blue-200 ring-1 ring-blue-500/25" : "text-slate-400 hover:bg-slate-900 hover:text-slate-100"}`}>
              <span className="flex items-center gap-3"><Icon size={17} />{item.label}</span>
              {active && <ChevronRight size={16} />}
            </button>
          );
        })}
      </div>
      <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
        <div className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-200"><Filter size={15} /> Quick Filters</div>
        <div className="space-y-2">
          {[["New Alerts", "new"], ["AI Detection", "ai"], ["Critical Risk", "critical"]].map(([label, value]) => (
            <button key={value} onClick={() => { setPage("detection"); setStatusFilter(value); }} className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-left text-xs text-slate-400 hover:border-blue-500/40 hover:text-blue-200">{label}</button>
          ))}
        </div>
      </div>
    </aside>
  );
}
