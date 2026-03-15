'use client';
import { useState, useEffect } from 'react';
import TopBar from '@/components/layout/TopBar';
import { PageLoader } from '@/components/ui/Loading';
import Button from '@/components/ui/Button';
import Chart from '@/components/charts/Chart';
import { api } from '@/lib/api';
import { FileBarChart, Download, RefreshCcw, ChevronDown, ChevronUp } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function ReportsPage() {
  const [uploads, setUploads] = useState<any[]>([]);
  const [selectedUpload, setSelectedUpload] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});

  useEffect(() => {
    api.getUploads().then((res) => {
      const data = res.data || [];
      setUploads(data);
      if (data.length > 0) setSelectedUpload(data[0].upload_id);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedUpload) {
      setLoading(true);
      api.getResults(selectedUpload)
        .then((res) => setResults(res.data || []))
        .catch(() => setResults([]))
        .finally(() => setLoading(false));
    }
  }, [selectedUpload]);

  const agentColors: Record<string, string> = {
    data_ingestion: 'border-l-cyan-400',
    anomaly_detection: 'border-l-red-400',
    trend_analysis: 'border-l-emerald-400',
    forecasting: 'border-l-amber-400',
    report_generator: 'border-l-purple-400',
    recommendation: 'border-l-orange-400',
  };

  const agentLabels: Record<string, string> = {
    data_ingestion: 'Data Ingestion',
    anomaly_detection: 'Anomaly Detection',
    trend_analysis: 'Trend Analysis',
    forecasting: 'Forecasting',
    report_generator: 'Report Generator',
    recommendation: 'Recommendations',
  };

  return (
    <div>
      <TopBar title="Reports" />
      <div className="p-6 space-y-6">
        {/* Controls */}
        <div className="glass-card p-5 flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-4">
            <FileBarChart className="w-5 h-5 text-fin-accent" />
            <select
              className="bg-fin-bg border border-fin-border rounded-lg px-3 py-2 text-sm text-fin-text focus:outline-none focus:border-fin-accent/50"
              value={selectedUpload}
              onChange={(e) => setSelectedUpload(e.target.value)}
            >
              {uploads.length === 0 && <option value="">No uploads</option>}
              {uploads.map((u) => (
                <option key={u.upload_id} value={u.upload_id}>{u.filename}</option>
              ))}
            </select>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="secondary" size="sm" icon={<RefreshCcw className="w-3 h-3" />}
              onClick={() => { setLoading(true); api.getResults(selectedUpload).then((r) => setResults(r.data || [])).finally(() => setLoading(false)); }}>
              Refresh
            </Button>
          </div>
        </div>

        {loading && <PageLoader message="Loading reports..." />}

        {!loading && results.length === 0 && (
          <div className="glass-card p-12 text-center">
            <FileBarChart className="w-12 h-12 text-fin-muted/30 mx-auto mb-4" />
            <h3 className="text-base font-semibold text-fin-text">No reports yet</h3>
            <p className="text-sm text-fin-muted mt-1">Run AI Analysis on your uploaded data to generate reports.</p>
          </div>
        )}

        {/* Report Cards */}
        {!loading && results.map((item, idx) => {
          const result = typeof item.result === 'string' ? (() => { try { return JSON.parse(item.result); } catch { return { raw: item.result }; } })() : item.result;
          const isExpanded = expanded[idx];

          return (
            <div key={idx} className={cn('glass-card border-l-4 overflow-hidden animate-slide-up', agentColors[item.agent_name] || 'border-l-fin-accent')}>
              {/* Header */}
              <button
                className="w-full p-5 flex items-center justify-between hover:bg-fin-hover/20 transition-colors"
                onClick={() => setExpanded((e) => ({ ...e, [idx]: !e[idx] }))}
              >
                <div className="flex items-center gap-3">
                  <h3 className="text-sm font-semibold text-fin-text">{agentLabels[item.agent_name] || item.agent_name}</h3>
                  <span className="text-[10px] text-fin-muted">{item.created_at}</span>
                </div>
                {isExpanded ? <ChevronUp className="w-4 h-4 text-fin-muted" /> : <ChevronDown className="w-4 h-4 text-fin-muted" />}
              </button>

              {/* Content */}
              {isExpanded && (
                <div className="px-5 pb-5 space-y-4">
                  {/* Executive Summary */}
                  {result.executive_summary && (
                    <div className="p-4 rounded-lg bg-fin-bg/50 border border-fin-border/30">
                      <p className="text-xs uppercase tracking-wider text-fin-muted mb-2">Executive Summary</p>
                      <p className="text-sm text-fin-text leading-relaxed">{result.executive_summary}</p>
                    </div>
                  )}

                  {/* Summary or strategic summary */}
                  {result.summary && !result.executive_summary && (
                    <p className="text-sm text-fin-muted leading-relaxed">{result.summary}</p>
                  )}
                  {result.strategic_summary && (
                    <p className="text-sm text-fin-muted leading-relaxed">{result.strategic_summary}</p>
                  )}

                  {/* KPIs */}
                  {result.kpis && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {result.kpis.slice(0, 8).map((kpi: any, i: number) => (
                        <div key={i} className="p-3 rounded-lg bg-fin-bg/50 border border-fin-border/30">
                          <p className="text-[10px] uppercase text-fin-muted tracking-wider">{kpi.name}</p>
                          <p className="text-base font-bold text-fin-text mt-1">{kpi.value}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Anomalies */}
                  {result.anomalies && (
                    <div className="space-y-2">
                      <p className="text-xs uppercase tracking-wider text-fin-muted">Anomalies Found: {result.anomalies.length}</p>
                      {result.anomalies.slice(0, 5).map((a: any, i: number) => (
                        <div key={i} className="p-3 rounded-lg bg-fin-bg/50 border border-fin-border/30 flex items-start gap-2">
                          <span className={cn('text-[10px] px-1.5 py-0.5 rounded font-semibold mt-0.5', {
                            'bg-fin-danger/10 text-fin-danger': a.severity === 'high' || a.severity === 'critical',
                            'bg-fin-warning/10 text-fin-warning': a.severity === 'medium',
                            'bg-fin-success/10 text-fin-success': a.severity === 'low',
                          })}>{a.severity}</span>
                          <p className="text-xs text-fin-text">{a.description}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Recommendations */}
                  {result.recommendations && (
                    <div className="space-y-2">
                      <p className="text-xs uppercase tracking-wider text-fin-muted">Recommendations</p>
                      {result.recommendations.slice(0, 5).map((rec: any, i: number) => (
                        <div key={i} className="p-3 rounded-lg bg-fin-bg/50 border border-fin-border/30">
                          <p className="text-sm font-medium text-fin-text">{rec.title}</p>
                          <p className="text-xs text-fin-muted mt-1">{rec.description}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Chart data */}
                  {result.chart_data && result.chart_data.labels && (
                    <Chart
                      option={{
                        tooltip: { trigger: 'axis' },
                        grid: { left: 50, right: 20, top: 30, bottom: 30 },
                        xAxis: { type: 'category', data: result.chart_data.labels },
                        yAxis: { type: 'value' },
                        series: (result.chart_data.datasets || [{ data: result.chart_data.values || [] }]).map((ds: any) => ({
                          type: 'line', smooth: true, data: ds.data || [], name: ds.label,
                          lineStyle: { width: 2 }, areaStyle: { opacity: 0.08 },
                        })),
                      }}
                      height="250px"
                    />
                  )}

                  {/* Raw JSON fallback */}
                  {!result.executive_summary && !result.summary && !result.anomalies && !result.recommendations && (
                    <pre className="text-xs text-fin-muted font-mono p-3 rounded-lg bg-fin-bg/50 border border-fin-border/30 max-h-64 overflow-y-auto whitespace-pre-wrap">
                      {JSON.stringify(result, null, 2)}
                    </pre>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
