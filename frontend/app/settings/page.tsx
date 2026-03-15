'use client';
import TopBar from '@/components/layout/TopBar';
import { Settings, Key, Database, Cpu, Globe } from 'lucide-react';
import Button from '@/components/ui/Button';

export default function SettingsPage() {
  return (
    <div>
      <TopBar title="Settings" />
      <div className="p-6 space-y-6 max-w-3xl">
        {/* API Configuration */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-5">
            <Key className="w-5 h-5 text-fin-accent" />
            <h3 className="text-base font-semibold text-fin-text">API Configuration</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-xs text-fin-muted mb-1.5">Anthropic API Key</label>
              <input
                type="password"
                placeholder="sk-ant-..."
                className="w-full bg-fin-bg border border-fin-border rounded-lg px-4 py-2.5 text-sm text-fin-text placeholder:text-fin-muted/30 focus:outline-none focus:border-fin-accent/50 font-mono"
              />
              <p className="text-[10px] text-fin-muted mt-1">Set in backend/.env file. This field is display-only.</p>
            </div>
            <div>
              <label className="block text-xs text-fin-muted mb-1.5">Claude Model</label>
              <select className="w-full bg-fin-bg border border-fin-border rounded-lg px-4 py-2.5 text-sm text-fin-text focus:outline-none focus:border-fin-accent/50">
                <option>claude-sonnet-4-20250514</option>
                <option>claude-haiku-4-5-20251001</option>
              </select>
            </div>
          </div>
        </div>

        {/* Data Storage */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-5">
            <Database className="w-5 h-5 text-fin-purple" />
            <h3 className="text-base font-semibold text-fin-text">Data Storage</h3>
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50">
              <span className="text-fin-muted">Storage Engine</span>
              <span className="text-fin-text font-medium">DuckDB + JSON File Store</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50">
              <span className="text-fin-muted">Database Path</span>
              <span className="text-fin-accent font-mono text-xs">data/finai.duckdb</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50">
              <span className="text-fin-muted">JSON Store</span>
              <span className="text-fin-accent font-mono text-xs">data/store/*.json</span>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-5">
            <Cpu className="w-5 h-5 text-fin-success" />
            <h3 className="text-base font-semibold text-fin-text">System Information</h3>
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50">
              <span className="text-fin-muted">Frontend</span>
              <span className="text-fin-text">Next.js 14 + Tailwind CSS + ECharts</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50">
              <span className="text-fin-muted">Backend</span>
              <span className="text-fin-text">Python FastAPI</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50">
              <span className="text-fin-muted">AI Engine</span>
              <span className="text-fin-text">7 Claude AI Agents</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-lg bg-fin-bg/50">
              <span className="text-fin-muted">Platform</span>
              <span className="text-fin-text">John Keells Holdings PLC</span>
            </div>
          </div>
        </div>

        {/* Endpoints */}
        <div className="glass-card p-6">
          <div className="flex items-center gap-3 mb-5">
            <Globe className="w-5 h-5 text-fin-warning" />
            <h3 className="text-base font-semibold text-fin-text">API Endpoints</h3>
          </div>
          <div className="space-y-2 font-mono text-xs">
            {[
              ['POST', '/api/data/upload', 'Upload SAP Excel file'],
              ['GET', '/api/data/uploads', 'List all uploads'],
              ['POST', '/api/analysis/run/:agent', 'Run specific agent'],
              ['POST', '/api/analysis/pipeline', 'Run full pipeline'],
              ['GET', '/api/analysis/results/:id', 'Get analysis results'],
              ['POST', '/api/chat/send', 'Send chat message'],
              ['GET', '/api/dashboard/stats', 'Dashboard statistics'],
            ].map(([method, path, desc]) => (
              <div key={path} className="flex items-center gap-3 p-2 rounded bg-fin-bg/50">
                <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${method === 'POST' ? 'bg-fin-accent/10 text-fin-accent' : 'bg-fin-success/10 text-fin-success'}`}>{method}</span>
                <span className="text-fin-text">{path}</span>
                <span className="text-fin-muted ml-auto">{desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
