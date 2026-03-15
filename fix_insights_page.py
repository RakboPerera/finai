"""Run this from the IAP folder to fix the insights frontend page."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

page_dir = os.path.join(BASE, "frontend", "app", "insights")
os.makedirs(page_dir, exist_ok=True)

page_code = """'use client';
import { useState, useEffect } from 'react';
import TopBar from '@/components/layout/TopBar';
import { Spinner, PageLoader } from '@/components/ui/Loading';
import Button from '@/components/ui/Button';
import Chart from '@/components/charts/Chart';
import { api } from '@/lib/api';
import {
  Sparkles, TrendingUp, TrendingDown, Minus, DollarSign,
  BarChart3, Activity, Wallet, AlertTriangle, RefreshCcw,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const iconMap: Record<string, any> = {
  revenue: DollarSign, expense: Wallet, profit: TrendingUp,
  balance: BarChart3, growth: Activity, alert: AlertTriangle,
};
const statusColors: Record<string, string> = {
  up: 'text-fin-success', down: 'text-fin-danger', stable: 'text-fin-warning',
};
const statusIcons: Record<string, any> = {
  up: TrendingUp, down: TrendingDown, stable: Minus,
};

const PALETTE = ['#22d3ee','#a78bfa','#34d399','#fbbf24','#f87171','#60a5fa','#fb923c','#e879f9'];

function buildChartOption(chart: any): any {
  const { type, data } = chart;
  if (!data) return {};
  const labels = data.labels || [];
  const datasets = data.datasets || [];
  const baseTooltip = {
    backgroundColor: '#1a2234',
    borderColor: '#1e2d45',
    textStyle: { color: '#e2e8f0', fontSize: 12 },
  };

  if (type === 'pie' || type === 'doughnut') {
    return {
      tooltip: { ...baseTooltip, trigger: 'item' },
      series: [{
        type: 'pie',
        radius: type === 'doughnut' ? ['42%', '68%'] : ['0%', '68%'],
        center: ['50%', '50%'],
        label: { color: '#8896ab', fontSize: 11 },
        data: labels.map((label: string, i: number) => ({
          name: label,
          value: datasets[0]?.values?.[i] || 0,
          itemStyle: { color: PALETTE[i % 8] },
        })),
      }],
    };
  }

  if (type === 'gauge') {
    return {
      series: [{
        type: 'gauge',
        min: 0,
        max: 100,
        progress: { show: true, width: 14 },
        axisLine: { lineStyle: { width: 14, color: [[0.3, '#f87171'], [0.7, '#fbbf24'], [1, '#34d399']] } },
        axisTick: { show: false },
        splitLine: { length: 8, lineStyle: { width: 2, color: '#1e2d45' } },
        axisLabel: { distance: 20, color: '#8896ab', fontSize: 11 },
        detail: { valueAnimation: true, fontSize: 22, color: '#e2e8f0', offsetCenter: [0, '70%'] },
        data: [{ value: datasets[0]?.values?.[0] || 0, name: datasets[0]?.name || '' }],
        title: { color: '#8896ab', fontSize: 12, offsetCenter: [0, '90%'] },
      }],
    };
  }

  if (type === 'treemap') {
    return {
      tooltip: baseTooltip,
      series: [{
        type: 'treemap',
        roam: false,
        breadcrumb: { show: false },
        label: { color: '#e2e8f0', fontSize: 12 },
        data: labels.map((label: string, i: number) => ({
          name: label,
          value: datasets[0]?.values?.[i] || 0,
          itemStyle: { color: PALETTE[i % 8] },
        })),
      }],
    };
  }

  if (type === 'heatmap') {
    const allVals = datasets.flatMap((d: any) => d.values || []);
    return {
      tooltip: baseTooltip,
      grid: { left: 80, right: 20, top: 20, bottom: 40 },
      xAxis: { type: 'category', data: labels, axisLine: { lineStyle: { color: '#1e2d45' } }, axisLabel: { color: '#8896ab' } },
      yAxis: { type: 'category', data: datasets.map((d: any) => d.name), axisLine: { lineStyle: { color: '#1e2d45' } }, axisLabel: { color: '#8896ab' } },
      visualMap: { min: 0, max: Math.max(...allVals, 1), orient: 'horizontal', left: 'center', bottom: 0, inRange: { color: ['#0e7490', '#22d3ee', '#fbbf24', '#f87171'] }, textStyle: { color: '#8896ab' } },
      series: [{
        type: 'heatmap',
        data: datasets.flatMap((d: any, di: number) => (d.values || []).map((v: number, li: number) => [li, di, v])),
        label: { show: true, color: '#e2e8f0', fontSize: 10 },
      }],
    };
  }

  const isStacked = type === 'stacked_bar';
  const chartType = (type === 'area' || type === 'line') ? 'line' : type === 'scatter' ? 'scatter' : 'bar';

  return {
    tooltip: { ...baseTooltip, trigger: 'axis' },
    legend: datasets.length > 1 ? { data: datasets.map((d: any) => d.name), textStyle: { color: '#8896ab', fontSize: 11 }, top: 0 } : undefined,
    grid: { left: 55, right: 20, top: datasets.length > 1 ? 35 : 15, bottom: 30 },
    xAxis: {
      type: 'category',
      data: labels,
      axisLine: { lineStyle: { color: '#1e2d45' } },
      axisLabel: { color: '#8896ab', fontSize: 11, rotate: labels.length > 8 ? 30 : 0 },
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#1e2d45' } },
      axisLabel: { color: '#8896ab', fontSize: 11 },
      splitLine: { lineStyle: { color: '#1e2d4520' } },
    },
    series: datasets.map((ds: any, i: number) => {
      const color = ds.color || PALETTE[i % 6];
      return {
        name: ds.name || 'Series ' + (i + 1),
        type: chartType,
        smooth: chartType === 'line',
        data: ds.values || [],
        stack: isStacked ? 'total' : undefined,
        itemStyle: { color },
        lineStyle: chartType === 'line' ? { color, width: 2.5 } : undefined,
        areaStyle: (type === 'area' || isStacked) ? {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [{ offset: 0, color: color + '30' }, { offset: 1, color: color + '05' }],
          },
        } : undefined,
        symbolSize: chartType === 'scatter' ? 10 : 4,
      };
    }),
  };
}

