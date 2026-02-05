'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { cn } from '@/app/lib/utils';
import {
  Bot,
  Send,
  Calendar,
  Target,
  TrendingUp,
  Zap,
  Loader2,
} from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

const modes = [
  { key: 'general', icon: Bot, label: 'Загальний' },
  { key: 'planDay', icon: Calendar, label: 'План дня' },
  { key: 'breakGoal', icon: Target, label: 'Розбити ціль' },
  { key: 'weekSummary', icon: TrendingUp, label: 'Підсумок тижня' },
  { key: 'antiProcrastination', icon: Zap, label: 'Антипрокрастинація' },
];

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function AIPage({ params: { locale } }: PageProps) {
  const t = useTranslations('ai');
  const [activeMode, setActiveMode] = useState('general');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Привіт! Я твій AI асистент у LifeHub. Обери режим або просто запитай що завгодно. 🤖',
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const modeMap: Record<string, string> = {
        general: 'general',
        planDay: 'plan_day',
        breakGoal: 'break_goal',
        weekSummary: 'week_summary',
        antiProcrastination: 'anti_procrastination',
      };
      const res = await api.chat(userMessage, modeMap[activeMode] || 'general');
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: res?.response || 'Не вдалося отримати відповідь.' },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: err?.message || 'Помилка AI сервісу.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl h-[calc(100vh-3rem)]">
      <Header locale={locale} title={t('title')} />

      <div className="flex gap-6 h-[calc(100%-6rem)]">
        {/* Mode selector */}
        <div className="w-64 space-y-2">
          {modes.map((mode) => {
            const Icon = mode.icon;
            return (
              <button
                key={mode.key}
                onClick={() => setActiveMode(mode.key)}
                className={cn(
                  'w-full flex items-center gap-3 p-4 rounded-2xl transition-all',
                  activeMode === mode.key
                    ? 'bg-lime-500 text-dark-900'
                    : 'bg-white hover:bg-sage-100'
                )}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{mode.label}</span>
              </button>
            );
          })}
        </div>

        {/* Chat area */}
        <Card className="flex-1 flex flex-col p-0 overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={cn(
                  'flex',
                  msg.role === 'user' ? 'justify-end' : 'justify-start'
                )}
              >
                <div
                  className={cn(
                    'max-w-[80%] rounded-2xl p-4',
                    msg.role === 'user'
                      ? 'bg-dark-800 text-white'
                      : 'bg-sage-100'
                  )}
                >
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-sage-100 rounded-2xl p-4">
                  <Loader2 className="w-5 h-5 animate-spin" />
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="p-4 border-t border-sage-200">
            <div className="flex gap-3">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder={t('placeholder')}
                className="input flex-1"
                disabled={isLoading}
              />
              <button
                onClick={handleSend}
                disabled={isLoading || !input.trim()}
                className="btn btn-primary px-6"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
