/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        fin: {
          bg: '#0a0e17',
          surface: '#111827',
          card: '#1a2234',
          border: '#1e2d45',
          hover: '#243352',
          text: '#e2e8f0',
          muted: '#8896ab',
          accent: '#22d3ee',
          'accent-dim': '#0e7490',
          success: '#34d399',
          warning: '#fbbf24',
          danger: '#f87171',
          purple: '#a78bfa',
        },
      },
      fontFamily: {
        display: ['"DM Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'pulse-glow': 'pulseGlow 2s infinite',
      },
      keyframes: {
        fadeIn: { '0%': { opacity: '0' }, '100%': { opacity: '1' } },
        slideUp: { '0%': { opacity: '0', transform: 'translateY(12px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } },
        pulseGlow: { '0%, 100%': { boxShadow: '0 0 8px rgba(34, 211, 238, 0.3)' }, '50%': { boxShadow: '0 0 20px rgba(34, 211, 238, 0.6)' } },
      },
    },
  },
  plugins: [],
};
