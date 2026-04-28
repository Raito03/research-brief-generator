import { ChatInterface } from '@/components/ChatInterface';
import { ThemeToggle } from '@/components/ThemeToggle';

export default function Home() {
  return (
    <main className="min-h-screen bg-[--background]">
      <ThemeToggle />
      <div className="max-w-4xl mx-auto px-6 py-12">
        <ChatInterface />
      </div>
    </main>
  );
}