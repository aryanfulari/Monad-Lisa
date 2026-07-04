'use client';
import { useEffect, useState } from 'react';

export default function TopBar() {
  const [address, setAddress] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/dashboard')
      .then(r => r.json())
      .then(data => {
        setAddress(data.address);
      })
      .catch(e => console.error(e));
  }, []);

  return (
    <header className="glass-panel" style={{
      height: '64px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 24px',
      borderTop: 'none',
      borderLeft: 'none',
      borderRight: 'none',
      borderBottom: '1px solid var(--border-light)',
      borderRadius: 0,
      position: 'sticky',
      top: 0,
      zIndex: 9
    }}>
      <div className="flex items-center gap-4">
        <h1 className="text-lg font-semibold">AgentPassport Overview</h1>
      </div>
      
      <div className="flex items-center gap-4">
        <div style={{
          background: 'var(--bg-primary)',
          border: '1px solid var(--border-color)',
          padding: '8px 16px',
          borderRadius: 'var(--radius-full)',
          color: 'var(--text-secondary)',
          fontSize: '0.875rem',
          fontFamily: 'monospace'
        }}>
          Wallet: {address || "Loading..."}
        </div>
      </div>
    </header>
  );
}
