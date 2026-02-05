\'use client\';
\n+import { useEffect, useState } from 'react';
import { api } from '@/app/lib/api';
import { cn } from '@/app/lib/utils';
\n+export default function AccessTokenBanner() {
  const [token, setToken] = useState('');
  const [storedToken, setStoredToken] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
\n+  useEffect(() => {
    if (typeof window !== 'undefined') {
      setStoredToken(localStorage.getItem('lifehub_token'));
    }
  }, []);
\n+  const handleSave = () => {
    if (!token.trim()) {
      setMessage('Введіть токен доступу.');
      return;
    }
    api.setToken(token.trim());
    setStoredToken(token.trim());
    setToken('');
    setMessage('Токен збережено.');
  };
\n+  const handleClear = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('lifehub_token');
    }
    setStoredToken(null);
    setMessage('Токен очищено.');
  };
\n+  if (storedToken) return null;
\n+  return (
    <div className="mb-4 rounded-2xl bg-lime-100 border border-lime-300 p-4">
      <div className="text-sm font-medium text-dark-900 mb-2">
        Потрібен токен доступу (APP_ACCESS_TOKEN), щоб підключити бекенд.
      </div>
      <div className="flex flex-col md:flex-row gap-3">
        <input
          className="input flex-1"
          type="password"
          placeholder="Вставте APP_ACCESS_TOKEN"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        />
        <button className="btn btn-primary" onClick={handleSave}>
          Зберегти токен
        </button>
        <button className={cn('btn btn-secondary')} onClick={handleClear}>
          Очистити
        </button>
      </div>
      {message && <div className="text-xs text-dark-600 mt-2">{message}</div>}
    </div>
  );
}
