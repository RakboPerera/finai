'use client';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: { value: number; label: string };
  color?: 'cyan' | 'purple' | 'green' | 'amber' | 'red';
}

const colorMap = {
  cyan: 'from-cyan-500/20 to-cyan-500/5 text-cyan-400 border-cyan-500/20',
  purple: 'from-purple-500/20 to-purple-500/5 text-purple-400 border-purple-500/20',
  green: 'from-emerald-500/20 to-emerald-500/5 text-emerald-400 border-emerald-500/20',
  amber: 'from-amber-500/20 to-amber-500/5 text-amber-400 border-amber-500/20',
  red: 'from-red-500/20 to-red-500/5 text-red-400 border-red-500/20',
};

export default function StatCard({ title, value, subtitle, icon: Icon, trend, color = 'cyan' }: StatCardProps) {
  return (
    <div className="glass-card p-5 animate-fade-in group hover:border-fin-accent/30 transition-all duration-300">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-xs font-medium uppercase tracking-wider text-fin-muted">{title}</p>
          <p className="text-2xl font-bold text-fin-text">{value}</p>
          {subtitle && <p className="text-xs text-fin-muted">{subtitle}</p>}
          {trend && (
            <div className="flex items-center gap-1.5">
              <span className={cn('text-xs font-semibold', trend.value >= 0 ? 'text-fin-success' : 'text-fin-danger')}>
                {trend.value >= 0 ? '↑' : '↓'} {Math.abs(trend.value)}%
              </span>
              <span className="text-xs text-fin-muted">{trend.label}</span>
            </div>
          )}
        </div>
        <div className={cn('w-10 h-10 rounded-xl bg-gradient-to-br flex items-center justify-center', colorMap[color])}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
    </div>
  );
}
