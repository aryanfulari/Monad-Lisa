from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pipeline import run_pipeline
from blockchain.blockchain import account
from dashboard.dashboard import get_dashboard_data, get_badges, get_performance_history
from dashboard.leaderboard import get_leaderboard, get_leaderboard_sorted

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard")
def dashboard():
    data = get_dashboard_data(account.address)
    return {"data": data, "address": account.address}

@app.get("/api/badges")
def badges():
    return {"badges": get_badges(account.address)}

@app.get("/api/history")
def history():
    return {"history": get_performance_history(account.address)}

@app.get("/api/leaderboard")
def leaderboard():
    sorted_data = get_leaderboard_sorted(account.address)
    return {"leaderboard": [{"Model": k, "Tasks Completed": v["count"], "Average Score": v["avg_score"]} for k, v in sorted_data]}

class PipelineRequest(BaseModel):
    task: str
    model: str

@app.post("/api/run-pipeline")
def run_pipe(req: PipelineRequest):
    result = run_pipeline(req.task, req.model)
    return result
