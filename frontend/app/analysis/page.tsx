'use client';
import { useEffect, useState } from 'react';
import TopBar from '@/components/layout/TopBar';
import AgentCard from '@/components/agents/AgentCard';
import Button from '@/components/ui/Button';
import Chart from '@/components/charts/Chart';
import { api } from '@/lib/api';
import { Play, Zap } from 'lucide-react';

const AGENT_DESCRIPTIONS: Record<string, string> = {
  data_ingestion: 'Parses SAP Excel files, cleans and normalizes financial data',
  anomaly_detection: 'Flags unusual transactions, outliers, and irregular patterns',
  trend_analysis: 'Identifies revenue/expense trends and seasonal patterns',
  forecasting: 'Generates predictions with optimistic/base/pessimistic scenarios',
  report_generator: 'Creates executive summaries and KPI dashboards',
  chat_analytics: 'Natural language Q&A on your financial data',
  recommendation: 'Generates actionable financial insights and strategic advice',
};

export default function AnalysisPage() {
  const [uploads, setUploads] = useState<any[]>([]);
  const [selectedUpload, setSelectedUpload] = useState('');
  const [agentStatuses, setAgentStatuses] = useState<Record<string, string>>({});
  const [agentResults, setAgentResults] = useState<Record<string, any>>({});
  const [pipelineRunning, setPipelineRunning] = useState(false);

  useEffect(() => {
    api.getUploads().then((res) => {
      const data = res.data || [];
      setUploads(data);
      if (data.length > 0) setSelectedUpload(data[0].upload_id);
    }).catch(() => {});
  }, []);

  const runSingleAgent = async (agentName: string) => {
    if (!selectedUpload) return;
    setAgentStatuses((s) => ({ ...s, [agentName]: 'running' }));
    try {
      const res = await api.runAgent(agentName, selectedUpload);
      setAgentStatuses((s) => ({ ...s, [agentName]: 'success' }));
      setAgentResults((r) => ({ ...r, [agentName]: res.data }));
    } catch {
      setAgentStatuses((s) => ({ ...s, [agentName]: 'error' }));
    }
  };

  const runFullPipeline = async () => {
    if (!selectedUpload) return;
    setPipelineRunning(true);
    const agents = ['data_ingestion', 'anomaly_detection', 'trend_analysis', 'forecasting', 'report_generator', 'recommendation'];
    for (const agent of agents) {
      await runSingleAgent(agent);
    }
    setPipelineRunning(false);
  };

  // Build a result chart if we have trend or forecast data
  const trendResult = agentResults.trend_analysis;
  const trendChart = trendResult?.chart_data ? {
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 30, bottom: 30 },
    xAxis: { type: 'category', data: trendResult.chart_data.labels || [] },
    yAxis: { type: 'value' },
    series: (trendResult.chart_data.datasets || []).map((ds: any) => ({
      name: ds.label || 'Data',
      type: 'line',
      smooth: true,
      data: ds.data || [],
      lineStyle: { width: 2 },
      areaStyle: { opacity: 0.1 },
    })),
  } : null;

  return (
    <div>
      <TopBar title="AI Analysis" />
      <div className="p-6 space-y-6">
        {/* Upload Selector + Pipeline Button */}
        <div className="glass-card p-5">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-4">
              <label className="text-sm text-fin-muted">Dataset:</label>
              <select
                className="bg-fin-bg border border-fin-border rounded-lg px-3 py-2 text-sm text-fin-text focus:outline-none focus:border-fin-accent/50"
                value={selectedUpload}
                onChange={(e) => setSelectedUpload(e.target.value)}
              >
                {uploads.length === 0 && <option value="">No uploads — upload data first</option>}
                {uploads.map((u) => (
                  <option key={u.upload_id} value={u.upload_id}>{u.filename} ({u.upload_id})</option>
                ))}
              </select>
            </div>
            <Button
              variant="primary"
              onClick={runFullPipeline}
              loading={pipelineRunning}
              disabled={!selectedUpload}
              icon={<Zap className="w-4 h-4" />}
            >
              Run Full Pipeline
            </Button>
          </div>
        </div>

        {/* Agent Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(AGENT_DESCRIPTIONS).map(([name, desc]) => (
            <AgentCard
              key={name}
              name={name}
              description={desc}
              status={(agentStatuses[name] as any) || 'idle'}
              onRun={() => runSingleAgent(name)}
              result={agentResults[name]}
            />
          ))}
        </div>

        {/* Results Visualization */}
        {trendChart && (
          <div className="glass-card p-5 animate-slide-up">
            <h3 className="text-sm font-semibold text-fin-text mb-4">Trend Analysis Results</h3>
            <Chart option={trendChart} height="300px" />
          </div>
        )}

        {/* Report Summary */}
        {agentResults.report_generator && (
          <div className="glass-card p-5 animate-slide-up">
            <h3 className="text-sm font-semibold text-fin-text mb-3">Executive Report</h3>
            {agentResults.report_generator.executive_summary && (
              <p className="text-sm text-fin-muted leading-relaxed">{agentResults.report_generator.executive_summary}</p>
            )}
            {agentResults.report_generator.kpis && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
                {agentResults.report_generator.kpis.slice(0, 4).map((kpi: any, i: number) => (
                  <div key={i} className="p-3 rounded-lg bg-fin-bg/50 border border-fin-border/30">
                    <p className="text-[10px] uppercase text-fin-muted tracking-wider">{kpi.name}</p>
                    <p className="text-lg font-bold text-fin-text mt-1">{kpi.value}</p>
                    {kpi.change_pct != null && (
                      <p className={`text-xs font-semibold ${kpi.status === 'up' ? 'text-fin-success' : 'text-fin-danger'}`}>
                        {kpi.status === 'up' ? '↑' : '↓'} {kpi.change_pct}%
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Recommendations */}
        {agentResults.recommendation?.recommendations && (
          <div className="glass-card p-5 animate-slide-up">
            <h3 className="text-sm font-semibold text-fin-text mb-3">AI Recommendations</h3>
            <div className="space-y-3">
              {agentResults.recommendation.recommendations.slice(0, 5).map((rec: any, i: number) => (
                <div key={i} className="p-4 rounded-lg bg-fin-bg/50 border border-fin-border/30">
                  <div className="flex items-start justify-between">
                    <h4 className="text-sm font-semibold text-fin-text">{rec.title}</h4>
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                      rec.urgency === 'high' ? 'bg-fin-danger/10 text-fin-danger' : rec.urgency === 'medium' ? 'bg-fin-warning/10 text-fin-warning' : 'bg-fin-success/10 text-fin-success'
                    }`}>{rec.urgency}</span>
                  </div>
                  <p className="text-xs text-fin-muted mt-1">{rec.description}</p>
                  <div className="flex items-center gap-4 mt-2 text-xs text-fin-muted">
                    <span>Impact: {rec.impact}/10</span>
                    <span>Effort: {rec.effort}/10</span>
                    {rec.estimated_value && <span className="text-fin-accent">{rec.estimated_value}</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
