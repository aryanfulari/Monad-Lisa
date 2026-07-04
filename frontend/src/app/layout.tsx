import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import TopBar from "@/components/TopBar";
import ChatPanel from "@/components/ChatPanel";

export const metadata: Metadata = {
  title: "AgentPassport",
  description: "AI Credential Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body style={{ display: 'flex', minHeight: '100vh' }}>
        <Sidebar />
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
          <TopBar />
          <main style={{ flex: 1, padding: '24px', overflowY: 'auto' }}>
            {children}
          </main>
        </div>
        <ChatPanel />
      </body>
    </html>
  );
}
