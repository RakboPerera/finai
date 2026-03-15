"""FinAI Insights Dashboard — Auto Installer
Run this from the IAP root folder to add the Insights Dashboard feature.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ===== 1. Create backend agent =====
agent_code = r'''"""Agent 8: Dashboard Builder — Analyzes data and generates dashboard configurations."""
import json
from agents.base import BaseAgent


class DashboardBuilderAgent(BaseAgent):
    name = "dashboard_builder"
    description = "Analyzes uploaded data and auto-configures interactive dashboards"
    system_prompt = """You are an expert data visualization and dashboard architect. Your job is to analyze financial data and generate a complete dashboard configuration with multiple charts and KPIs.

You MUST respond with ONLY valid JSON — no markdown, no explanation, just pure JSON.

The JSON must have this exact structure:
{
  "title": "string - dashboard title",
  "subtitle": "string - brief description",
  "kpis": [
    {"label": "string", "value": "string", "change": "string like +12.5% or -3.2%", "status": "up|down|stable", "icon": "revenue|expense|profit|balance|growth|alert"}
  ],
  "charts": [
    {
      "id": "string - unique id",
      "title": "string - chart title",
      "type": "line|bar|pie|doughnut|area|stacked_bar|scatter|heatmap|gauge|treemap",
      "width": "full|half|third",
      "height": "normal|tall|short",
      "data": {
        "labels": ["array of x-axis labels or category names"],
        "datasets": [
          {
            "name": "string - series name",
            "values": [1, 2, 3],
            "color": "#hex color"
          }
        ]
      },
      "insight": "string - one line AI insight about what this chart reveals"
    }
  ],
  "summary": "string - 2-3 sentence executive summary of the dashboard findings"
}

RULES:
- Generate 4-8 charts that tell a complete financial story
- Use a MIX of chart types — never all the same
- Use real values from the data — never make up numbers
- KPIs should be 4-6 key metrics
- Colors should use this palette: #22d3ee (cyan), #a78bfa (purple), #34d399 (green), #fbbf24 (amber), #f87171 (red), #60a5fa (blue), #fb923c (orange), #e879f9 (pink)
- Each chart should have an insight explaining what it shows
- Make the dashboard tell a story: overview then breakdown then trends then anomalies
"""

    async def run(self, upload_id: str, context: dict = None) -> dict:
        data_context = self._get_data_context(upload_id, limit=500)

        prompt = f"""Analyze this financial dataset and generate a complete dashboard configuration.

DATA:
{data_context}

Generate a JSON dashboard config with:
1. 4-6 KPI cards showing the most important metrics
2. 4-8 charts using different visualization types that tell the financial story
3. Use REAL numbers from the data
4. Mix chart types: at least one line, one bar, one pie/doughnut, and one other type

Respond with ONLY the JSON object — no markdown, no code blocks, no explanation."""

        result_text = self._call_claude(prompt)
        try:
            result = json.loads(result_text)
        except json.JSONDecodeError:
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            if start >= 0 and end > start:
                try:
                    result = json.loads(result_text[start:end])
                except json.JSONDecodeError:
                    result = {"error": "Failed to parse dashboard config", "raw": result_text[:500]}
            else:
                result = {"error": "Failed to parse dashboard config", "raw": result_text[:500]}

        result["agent"] = self.name
        result["upload_id"] = upload_id
        self._save_result(upload_id, result)
        return result
'''

agent_path = os.path.join(BASE, "backend", "agents", "dashboard_builder.py")
with open(agent_path, "w") as f:
    f.write(agent_code)
print(f"[OK] Created {agent_path}")

# ===== 2. Create backend route =====
route_code = '''"""Insights Dashboard routes — auto-generated dashboards."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.dashboard_builder import DashboardBuilderAgent
from services.database import db
from services.store import store
import json

router = APIRouter(prefix="/api/insights", tags=["insights"])


class InsightsRequest(BaseModel):
    upload_id: str


@router.post("/generate")
async def generate_dashboard(request: InsightsRequest):
    """Generate an AI-powered dashboard for the given dataset."""
    agent = DashboardBuilderAgent()
    try:
        result = await agent.run(request.upload_id)
        store.append("dashboards", {
            "upload_id": request.upload_id,
            "config": result
        })
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(500, f"Dashboard generation failed: {str(e)}")


