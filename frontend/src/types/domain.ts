export type AlertStatus = "new" | "in_progress" | "resolved";

export type Evidence = {
  feature: string;
  value: string;
  importance: number;
};

export type NormalizedEvent = {
  eventID: string;
  eventName: string;
  eventTime: string;
  userIdentity: Record<string, any>;
  principal: string;
  sourceIPAddress: string;
  userAgent: string;
  awsRegion: string;
  eventSource: string;
  eventStatus: "Success" | "Error";
  risk_score: number;
  risk_level: string;
  requestParameters?: Record<string, any> | null;
  responseElements?: any;
  anomaly_reason?: string | null;
  raw?: Record<string, any>;
};

export type Alert = {
  alert_id: string;
  user_id: string;
  detection_method: "rule" | "ai";
  rule_id?: string;
  rule_name?: string;
  risk_score: number;
  status: AlertStatus;
  detected_at: string;
  summary: string;
  related_events: string[];
  evidence: Evidence[];
  suppressed?: boolean;
};

export type DashboardSummary = {
  risk_score: { current: number; previous: number; trend: string };
  risk_trend: Array<{ time: string; risk: number; events: number }>;
  event_histogram: Array<{ time: string; count: number }>;
  top_anomalies: Alert[];
  signal_distribution: Array<{ service: string; value: number }>;
  totals: { events: number; alerts: number; principals: number; source_ips: number };
};

export type TimelineEvent = {
  id: string;
  time: string;
  timestamp: string;
  event_name: string;
  status: string;
  risk_score: number;
  is_anomaly: boolean;
  stage: string;
  anomaly_reason?: string | null;
};

export type AttackGraph = {
  alert_id: string;
  nodes: Array<{ id: string; type: string; label: string; risk_score: number; arn?: string | null }>;
  edges: Array<{ source: string; target: string; action: string; timestamp: string; risk: string; event_id: string }>;
  kill_chain: Array<{ stage: string; events: string[]; timestamp: string; description: string; risk: string }>;
};
