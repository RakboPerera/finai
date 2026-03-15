'use client';
import { cn } from '@/lib/utils';
import { Spinner } from './Loading';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
}

export default function Button({
  children, variant = 'primary', size = 'md', loading, icon, className, disabled, ...props
}: ButtonProps) {
  const variants = {
    primary: 'bg-fin-accent text-fin-bg hover:bg-cyan-300 font-semibold shadow-lg shadow-fin-accent/20',
    secondary: 'bg-fin-card border border-fin-border text-fin-text hover:bg-fin-hover',
    ghost: 'text-fin-muted hover:text-fin-text hover:bg-fin-hover',
    danger: 'bg-fin-danger/10 text-fin-danger border border-fin-danger/20 hover:bg-fin-danger/20',
  };
  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-2.5 text-base',
  };

  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <Spinner size="sm" /> : icon}
      {children}
    </button>
  );
}
