import { ChatInterface } from '@/components/ChatInterface';

export default function Home() {
  return (
    <main className="relative min-h-screen">
      <div className="fixed inset-0 -z-10 bg-gradient-to-br from-chinese-black via-american-blue/5 to-chinese-black" />
      <div className="fixed inset-0 -z-10 opacity-30">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(131,135,195,0.1),transparent_50%)]" />
      </div>
      <ChatInterface />
    </main>
  );
}
