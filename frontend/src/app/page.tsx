'use client';
import { useState, useEffect } from 'react';

const MODELS = [
    { label: "Gemini 2.5 Flash", value: "gemini-2.5-flash" },
    { label: "Gemini 2.5 Pro", value: "gemini-2.5-pro" },
    { label: "Gemini 3.5 Flash", value: "gemini-3.5-flash" },
    { label: "Gemini 2.0 Flash", value: "gemini-2.0-flash" },
    { label: "Gemini 2.0 Flash Lite", value: "gemini-2.0-flash-lite" },
];

export default function Home() {
  const [dashboard, setDashboard] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [badges, setBadges] = useState<any[]>([]);
  const [history, setHistory] = useState<any[]>([]);

  const [taskInput, setTaskInput] = useState("");
  const [selectedModel, setSelectedModel] = useState(MODELS[0].value);
  const [isRunning, setIsRunning] = useState(false);
  const [runResult, setRunResult] = useState<any>(null);

  const loadData = async () => {
    try {
      const [dashRes, leadRes, badgeRes, histRes] = await Promise.all([
        fetch('/api/dashboard'),
        fetch('/api/leaderboard'),
        fetch('/api/badges'),
        fetch('/api/history'),
      ]);
      const dashData = await dashRes.json();
      const leadData = await leadRes.json();
      const badgeData = await badgeRes.json();
      const histData = await histRes.json();

      setDashboard(dashData.data);
      setLeaderboard(leadData.leaderboard);
      setBadges(badgeData.badges);
      setHistory(histData.history);
    } catch (e) {
      console.error("Failed to load dashboard data", e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunPipeline = async () => {
    if (!taskInput.trim()) return;
    setIsRunning(true);
    setRunResult(null);

    try {
      const res = await fetch('/api/run-pipeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: taskInput, model: selectedModel })
      });
      const data = await res.json();
      setRunResult(data);
      if (data.success) {
        await loadData(); // Reload data to show new achievement
      }
    } catch (e) {
      console.error(e);
      setRunResult({ success: false, error: String(e) });
    }
    setIsRunning(false);
  };

  if (!dashboard) {
    return <div className="p-6 text-secondary">Loading AgentPassport Data...</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Header Area */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">AgentPassport</h2>
          <p className="text-secondary text-sm">AI-powered credentials stored permanently on Monad Blockchain.</p>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px'
      }}>
        <StatCard title="Tasks Completed" value={dashboard.tasks_completed} />
        <StatCard title="Average Score" value={dashboard.average_score} />
        <StatCard title="Trust Score" value={dashboard.trust_score} positive={dashboard.trust_score >= 80} />
        <StatCard title="Level" value={dashboard.level} positive />
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '24px'
      }}>
        {/* Pipeline Runner */}
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <h3 className="font-semibold text-lg">Generate & Verify Credential</h3>
          
          <textarea 
            placeholder="Ask the AI to perform any task..." 
            value={taskInput}
            onChange={(e) => setTaskInput(e.target.value)}
            style={{
              width: '100%',
              height: '100px',
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              padding: '12px',
              borderRadius: 'var(--radius-md)',
              resize: 'vertical',
              fontFamily: 'inherit'
            }}
          />

          <select 
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            style={{
              width: '100%',
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              padding: '12px',
              borderRadius: 'var(--radius-md)',
              fontFamily: 'inherit'
            }}
          >
            {MODELS.map(m => (
              <option key={m.value} value={m.value}>{m.label}</option>
            ))}
          </select>

          <button 
            onClick={handleRunPipeline}
            disabled={isRunning || !taskInput.trim()}
            style={{
              background: isRunning ? 'var(--bg-tertiary)' : 'var(--accent-primary)',
              color: 'white',
              padding: '12px',
              borderRadius: 'var(--radius-md)',
              fontWeight: 'bold',
              border: 'none',
              cursor: isRunning ? 'not-allowed' : 'pointer'
            }}
          >
            {isRunning ? 'Running Workflow...' : 'Generate & Verify'}
          </button>

          {/* Result Area */}
          {runResult && (
            <div style={{ marginTop: '16px', padding: '16px', borderRadius: 'var(--radius-md)', background: 'var(--bg-primary)', border: '1px solid var(--border-color)' }}>
              {runResult.success ? (
                <>
                  <div className="text-sm font-semibold mb-2" style={{ color: 'var(--success)' }}>Credential generated and verified!</div>
                  
                  <div style={{ marginBottom: '16px' }}>
                    <div className="text-xs font-semibold mb-1">Worker Agent Output:</div>
                    <div style={{ background: 'var(--bg-tertiary)', padding: '12px', borderRadius: 'var(--radius-md)', fontSize: '0.875rem', whiteSpace: 'pre-wrap' }}>
                      {runResult.output}
                    </div>
                  </div>

                  <div className="text-xs text-secondary mb-2">Judge Score: <strong style={{ color: 'var(--text-primary)'}}>{runResult.score}/100</strong></div>
                  <div className="text-xs text-secondary mb-4"><strong>Judge Feedback:</strong> {runResult.feedback}</div>
                  
                  <a href={`https://testnet.monadvision.com/tx/0x${runResult.tx_hash}`} target="_blank" rel="noreferrer" style={{ fontSize: '0.875rem' }}>
                    View on Monad Explorer
                  </a>
                </>
              ) : (
                <div style={{ color: 'var(--error)' }}>
                  Error: {runResult.error}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Badges Grid */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3 className="font-semibold mb-4 text-lg">Badges</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
            {badges.map((badge, i) => (
              <div key={i} style={{
                background: badge.earned ? 'var(--accent-glow)' : 'var(--bg-primary)',
                border: '1px solid',
                borderColor: badge.earned ? 'var(--accent-primary)' : 'var(--border-color)',
                padding: '12px',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '8px',
                opacity: badge.earned ? 1 : 0.5
              }}>
                <div style={{ fontSize: '2rem' }}>{badge.icon}</div>
                <div className="text-sm font-medium">{badge.name}</div>
                <div className="text-xs" style={{ color: badge.earned ? 'var(--success)' : 'var(--text-secondary)' }}>
                  {badge.earned ? 'Earned' : 'Locked'}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
        gap: '24px'
      }}>
        {/* Performance History */}
        <div className="glass-panel" style={{ padding: '20px', minHeight: '300px' }}>
          <h3 className="font-semibold mb-4 text-lg">Performance History</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {history.length > 0 ? history.map((item, i) => (
              <ActivityRow key={i} task={item.Task} score={item.Score} time={`${item.Date} ${item.Time}`} />
            )) : (
              <div className="text-secondary text-sm">No history yet.</div>
            )}
          </div>
        </div>

        {/* Leaderboard */}
        <div className="glass-panel" style={{ padding: '20px', minHeight: '300px' }}>
          <h3 className="font-semibold mb-4 text-lg">Model Leaderboard</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {leaderboard.length > 0 ? leaderboard.map((item, i) => (
              <StatusRow key={i} label={item.Model} status={`${item['Average Score']} avg`} color={i === 0 ? 'var(--warning)' : 'var(--accent-primary)'} />
            )) : (
              <div className="text-secondary text-sm">No data yet.</div>
            )}
          </div>
        </div>
      </div>
      
    </div>
  );
}

function StatCard({ title, value, positive = true }: { title: string, value: string | number, positive?: boolean }) {
  return (
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
      <span className="text-secondary text-sm font-medium">{title}</span>
      <div className="flex items-center gap-4">
        <span className="text-2xl font-bold" style={{ color: positive ? 'inherit' : 'var(--warning)'}}>{value}</span>
      </div>
    </div>
  );
}

function StatusRow({ label, status, color }: { label: string, status: string, color: string }) {
  return (
    <div className="flex justify-between items-center" style={{ paddingBottom: '8px', borderBottom: '1px solid var(--border-color)' }}>
      <span className="text-sm font-medium">{label}</span>
      <div className="flex items-center gap-2">
        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: color }} />
        <span className="text-sm" style={{ color }}>{status}</span>
      </div>
    </div>
  );
}

function ActivityRow({ task, score, time }: { task: string, score: number, time: string }) {
  return (
    <div className="flex items-start gap-3">
      <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--bg-tertiary)', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 'bold' }}>
        {score}
      </div>
      <div className="flex flex-col">
        <span className="text-sm">{task.length > 60 ? task.substring(0, 60) + '...' : task}</span>
        <span className="text-xs text-secondary">{time}</span>
      </div>
    </div>
  );
}
