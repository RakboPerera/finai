'use client';
import { useState, useEffect, useRef } from 'react';
import TopBar from '@/components/layout/TopBar';
import { Spinner } from '@/components/ui/Loading';
import Chart from '@/components/charts/Chart';
import { api } from '@/lib/api';
import { Send, BrainCircuit, User, Sparkles, Trash2 } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  chart?: any;
  followUps?: string[];
}

export default function ChatPage() {
  const [uploads, setUploads] = useState<any[]>([]);
  const [selectedUpload, setSelectedUpload] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.getUploads().then((res) => {
      const data = res.data || [];
      setUploads(data);
      if (data.length > 0) setSelectedUpload(data[0].upload_id);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg || !selectedUpload) return;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: msg }]);
    setLoading(true);

    try {
      const res = await api.sendMessage(selectedUpload, msg);
      const data = res.data;
      const assistantMsg: Message = {
        role: 'assistant',
        content: data.answer || JSON.stringify(data),
        followUps: data.follow_up_questions,
      };

      // If agent suggested a chart
      if (data.chart_suggestion) {
        const cs = data.chart_suggestion;
        assistantMsg.chart = {
          tooltip: { trigger: cs.type === 'pie' ? 'item' : 'axis' },
          xAxis: cs.type !== 'pie' ? { type: 'category', data: cs.data?.labels || [] } : undefined,
          yAxis: cs.type !== 'pie' ? { type: 'value' } : undefined,
          series: cs.type === 'pie'
            ? [{ type: 'pie', radius: ['40%', '65%'], data: cs.data?.values || [] }]
            : [{ type: cs.type || 'bar', data: cs.data?.values || [], itemStyle: { color: '#22d3ee' } }],
        };
      }

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setMessages((prev) => [...prev, { role: 'assistant', content: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    api.clearChat('default').catch(() => {});
  };

  const suggestedQuestions = [
    'What are the top 5 expense categories?',
    'Show me monthly revenue trends',
    'Are there any anomalies in recent transactions?',
    'Compare this quarter vs last quarter',
  ];

  return (
    <div className="flex flex-col h-screen">
      <TopBar title="Chat Analytics" />
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Controls Bar */}
        <div className="px-6 py-3 border-b border-fin-border bg-fin-surface/50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <label className="text-xs text-fin-muted">Dataset:</label>
            <select
              className="bg-fin-bg border border-fin-border rounded-lg px-3 py-1.5 text-xs text-fin-text focus:outline-none focus:border-fin-accent/50"
              value={selectedUpload}
              onChange={(e) => setSelectedUpload(e.target.value)}
            >
              {uploads.length === 0 && <option value="">No uploads</option>}
              {uploads.map((u) => (
                <option key={u.upload_id} value={u.upload_id}>{u.filename}</option>
              ))}
            </select>
          </div>
          <button onClick={clearChat} className="flex items-center gap-1.5 text-xs text-fin-muted hover:text-fin-danger transition-colors">
            <Trash2 className="w-3 h-3" /> Clear Chat
          </button>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full gap-6">
              <div className="w-16 h-16 rounded-2xl bg-fin-accent/10 flex items-center justify-center">
                <Sparkles className="w-8 h-8 text-fin-accent" />
              </div>
              <div className="text-center">
                <h3 className="text-lg font-semibold text-fin-text">Ask anything about your data</h3>
                <p className="text-sm text-fin-muted mt-1">AI-powered financial Q&A with real-time chart generation</p>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg">
                {suggestedQuestions.map((q) => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    className="text-left p-3 rounded-lg border border-fin-border text-xs text-fin-muted hover:border-fin-accent/30 hover:text-fin-text transition-all"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              {msg.role === 'assistant' && (
                <div className="w-7 h-7 rounded-lg bg-fin-accent/10 flex items-center justify-center flex-shrink-0 mt-1">
                  <BrainCircuit className="w-4 h-4 text-fin-accent" />
                </div>
              )}
              <div className={`max-w-[70%] ${msg.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'} px-4 py-3`}>
                <p className="text-sm text-fin-text leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                {msg.chart && (
                  <div className="mt-3 rounded-lg overflow-hidden bg-fin-bg/30">
                    <Chart option={msg.chart} height="200px" />
                  </div>
                )}
                {msg.followUps && msg.followUps.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {msg.followUps.map((q, j) => (
                      <button key={j} onClick={() => sendMessage(q)} className="text-[10px] px-2 py-1 rounded-full border border-fin-accent/20 text-fin-accent hover:bg-fin-accent/10 transition-colors">
                        {q}
                      </button>
                    ))}
                  </div>
                )}
              </div>
              {msg.role === 'user' && (
                <div className="w-7 h-7 rounded-lg bg-fin-purple/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <User className="w-4 h-4 text-fin-purple" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3">
              <div className="w-7 h-7 rounded-lg bg-fin-accent/10 flex items-center justify-center flex-shrink-0">
                <BrainCircuit className="w-4 h-4 text-fin-accent" />
              </div>
              <div className="chat-bubble-ai px-4 py-3">
                <div className="flex items-center gap-2">
                  <Spinner size="sm" />
                  <span className="text-xs text-fin-muted">Analyzing your data...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="px-6 py-4 border-t border-fin-border bg-fin-surface/50">
          <div className="flex items-center gap-3 max-w-4xl mx-auto">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder={selectedUpload ? 'Ask about your financial data...' : 'Upload a file first to start chatting'}
              disabled={!selectedUpload || loading}
              className="flex-1 bg-fin-bg border border-fin-border rounded-xl px-4 py-3 text-sm text-fin-text placeholder:text-fin-muted/40 focus:outline-none focus:border-fin-accent/50 transition-colors disabled:opacity-50"
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || !selectedUpload || loading}
              className="w-10 h-10 rounded-xl bg-fin-accent text-fin-bg flex items-center justify-center hover:bg-cyan-300 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
