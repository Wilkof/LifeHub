'use client';

import { useEffect, useState } from 'react';
import { useTranslations } from 'next-intl';
import Header from '@/app/components/layout/Header';
import Card from '@/app/components/ui/Card';
import { api } from '@/app/lib/api';
import { FileText, Plus } from 'lucide-react';

interface PageProps {
  params: { locale: string };
}

export default function NotesPage({ params: { locale } }: PageProps) {
  const t = useTranslations('notes');
  const [notes, setNotes] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [quickNote, setQuickNote] = useState('');

  const loadNotes = async () => {
    setError(null);
    try {
      const data = await api.getNotes({ limit: '20' });
      setNotes(data);
    } catch (err: any) {
      setError(err?.message || 'Не вдалося завантажити нотатки');
    }
  };

  useEffect(() => {
    loadNotes();
  }, []);

  const addQuickNote = async () => {
    if (!quickNote.trim()) return;
    try {
      await api.createQuickNote(quickNote.trim());
      setQuickNote('');
      await loadNotes();
    } catch (err: any) {
      setError(err?.message || 'Не вдалося створити нотатку');
    }
  };

  return (
    <div className="max-w-4xl">
      <Header locale={locale} title={t('title')} />

      {error && (
        <Card className="mb-4 border border-red-200 bg-red-50 text-red-700">
          {error}
        </Card>
      )}

      <Card className="mb-4">
        <div className="flex gap-3">
          <input
            className="input flex-1"
            placeholder={t('quickNote')}
            value={quickNote}
            onChange={(e) => setQuickNote(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addQuickNote()}
          />
          <button className="btn btn-primary" onClick={addQuickNote}>
            <Plus className="w-4 h-4" />
          </button>
        </div>
      </Card>

      <div className="space-y-3">
        {notes.length ? (
          notes.map((note) => (
            <Card key={note.id}>
              <div className="flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4 text-dark-600" />
                <div className="font-medium">{note.title || 'Без назви'}</div>
              </div>
              <div className="text-sm text-dark-500 whitespace-pre-wrap">
                {note.content}
              </div>
            </Card>
          ))
        ) : (
          <Card className="text-center py-8">Немає нотаток</Card>
        )}
      </div>
    </div>
  );
}
