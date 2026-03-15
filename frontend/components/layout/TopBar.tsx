'use client';
import { Search, Bell } from 'lucide-react';

export default function TopBar({ title }: { title?: string }) {
  return (
    <header className="sticky top-0 z-30 h-14 border-b border-fin-border bg-fin-bg/80 backdrop-blur-md flex items-center justify-between px-6">
      <h2 className="text-base font-semibold text-fin-text">{title || 'Dashboard'}</h2>
      <div className="flex items-center gap-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-fin-muted" />
          <input
            type="text"
            placeholder="Search data, reports..."
            className="w-64 bg-fin-surface border border-fin-border rounded-lg pl-9 pr-4 py-1.5 text-sm text-fin-text placeholder:text-fin-muted/50 focus:outline-none focus:border-fin-accent/50 transition-colors"
          />
        </div>
        <button className="relative p-2 rounded-lg hover:bg-fin-hover transition-colors">
          <Bell className="w-4 h-4 text-fin-muted" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-fin-accent" />
        </button>
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-fin-accent to-fin-purple flex items-center justify-center text-xs font-bold text-white">
          RB
        </div>
      </div>
    </header>
  );
}
