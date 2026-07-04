'use client';
import { useState } from 'react';

export default function ChatPanel() {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button 
          onClick={() => setIsOpen(true)}
          className="glass-panel-hover"
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            background: 'var(--accent-primary)',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '24px',
            boxShadow: 'var(--shadow-lg)',
            zIndex: 50
          }}
        >
          Chat
        </button>
      )}

      {/* Chat Panel */}
      <div 
        className="glass-panel"
        style={{
          position: 'fixed',
          bottom: '24px',
          right: isOpen ? '24px' : '-400px',
          width: '320px',
          height: '480px',
          transition: 'right var(--transition-normal)',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: 'var(--shadow-lg)',
          zIndex: 50,
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-color)',
          overflow: 'hidden'
        }}
      >
        <div style={{
          padding: '16px',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          background: 'var(--bg-tertiary)'
        }}>
          <h3 className="font-semibold text-sm">Team Chat</h3>
          <button onClick={() => setIsOpen(false)} style={{ color: 'var(--text-secondary)' }}>
            ✕
          </button>
        </div>
        
        <div style={{ flex: 1, padding: '16px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <ChatMessage sender="System" text="Welcome to AgentPassport." time="10:00 AM" />
          <ChatMessage sender="Aryan" text="Let's build something fast!" time="10:02 AM" isSelf />
        </div>
        
        <div style={{ padding: '12px', borderTop: '1px solid var(--border-color)', display: 'flex', gap: '8px' }}>
          <input 
            type="text" 
            placeholder="Type a message..." 
            style={{
              flex: 1,
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-color)',
              borderRadius: 'var(--radius-full)',
              padding: '8px 16px',
              color: 'var(--text-primary)',
              outline: 'none',
              fontSize: '0.875rem'
            }}
          />
          <button style={{
            background: 'var(--accent-primary)',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            ↑
          </button>
        </div>
      </div>
    </>
  );
}

function ChatMessage({ sender, text, time, isSelf = false }: { sender: string, text: string, time: string, isSelf?: boolean }) {
  return (
    <div style={{
      alignSelf: isSelf ? 'flex-end' : 'flex-start',
      maxWidth: '85%'
    }}>
      <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginBottom: '4px', textAlign: isSelf ? 'right' : 'left' }}>
        {sender} • {time}
      </div>
      <div style={{
        background: isSelf ? 'var(--accent-primary)' : 'var(--bg-tertiary)',
        padding: '8px 12px',
        borderRadius: 'var(--radius-lg)',
        borderBottomRightRadius: isSelf ? '4px' : 'var(--radius-lg)',
        borderBottomLeftRadius: !isSelf ? '4px' : 'var(--radius-lg)',
        fontSize: '0.875rem'
      }}>
        {text}
      </div>
    </div>
  );
}
