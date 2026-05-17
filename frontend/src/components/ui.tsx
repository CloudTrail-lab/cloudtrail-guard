import React from "react";

export function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={`rounded-2xl border border-slate-800 bg-slate-950/70 shadow-2xl shadow-black/20 ${className}`}>{children}</div>;
}

export function Badge({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <span className={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium ${className}`}>{children}</span>;
}

export function Button({ children, className = "", ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button {...props} className={`rounded-xl border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-300 hover:border-blue-500/40 hover:text-white ${className}`}>{children}</button>;
}

export function riskColor(score: number) {
  if (score >= 85) return "text-red-400";
  if (score >= 70) return "text-orange-300";
  if (score >= 40) return "text-yellow-300";
  return "text-emerald-300";
}

export function riskBg(score: number) {
  if (score >= 85) return "bg-red-500/15 border-red-500/35 text-red-200";
  if (score >= 70) return "bg-orange-500/15 border-orange-500/35 text-orange-200";
  if (score >= 40) return "bg-yellow-500/15 border-yellow-500/35 text-yellow-200";
  return "bg-emerald-500/15 border-emerald-500/35 text-emerald-200";
}

export function riskHex(score: number) {
  if (score >= 85) return "#ff4d4f";
  if (score >= 70) return "#faad14";
  if (score >= 40) return "#d4b106";
  return "#52c41a";
}