@router.get("/dashboard/{upload_id}")
async def get_dashboard(upload_id: str):
    """Get cached dashboard for an upload, or return empty."""
    dashboards = store.find("dashboards", {"upload_id": upload_id})
    if dashboards:
        latest = dashboards[-1]
        return {"status": "success", "data": latest.get("config", {})}

    df = db.get_analysis_results(upload_id, "dashboard_builder")
    if not df.empty:
        row = df.iloc[0]
        result = row["result"]
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                pass
        return {"status": "success", "data": result}

    return {"status": "success", "data": None}
'''

route_path = os.path.join(BASE, "backend", "routes", "insights.py")
with open(route_path, "w") as f:
    f.write(route_code)
print(f"[OK] Created {route_path}")

# ===== 3. Patch main.py to include insights route =====
main_path = os.path.join(BASE, "backend", "main.py")
with open(main_path, "r") as f:
    main_code = f.read()

if "insights" not in main_code:
    main_code = main_code.replace(
        "from routes import data, analysis, chat, dashboard",
        "from routes import data, analysis, chat, dashboard, insights"
    )
    main_code = main_code.replace(
        "app.include_router(dashboard.router)",
        "app.include_router(dashboard.router)\napp.include_router(insights.router)"
    )
    with open(main_path, "w") as f:
        f.write(main_code)
    print(f"[OK] Patched {main_path}")
else:
    print(f"[SKIP] {main_path} already has insights route")

# ===== 4. Create frontend insights page =====
insights_dir = os.path.join(BASE, "frontend", "app", "insights")
os.makedirs(insights_dir, exist_ok=True)

page_code = r""""use client";
import { useState, useEffect } from "react";
import TopBar from "@/components/layout/TopBar";
import { Spinner, PageLoader } from "@/components/ui/Loading";
import Button from "@/components/ui/Button";
import Chart from "@/components/charts/Chart";
import { api } from "@/lib/api";
import {
  Sparkles, TrendingUp, TrendingDown, Minus, DollarSign,
  BarChart3, Activity, Wallet, AlertTriangle, RefreshCcw,
} from "lucide-react";
import { cn } from "@/lib/utils";

const iconMap = { revenue: DollarSign, expense: Wallet, profit: TrendingUp, balance: BarChart3, growth: Activity, alert: AlertTriangle };
const statusColors = { up: "text-fin-success", down: "text-fin-danger", stable: "text-fin-warning" };
const statusIcons = { up: TrendingUp, down: TrendingDown, stable: Minus };

function buildChartOption(chart) {
  const { type, data } = chart;
  const labels = data?.labels || [];
  const datasets = data?.datasets || [];
  const baseTooltip = { backgroundColor: "#1a2234", borderColor: "#1e2d45", textStyle: { color: "#e2e8f0", fontSize: 12 } };
  const palette = ["#22d3ee","#a78bfa","#34d399","#fbbf24","#f87171","#60a5fa","#fb923c","#e879f9"];

  if (type === "pie" || type === "doughnut") {
    return {
      tooltip: { ...baseTooltip, trigger: "item" },
      series: [{ type: "pie", radius: type === "doughnut" ? ["42%","68%"] : ["0%","68%"], center: ["50%","50%"],
        label: { color: "#8896ab", fontSize: 11 },
        data: labels.map((label, i) => ({ name: label, value: datasets[0]?.values?.[i] || 0, itemStyle: { color: palette[i % 8] } })),
      }],
    };
  }

  if (type === "gauge") {
    return {
      series: [{ type: "gauge", min: 0, max: 100, progress: { show: true, width: 14 },
        axisLine: { lineStyle: { width: 14, color: [[0.3,"#f87171"],[0.7,"#fbbf24"],[1,"#34d399"]] } },
        axisTick: { show: false }, splitLine: { length: 8, lineStyle: { width: 2, color: "#1e2d45" } },
        axisLabel: { distance: 20, color: "#8896ab", fontSize: 11 },
        detail: { valueAnimation: true, fontSize: 22, color: "#e2e8f0", offsetCenter: [0,"70%"] },
        data: [{ value: datasets[0]?.values?.[0] || 0, name: datasets[0]?.name || "" }],
        title: { color: "#8896ab", fontSize: 12, offsetCenter: [0,"90%"] },
      }],
    };
  }

  if (type === "treemap") {
    return {
      tooltip: baseTooltip,
      series: [{ type: "treemap", roam: false, breadcrumb: { show: false }, label: { color: "#e2e8f0", fontSize: 12 },
        data: labels.map((label, i) => ({ name: label, value: datasets[0]?.values?.[i] || 0, itemStyle: { color: palette[i % 8] } })),
      }],
    };
  }

  const isStacked = type === "stacked_bar";
  const chartType = type === "area" || type === "line" ? "line" : type === "scatter" ? "scatter" : "bar";

  return {
    tooltip: { ...baseTooltip, trigger: "axis" },
    legend: datasets.length > 1 ? { data: datasets.map(d => d.name), textStyle: { color: "#8896ab", fontSize: 11 }, top: 0 } : undefined,
    grid: { left: 55, right: 20, top: datasets.length > 1 ? 35 : 15, bottom: 30 },
    xAxis: { type: "category", data: labels, axisLine: { lineStyle: { color: "#1e2d45" } }, axisLabel: { color: "#8896ab", fontSize: 11, rotate: labels.length > 8 ? 30 : 0 } },
    yAxis: { type: "value", axisLine: { lineStyle: { color: "#1e2d45" } }, axisLabel: { color: "#8896ab", fontSize: 11 }, splitLine: { lineStyle: { color: "#1e2d4520" } } },
    series: datasets.map((ds, i) => {
      const color = ds.color || palette[i % 6];
      return {
        name: ds.name || ("Series " + (i+1)), type: chartType, smooth: chartType === "line", data: ds.values || [],
        stack: isStacked ? "total" : undefined, itemStyle: { color },
        lineStyle: chartType === "line" ? { color, width: 2.5 } : undefined,
        areaStyle: (type === "area" || isStacked) ? { color: { type: "linear", x:0, y:0, x2:0, y2:1, colorStops: [{offset:0, color: color+"30"},{offset:1, color: color+"05"}] } } : undefined,
        symbolSize: chartType === "scatter" ? 10 : 4,
      };
    }),
  };
}

export default function InsightsPage() {
  const [uploads, setUploads] = useState([]);
  const [selectedUpload, setSelectedUpload] = useState("");
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    api.getUploads().then((res) => {
      const data = res.data || [];
      setUploads(data);
      if (data.length > 0) setSelectedUpload(data[0].upload_id);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedUpload) {
      setLoading(true);
      fetch("/api/insights/dashboard/" + selectedUpload)
        .then(r => r.json())
        .then(res => { if (res.data) setDashboard(res.data); else setDashboard(null); })
        .catch(() => setDashboard(null))
        .finally(() => setLoading(false));
    }
  }, [selectedUpload]);

  const generateDashboard = async () => {
    if (!selectedUpload) return;
    setGenerating(true);
    try {
      const res = await fetch("/api/insights/generate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ upload_id: selectedUpload }) });
      const data = await res.json();
      if (data.data) setDashboard(data.data);
    } catch (err) { console.error(err); }
    finally { setGenerating(false); }
  };

  const widthClasses = { full: "col-span-1 md:col-span-2 lg:col-span-3", half: "col-span-1 lg:col-span-2", third: "col-span-1" };
  const heightMap = { short: "220px", normal: "300px", tall: "400px" };

  return (
    <div>
      <TopBar title="AI Insights Dashboard" />
      <div className="p-6 space-y-6">
        <div className="glass-card p-5">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div className="flex items-center gap-4">
              <Sparkles className="w-5 h-5 text-fin-accent" />
              <div>
                <h2 className="text-sm font-semibold text-fin-text">AI-Generated Dashboard</h2>
                <p className="text-xs text-fin-muted">Auto-configured visualizations based on your data</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <select className="bg-fin-bg border border-fin-border rounded-lg px-3 py-2 text-sm text-fin-text focus:outline-none focus:border-fin-accent/50" value={selectedUpload} onChange={e => { setSelectedUpload(e.target.value); setDashboard(null); }}>
                {uploads.length === 0 && <option value="">No uploads</option>}
                {uploads.map(u => <option key={u.upload_id} value={u.upload_id}>{u.filename}</option>)}
              </select>
              <Button variant="primary" onClick={generateDashboard} loading={generating} disabled={!selectedUpload} icon={<Sparkles className="w-4 h-4" />}>
                {dashboard ? "Regenerate" : "Generate Dashboard"}
              </Button>
            </div>
          </div>
        </div>

        {loading && <PageLoader message="Loading dashboard..." />}

        {generating && (
          <div className="flex flex-col items-center justify-center py-20 gap-4">
            <div className="relative"><Spinner size="lg" /><Sparkles className="w-5 h-5 text-fin-accent absolute -top-1 -right-1 animate-pulse" /></div>
            <p className="text-sm text-fin-accent animate-pulse">AI is analyzing your data and building the dashboard...</p>
            <p className="text-xs text-fin-muted">This may take 15-30 seconds</p>
          </div>
        )}

        {!loading && !generating && !dashboard && (
          <div className="glass-card p-16 text-center">
            <Sparkles className="w-14 h-14 text-fin-muted/20 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-fin-text">No Dashboard Generated Yet</h3>
            <p className="text-sm text-fin-muted mt-2 max-w-md mx-auto">Select a dataset and click Generate Dashboard. The AI will analyze your data and create a custom dashboard.</p>
          </div>
        )}

        {dashboard && !generating && !dashboard.error && (
          <div className="space-y-6 animate-fade-in">
            <div className="glass-card p-5 glow-accent">
              <h2 className="text-lg font-bold text-gradient">{dashboard.title || "Financial Dashboard"}</h2>
              <p className="text-sm text-fin-muted mt-1">{dashboard.subtitle || ""}</p>
              {dashboard.summary && <p className="text-sm text-fin-text/80 mt-3 leading-relaxed border-t border-fin-border/30 pt-3">{dashboard.summary}</p>}
            </div>

            {dashboard.kpis && dashboard.kpis.length > 0 && (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                {dashboard.kpis.map((kpi, i) => {
                  const Icon = iconMap[kpi.icon] || DollarSign;
                  const StatusIcon = statusIcons[kpi.status] || Minus;
                  const accentColors = ["text-cyan-400","text-purple-400","text-emerald-400","text-amber-400","text-red-400","text-blue-400"];
                  return (
                    <div key={i} className="glass-card p-4 animate-slide-up" style={{ animationDelay: (i*80)+"ms" }}>
                      <div className="flex items-center justify-between mb-2">
                        <Icon className={cn("w-4 h-4", accentColors[i % 6])} />
                        <div className={cn("flex items-center gap-1 text-xs font-semibold", statusColors[kpi.status] || "text-fin-muted")}>
                          <StatusIcon className="w-3 h-3" />{kpi.change}
                        </div>
                      </div>
                      <p className="text-lg font-bold text-fin-text">{kpi.value}</p>
                      <p className="text-[10px] uppercase tracking-wider text-fin-muted mt-1">{kpi.label}</p>
                    </div>
                  );
                })}
              </div>
            )}

            {dashboard.charts && dashboard.charts.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {dashboard.charts.map((chart, i) => (
                  <div key={chart.id || i} className={cn("glass-card p-5 animate-slide-up", widthClasses[chart.width] || "col-span-1")} style={{ animationDelay: ((i+4)*100)+"ms" }}>
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-sm font-semibold text-fin-text">{chart.title}</h3>
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-fin-accent/10 text-fin-accent font-medium">{chart.type}</span>
                    </div>
                    <Chart option={buildChartOption(chart)} height={heightMap[chart.height] || "300px"} />
                    {chart.insight && <p className="text-xs text-fin-muted mt-3 pt-2 border-t border-fin-border/30 italic">{chart.insight}</p>}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {dashboard?.error && (
          <div className="glass-card p-8 text-center border-fin-danger/20">
            <AlertTriangle className="w-10 h-10 text-fin-danger/50 mx-auto mb-3" />
            <p className="text-sm text-fin-danger">{dashboard.error}</p>
            <Button variant="secondary" size="sm" className="mt-4" onClick={generateDashboard} icon={<RefreshCcw className="w-3 h-3" />}>Retry</Button>
          </div>
        )}
      </div>
    </div>
  );
}
"""

page_path = os.path.join(insights_dir, "page.tsx")
with open(page_path, "w") as f:
    f.write(page_code)
print(f"[OK] Created {page_path}")

# ===== 5. Patch Sidebar to add Insights link =====
sidebar_path = os.path.join(BASE, "frontend", "components", "layout", "Sidebar.tsx")
with open(sidebar_path, "r") as f:
    sidebar_code = f.read()

if "/insights" not in sidebar_code:
    # Add Sparkles import
    sidebar_code = sidebar_code.replace(
        "  Zap,",
        "  Zap,\n  Sparkles,"
    )
    # Add nav item after Dashboard
    sidebar_code = sidebar_code.replace(
        "  { href: '/upload', label: 'Upload Data', icon: Upload },",
        "  { href: '/insights', label: 'AI Insights', icon: Sparkles },\n  { href: '/upload', label: 'Upload Data', icon: Upload },"
    )
    with open(sidebar_path, "w") as f:
        f.write(sidebar_code)
    print(f"[OK] Patched {sidebar_path}")
else:
    print(f"[SKIP] {sidebar_path} already has insights link")

print("\n✅ Insights Dashboard installed! Backend will auto-reload. Refresh browser.")
