'use client';
import { useEffect, useState } from 'react';
import TopBar from '@/components/layout/TopBar';
import StatCard from '@/components/ui/StatCard';
import { PageLoader } from '@/components/ui/Loading';
import Chart from '@/components/charts/Chart';
import { api } from '@/lib/api';
import { Database, FileBarChart, BrainCircuit, MessageSquareText, Upload, Clock } from 'lucide-react';
import { timeAgo } from '@/lib/utils';
import Link from 'next/link';

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDashboardStats()
      .then((res) => setStats(res.data))
      .catch(() => setStats(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <PageLoader message="Loading dashboard..." />;

  const s = stats || { total_uploads: 0, total_rows: 0, total_analyses: 0, total_chats: 0, recent_uploads: [], agents_available: 7 };

  // Demo chart data for when there's no data yet
  const overviewChart = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['Revenue', 'Expenses'] },
    grid: { left: 50, right: 20, top: 40, bottom: 30 },
    xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] },
    yAxis: { type: 'value' },
    series: [
      { name: 'Revenue', type: 'line', smooth: true, data: [420, 480, 460, 530, 510, 580], lineStyle: { color: '#22d3ee', width: 2 }, areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(34,211,238,0.2)' }, { offset: 1, color: 'rgba(34,211,238,0)' }] } }, itemStyle: { color: '#22d3ee' } },
      { name: 'Expenses', type: 'line', smooth: true, data: [310, 340, 350, 370, 380, 360], lineStyle: { color: '#a78bfa', width: 2 }, areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(167,139,250,0.15)' }, { offset: 1, color: 'rgba(167,139,250,0)' }] } }, itemStyle: { color: '#a78bfa' } },
    ],
  };

  const agentPieChart = {
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: ['45%', '70%'], center: ['50%', '50%'],
      label: { color: '#8896ab', fontSize: 11 },
      data: [
        { value: 1, name: 'Ingestion', itemStyle: { color: '#22d3ee' } },
        { value: 1, name: 'Anomaly', itemStyle: { color: '#f87171' } },
        { value: 1, name: 'Trends', itemStyle: { color: '#34d399' } },
        { value: 1, name: 'Forecast', itemStyle: { color: '#fbbf24' } },
        { value: 1, name: 'Reports', itemStyle: { color: '#a78bfa' } },
        { value: 1, name: 'Chat', itemStyle: { color: '#60a5fa' } },
        { value: 1, name: 'Recommend', itemStyle: { color: '#fb923c' } },
      ],
    }],
  };

  return (
    <div>
      <TopBar title="Dashboard" />
      <div className="p-6 space-y-6">
        {/* Welcome */}
        <div className="glass-card p-6 glow-accent">
          <h2 className="text-xl font-bold text-fin-text">Welcome to <span className="text-gradient">FinAI</span></h2>
          <p className="text-sm text-fin-muted mt-1">
            Financial Intelligence Platform — Upload SAP Excel data to activate AI-powered analytics.
          </p>
          {s.total_uploads === 0 && (
            <Link href="/upload" className="inline-flex items-center gap-2 mt-4 px-4 py-2 bg-fin-accent text-fin-bg rounded-lg text-sm font-semibold hover:bg-cyan-300 transition-colors">
              <Upload className="w-4 h-4" /> Upload Your First File
            </Link>
          )}
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard title="Files Uploaded" value={s.total_uploads} icon={Database} color="cyan" subtitle={`${s.total_rows.toLocaleString()} total rows`} />
          <StatCard title="Analyses Run" value={s.total_analyses} icon={BrainCircuit} color="purple" subtitle="Across all agents" />
          <StatCard title="Chat Messages" value={s.total_chats} icon={MessageSquareText} color="green" subtitle="Q&A interactions" />
          <StatCard title="AI Agents" value={s.agents_available} icon={FileBarChart} color="amber" subtitle="All systems online" />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 glass-card p-5">
            <h3 className="text-sm font-semibold text-fin-text mb-4">Financial Overview</h3>
            <Chart option={overviewChart} height="280px" />
            {s.total_uploads === 0 && (
              <p className="text-xs text-fin-muted text-center mt-2">Sample data shown — upload files for real analytics</p>
            )}
          </div>
          <div className="glass-card p-5">
            <h3 className="text-sm font-semibold text-fin-text mb-4">AI Agent Distribution</h3>
            <Chart option={agentPieChart} height="280px" />
          </div>
        </div>

        {/* Recent Uploads */}
        <div className="glass-card p-5">
          <h3 className="text-sm font-semibold text-fin-text mb-4">Recent Uploads</h3>
          {s.recent_uploads.length === 0 ? (
            <p className="text-sm text-fin-muted py-6 text-center">No files uploaded yet. Head to Upload Data to get started.</p>
          ) : (
            <div className="space-y-2">
              {s.recent_uploads.map((u: any) => (
                <div key={u.upload_id} className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50 border border-fin-border/30">
                  <div className="flex items-center gap-3">
                    <Database className="w-4 h-4 text-fin-accent" />
                    <div>
                      <p className="text-sm text-fin-text">{u.filename}</p>
                      <p className="text-xs text-fin-muted">{u.total_rows} rows • {u.sheets?.length || 0} sheets</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-fin-muted">
                    <Clock className="w-3 h-3" />
                    {u._created_at ? timeAgo(u._created_at) : 'recently'}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