export default function InsightsPage() {
  const [uploads, setUploads] = useState<any[]>([]);
  const [selectedUpload, setSelectedUpload] = useState('');
  const [dashboard, setDashboard] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

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
      fetch('/api/insights/dashboard/' + selectedUpload)
        .then((r) => r.json())
        .then((res) => {
          if (res.data) setDashboard(res.data);
          else setDashboard(null);
        })
        .catch(() => setDashboard(null))
        .finally(() => setLoading(false));
    }
  }, [selectedUpload]);

  const generateDashboard = async () => {
    if (!selectedUpload) return;
    setGenerating(true);
    try {
      const res = await fetch('/api/insights/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ upload_id: selectedUpload }),
      });
      const data = await res.json();
      if (data.data) setDashboard(data.data);
    } catch (err) {
      console.error('Generation failed:', err);
    } finally {
      setGenerating(false);
    }
  };

  const widthClasses: Record<string, string> = {
    full: 'col-span-1 md:col-span-2 lg:col-span-3',
    half: 'col-span-1 lg:col-span-2',
    third: 'col-span-1',
  };
  const heightMap: Record<string, string> = {
    short: '220px', normal: '300px', tall: '400px',
  };

  return (
    <div>
      <TopBar title="AI Insights Dashboard" />
      <div className="p-6 space-y-6">
        {/* Controls */}
        <div className="glass-card p-5">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-4">
              <Sparkles className="w-5 h-5 text-fin-accent" />
              <div>
                <h2 className="text-sm font-semibold text-fin-text">AI-Generated Dashboard</h2>
                <p className="text-xs text-fin-muted">Auto-configured visualizations based on your data</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <select
                className="bg-fin-bg border border-fin-border rounded-lg px-3 py-2 text-sm text-fin-text focus:outline-none focus:border-fin-accent/50"
                value={selectedUpload}
                onChange={(e) => { setSelectedUpload(e.target.value); setDashboard(null); }}
              >
                {uploads.length === 0 && <option value="">No uploads</option>}
                {uploads.map((u) => (
                  <option key={u.upload_id} value={u.upload_id}>{u.filename}</option>
                ))}
              </select>
              <Button
                variant="primary"
                onClick={generateDashboard}
                loading={generating}
                disabled={!selectedUpload}
                icon={<Sparkles className="w-4 h-4" />}
              >
                {dashboard ? 'Regenerate' : 'Generate Dashboard'}
              </Button>
            </div>
          </div>
        </div>

        {loading && <PageLoader message="Loading dashboard..." />}

        {generating && (
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <div className="relative">
              <Spinner size="lg" />
              <Sparkles className="w-5 h-5 text-fin-accent absolute -top-1 -right-1 animate-pulse" />
            </div>
            <p className="text-sm text-fin-accent animate-pulse">AI is analyzing your data and building the dashboard...</p>
            <p className="text-xs text-fin-muted">This may take 15-30 seconds</p>
          </div>
        )}

        {!loading && !generating && !dashboard && (
          <div className="glass-card p-16 text-center">
            <Sparkles className="w-14 h-14 text-fin-muted/20 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-fin-text">No Dashboard Generated Yet</h3>
            <p className="text-sm text-fin-muted mt-2 max-w-md mx-auto">
              Select a dataset and click Generate Dashboard to create a custom AI-powered dashboard.
            </p>
          </div>
        )}

        {dashboard && !generating && !dashboard.error && (
          <div className="space-y-6 animate-fade-in">
            {/* Title */}
            <div className="glass-card p-5 glow-accent">
              <h2 className="text-lg font-bold text-gradient">{dashboard.title || 'Financial Dashboard'}</h2>
              <p className="text-sm text-fin-muted mt-1">{dashboard.subtitle || ''}</p>
              {dashboard.summary && (
                <p className="text-sm text-fin-text/80 mt-3 leading-relaxed border-t border-fin-border/30 pt-3">{dashboard.summary}</p>
              )}
            </div>

            {/* KPI Cards */}
            {dashboard.kpis && dashboard.kpis.length > 0 && (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                {dashboard.kpis.map((kpi: any, i: number) => {
                  const Icon = iconMap[kpi.icon] || DollarSign;
                  const StatusIcon = statusIcons[kpi.status] || Minus;
                  const accentColors = ['text-cyan-400', 'text-purple-400', 'text-emerald-400', 'text-amber-400', 'text-red-400', 'text-blue-400'];
                  return (
                    <div key={i} className="glass-card p-4 animate-slide-up" style={{ animationDelay: `${i * 80}ms` }}>
                      <div className="flex items-center justify-between mb-2">
                        <Icon className={cn('w-4 h-4', accentColors[i % 6])} />
                        <div className={cn('flex items-center gap-1 text-xs font-semibold', statusColors[kpi.status] || 'text-fin-muted')}>
                          <StatusIcon className="w-3 h-3" />
                          {kpi.change}
                        </div>
                      </div>
                      <p className="text-lg font-bold text-fin-text">{kpi.value}</p>
                      <p className="text-[10px] uppercase tracking-wider text-fin-muted mt-1">{kpi.label}</p>
                    </div>
                  );
                })}
              </div>
            )}

            {/* Charts Grid */}
            {dashboard.charts && dashboard.charts.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {dashboard.charts.map((chart: any, i: number) => {
                  const option = buildChartOption(chart);
                  return (
                    <div
                      key={chart.id || i}
                      className={cn('glass-card p-5 animate-slide-up', widthClasses[chart.width] || 'col-span-1')}
                      style={{ animationDelay: `${(i + 4) * 100}ms` }}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="text-sm font-semibold text-fin-text">{chart.title}</h3>
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-fin-accent/10 text-fin-accent font-medium">{chart.type}</span>
                      </div>
                      <Chart option={option} height={heightMap[chart.height] || '300px'} />
                      {chart.insight && (
                        <p className="text-xs text-fin-muted mt-3 pt-2 border-t border-fin-border/30 italic">
                          {chart.insight}
                        </p>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {dashboard?.error && (
          <div className="glass-card p-8 text-center border-fin-danger/20">
            <AlertTriangle className="w-10 h-10 text-fin-danger/50 mx-auto mb-3" />
            <p className="text-sm text-fin-danger">{dashboard.error}</p>
            <Button variant="secondary" size="sm" className="mt-4" onClick={generateDashboard} icon={<RefreshCcw className="w-3 h-3" />}>
              Retry
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
"""

page_path = os.path.join(page_dir, "page.tsx")
with open(page_path, "w", encoding="utf-8") as f:
    f.write(page_code)
print(f"[OK] Fixed {page_path}")
print("\\nDone! Refresh your browser to see the fix.")
