import type { Metadata } from 'next';
import './globals.css';
import Sidebar from '@/components/layout/Sidebar';

export const metadata: Metadata = {
  title: 'FinAI — Financial Intelligence Platform',
  description: 'AI-powered financial analytics for John Keells Holdings PLC',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="flex-1 ml-64">{children}</main>
        </div>
      </body>
    </html>
  );
}
