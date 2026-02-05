'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
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

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const responses: Record<string, string> = {
        general: `Зрозуміло! Давай розберемося з цим питанням. На основі твоїх даних можу порадити наступне:\n\n1. Спочатку визнач пріоритети\n2. Розбий велике на менші кроки\n3. Почни з найпростішого\n\nЩо конкретно тебе турбує?`,
        planDay: `📅 **План на сьогодні:**\n\n**Ранок (8:00-12:00):**\n• Перша MIT задача\n• 25 хв фокус + 5 хв перерва\n\n**День (12:00-18:00):**\n• Друга MIT задача\n• Рутинні справи\n\n**Вечір (18:00-21:00):**\n• Третя MIT або відпочинок\n• Підготовка до завтра\n\n💧 Не забудь про воду!`,
        breakGoal: `🎯 **Розбиваємо ціль на кроки:**\n\n**Етап 1 (Тиждень 1-2):**\n• Крок 1.1\n• Крок 1.2\n\n**Етап 2 (Тиждень 3-4):**\n• Крок 2.1\n• Крок 2.2\n\n**Ключові результати:**\n• KR1: ...\n• KR2: ...\n\nПочни з найпершого кроку прямо зараз!`,
        weekSummary: `📊 **Підсумок твого тижня:**\n\n✅ **Досягнення:**\n• Виконано задач: 12\n• Звички: 78%\n\n⚠️ **Зони росту:**\n• Сон нижче норми 2 дні\n• 2 дедлайни перенесено\n\n💡 **Рекомендації:**\n1. Лягай на 30 хв раніше\n2. Зменши MIT до 2 на день\n\nЗагалом - хороший тиждень! 💪`,
        antiProcrastination: `⚡ **Почни ЗАРАЗ:**\n\n**Мікро-крок (2 хвилини):**\nПросто відкрий файл/документ. Нічого більше.\n\n**Чому це важливо:**\nКожна хвилина відкладання - це енергія на тривогу замість дії.\n\n**Техніка 5-4-3-2-1:**\nПорахуй 5-4-3-2-1 і РОБИ.\n\n💪 Ти можеш. Один маленький крок.`,
      };

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: responses[activeMode] || responses.general,
        },
      ]);
      setIsLoading(false);
    }, 1500);
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
