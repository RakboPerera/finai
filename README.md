# FinAI — Financial Intelligence Platform
## John Keells Holdings PLC

> SAP Excel → 7 Claude AI Agents → Interactive Dashboards + Chat Analytics

### Architecture
- **Frontend**: Next.js 14 (App Router) + ECharts + Tailwind CSS
- **Backend**: Python FastAPI + DuckDB
- **AI Engine**: 7 Specialized Claude AI Agents
- **Storage**: JSON file store + DuckDB (no Docker/PostgreSQL required)

### Quick Setup (Windows CMD)

```cmd
cd "C:\Users\rakbop\OneDrive - John Keells Holdings PLC\Claude presentations\IAP"

:: 1. Backend setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

:: 2. Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### AI Agents
1. **Data Ingestion Agent** — Parses SAP Excel files, cleans & normalizes
2. **Anomaly Detection Agent** — Flags unusual transactions & patterns
3. **Trend Analysis Agent** — Identifies financial trends & seasonality
4. **Forecasting Agent** — Revenue/expense predictions
5. **Report Generator Agent** — Creates executive summaries
6. **Chat Analytics Agent** — Natural language Q&A on financial data
7. **Recommendation Agent** — Actionable financial insights
