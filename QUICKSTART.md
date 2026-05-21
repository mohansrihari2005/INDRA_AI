# INDRA AI v2 - Quick Start Guide

## Complete Setup Steps

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**What gets installed:**
- `autogen` - Multi-agent orchestration framework (0.13.0)
- `fastapi` - Backend API framework
- `openai` - OpenAI API client
- `uvicorn` - ASGI server
- All other required packages

### Step 2: Set Environment Variables

#### Option A: Windows PowerShell (Temporary)
```powershell
$env:OPENAI_API_KEY = "sk-your-actual-api-key"
$env:OPENWEATHER_API_KEY = "your-openweather-key"
```

#### Option B: Windows CMD (Temporary)
```cmd
set OPENAI_API_KEY=sk-your-actual-api-key
set OPENWEATHER_API_KEY=your-openweather-key
```

#### Option C: Permanent (Windows - Set System Environment Variables)
```
1. Press Win + X, select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Add new variables:
   - OPENAI_API_KEY = sk-...
   - OPENWEATHER_API_KEY = ...
5. Click OK and restart terminal
```

#### Option D: Create .env file (Easiest)
Create `backend/.env`:
```
OPENAI_API_KEY=sk-your-actual-api-key
OPENWEATHER_API_KEY=your-openweather-key
```

### Step 3: Verify Installation

```bash
cd c:\Mohan\INDRA_AI_v2
python test_autogen_integration.py
```

**Expected output:**
```
✓ PASS: AutoGen Installation
✓ PASS: Agent Imports
✓ PASS: Agent Creation
✓ PASS: Legacy Compatibility
✓ PASS: Coordinator
✓ PASS: Configuration
✓ PASS: Environment Variables

Results: 7/7 tests passed
```

### Step 4: Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**API available at:**
- http://localhost:8000/docs (Interactive API docs)
- http://localhost:8000/redoc (Alternative API docs)

### Step 5: Start Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

**You should see:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

### Step 6: Access the Dashboard

Open your browser: **http://localhost:5173**

You should see the INDRA AI v2 disaster response dashboard.

---

## Testing the System

### Test 1: Legacy Mode (Default - Recommended)

```bash
curl -X POST http://localhost:8000/api/generate/stream \
  -H "Content-Type: application/json" \
  -d '{"place": "Visakhapatnam, Andhra Pradesh"}'
```

**Response:** Real-time disaster analysis (SSE stream)

### Test 2: AutoGen Mode (Optional)

```bash
curl -X POST http://localhost:8000/api/generate/stream \
  -H "Content-Type: application/json" \
  -d '{"place": "Visakhapatnam, Andhra Pradesh", "use_autogen": true}'
```

**Response:** Same analysis, using GroupChat orchestration

### Test 3: Via Dashboard

1. Open http://localhost:5173
2. Enter location: "Visakhapatnam, Andhra Pradesh"
3. Click "Generate"
4. Watch real-time analysis stream
5. View results with alerts, maps, recovery plans

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'autogen'`

**Solution:**
```bash
pip install autogen>=0.2.0,<1.0.0
```

### Issue: `OPENAI_API_KEY is not set`

**Solution:** Set environment variable:
```powershell
$env:OPENAI_API_KEY = "sk-your-key"
```

Or create `.env` file in backend folder.

### Issue: Backend port 8000 already in use

**Solution:** Use different port:
```bash
uvicorn main:app --reload --port 8001
```

Then update frontend API to: `http://localhost:8001`

### Issue: Frontend not connecting to backend

**Solution:** Check CORS in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: `npm: command not found`

**Solution:** Install Node.js:
- Download from https://nodejs.org/
- Install LTS version
- Restart terminal

---

## System Architecture

```
Frontend (React + Vite)
    ↓
http://localhost:5173
    ↓
Backend (FastAPI)
    ↓
http://localhost:8000
    ↓
┌─────────────────────────────────────────────────────┐
│ Coordinator (Orchestrator)                          │
│   ├─ Mode 1: Legacy (default, sequential)          │
│   └─ Mode 2: AutoGen (optional, GroupChat)         │
│       ├─ HazardOfficer (Meteorological analysis)   │
│       ├─ RiskAssessor (Risk calculation)           │
│       ├─ ResourcePlanner (NDRF deployment)        │
│       ├─ EvacuationCoordinator (Alerts)           │
│       └─ RecoveryCoordinator (Recovery planning)   │
└─────────────────────────────────────────────────────┘
    ↓
Data Sources
    ├─ IMD (Meteorological data)
    ├─ OpenWeather API
    ├─ NDRF Database
    └─ Government Schemes
```

---

## Key Features

### 🎯 5 Specialized Agents
1. **HazardOfficer** - Cyclone analysis, warning colors
2. **RiskAssessor** - INDRA formula (wind 40%, surge 35%, rainfall 25%)
3. **ResourcePlanner** - NDRF deployment, logistics
4. **EvacuationCoordinator** - SMS in 5 languages (English, Telugu, Hindi, Odia, Tamil)
5. **RecoveryCoordinator** - 7-day recovery timeline, schemes

### ⚡ Two Execution Modes
- **Legacy** (default): 3-5 seconds, ~2000 tokens
- **AutoGen** (optional): 8-15 seconds, ~3000-4000 tokens, sophisticated reasoning

### 📊 Real-Time Streaming
- Server-Sent Events (SSE) for live updates
- Progressive analysis display
- Real-time alerts

### 🌐 Multilingual Support
- English, Telugu, Hindi, Odia, Tamil
- 160-char SMS format
- Native script support

---

## Next Steps

### For Development
1. Explore agent code: `backend/agents/*.py`
2. Check API docs: http://localhost:8000/docs
3. Read configuration: `backend/autogen_config.py`
4. Review coordinator: `backend/agents/coordinator.py`

### For Deployment
1. Set `use_autogen: False` (default, recommended)
2. Use production API key
3. Deploy backend to server
4. Deploy frontend separately
5. Update CORS if needed

### For Extension
1. Add new agents following factory pattern
2. Update coordinator to include new agents
3. Add UI components for new features
4. Update agent system prompts as needed

---

## Command Reference

```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
$env:OPENAI_API_KEY = "sk-..."
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Terminal 3: Testing
cd c:\Mohan\INDRA_AI_v2
python test_autogen_integration.py

# Terminal 4: API Testing
curl -X POST http://localhost:8000/api/generate/stream \
  -H "Content-Type: application/json" \
  -d '{"place": "Visakhapatnam"}'
```

---

## Support

- **Documentation**: [AUTOGEN_INTEGRATION.md](./AUTOGEN_INTEGRATION.md)
- **Tests**: `python test_autogen_integration.py`
- **API Docs**: http://localhost:8000/docs
- **Source Code**: `backend/agents/`, `frontend/src/`

---

## Success Checklist

- [ ] Python packages installed (`pip install -r requirements.txt`)
- [ ] Environment variables set (OPENAI_API_KEY, OPENWEATHER_API_KEY)
- [ ] Tests passing (`python test_autogen_integration.py` → 7/7)
- [ ] Backend running (`http://localhost:8000/docs` accessible)
- [ ] Frontend running (`http://localhost:5173` accessible)
- [ ] Dashboard displays map and input field
- [ ] Can generate analysis from dashboard
- [ ] Real-time alerts appear in stream

---

**You're all set! 🚀 The system is ready to analyze disasters and generate response plans.**
