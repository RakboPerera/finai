'use client';
import { cn } from '@/lib/utils';
import { BrainCircuit, CheckCircle2, Loader2, AlertCircle, Play } from 'lucide-react';
import Button from '@/components/ui/Button';

interface AgentCardProps {
  name: string;
  description: string;
  status: 'idle' | 'running' | 'success' | 'error';
  onRun?: () => void;
  result?: any;
}

const statusConfig = {
  idle: { icon: BrainCircuit, color: 'text-fin-muted', bg: 'bg-fin-muted/10', label: 'Ready' },
  running: { icon: Loader2, color: 'text-fin-accent', bg: 'bg-fin-accent/10', label: 'Running...' },
  success: { icon: CheckCircle2, color: 'text-fin-success', bg: 'bg-fin-success/10', label: 'Complete' },
  error: { icon: AlertCircle, color: 'text-fin-danger', bg: 'bg-fin-danger/10', label: 'Error' },
};

const agentLabels: Record<string, string> = {
  data_ingestion: 'Data Ingestion',
  anomaly_detection: 'Anomaly Detection',
  trend_analysis: 'Trend Analysis',
  forecasting: 'Forecasting',
  report_generator: 'Report Generator',
  chat_analytics: 'Chat Analytics',
  recommendation: 'Recommendations',
};

export default function AgentCard({ name, description, status, onRun, result }: AgentCardProps) {
  const config = statusConfig[status];
  const StatusIcon = config.icon;

  return (
    <div className="glass-card p-5 animate-slide-up hover:border-fin-accent/20 transition-all duration-300">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className={cn('w-9 h-9 rounded-lg flex items-center justify-center', config.bg)}>
            <StatusIcon className={cn('w-5 h-5', config.color, status === 'running' && 'animate-spin')} />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-fin-text">{agentLabels[name] || name}</h3>
            <p className="text-xs text-fin-muted mt-0.5">{description}</p>
          </div>
        </div>
        <span className={cn('text-[10px] font-semibold uppercase tracking-wider px-2 py-1 rounded-full', config.bg, config.color)}>
          {config.label}
        </span>
      </div>

      {result && status === 'success' && (
        <div className="mt-3 p-3 rounded-lg bg-fin-bg/50 border border-fin-border/50 max-h-32 overflow-y-auto">
          <pre className="text-xs text-fin-muted font-mono whitespace-pre-wrap">
            {typeof result === 'string' ? result : JSON.stringify(result, null, 2).slice(0, 500)}
          </pre>
        </div>
      )}

      {status === 'idle' && onRun && (
        <Button variant="secondary" size="sm" onClick={onRun} icon={<Play className="w-3 h-3" />} className="mt-3 w-full">
          Run Agent
        </Button>
      )}
    </div>
  );
}
