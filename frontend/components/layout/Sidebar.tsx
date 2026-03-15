'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  Upload,
  BrainCircuit,
  MessageSquareText,
  FileBarChart,
  Settings,
  Zap,
  Sparkles,
} from 'lucide-react';

const nav = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/insights', label: 'AI Insights', icon: Sparkles },
  { href: '/upload', label: 'Upload Data', icon: Upload },
  { href: '/analysis', label: 'AI Analysis', icon: BrainCircuit },
  { href: '/chat', label: 'Chat Analytics', icon: MessageSquareText },
  { href: '/reports', label: 'Reports', icon: FileBarChart },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-fin-border bg-fin-surface flex flex-col">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-fin-border">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center">
          <Zap className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight text-gradient">FinAI</h1>
          <p className="text-[10px] uppercase tracking-widest text-fin-muted">Intelligence Platform</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {nav.map((item) => {
          const active = pathname === item.href || pathname?.startsWith(item.href + '/');
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                active
                  ? 'bg-fin-accent/10 text-fin-accent glow-accent'
                  : 'text-fin-muted hover:text-fin-text hover:bg-fin-hover'
              )}
            >
              <item.icon className={cn('w-[18px] h-[18px]', active && 'text-fin-accent')} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-fin-border">
        <div className="flex items-center gap-2 text-xs text-fin-muted">
          <div className="w-2 h-2 rounded-full bg-fin-success animate-pulse" />
          <span>7 AI Agents Online</span>
        </div>
        <p className="text-[10px] text-fin-muted/60 mt-1">John Keells Holdings PLC</p>
      </div>
    </aside>
  );
}
