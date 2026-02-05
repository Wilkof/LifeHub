/**
 * API client for LifeHub backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: any;
  headers?: Record<string, string>;
}

class ApiClient {
  private baseUrl: string;
  private accessToken: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    // Get token from localStorage on client side
    if (typeof window !== 'undefined') {
      this.accessToken = localStorage.getItem('lifehub_token');
    }
  }

  setToken(token: string) {
    this.accessToken = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('lifehub_token', token);
    }
  }

  private async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const { method = 'GET', body, headers = {} } = options;

    // Refresh token from localStorage if needed (client-side)
    if (!this.accessToken && typeof window !== 'undefined') {
      this.accessToken = localStorage.getItem('lifehub_token');
    }

    const requestHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...headers,
    };

    if (this.accessToken) {
      requestHeaders['X-Access-Token'] = this.accessToken;
    }

    const response = await fetch(`${this.baseUrl}/api${endpoint}`, {
      method,
      headers: requestHeaders,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Dashboard
  async getDashboardToday() {
    return this.request('/dashboard/today');
  }

  async getWeeklyOverview() {
    return this.request('/dashboard/weekly-overview');
  }

  // Tasks
  async getTasks(params?: Record<string, any>) {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/tasks${query}`);
  }

  async getTodayTasks() {
    return this.request('/tasks/today');
  }

  async getMitTasks() {
    return this.request('/tasks/mit');
  }

  async createTask(data: any) {
    return this.request('/tasks', { method: 'POST', body: data });
  }

  async updateTask(id: number, data: any) {
    return this.request(`/tasks/${id}`, { method: 'PUT', body: data });
  }

  async deleteTask(id: number) {
    return this.request(`/tasks/${id}`, { method: 'DELETE' });
  }

  async completeTask(id: number) {
    return this.request(`/tasks/${id}/complete`, { method: 'POST' });
  }

  async toggleMit(id: number) {
    return this.request(`/tasks/${id}/mit`, { method: 'POST' });
  }

  // Calendar
  async getEvents(startDate?: string, endDate?: string) {
    const params = new URLSearchParams();
    if (startDate) params.set('start_date', startDate);
    if (endDate) params.set('end_date', endDate);
    return this.request(`/calendar/events?${params}`);
  }

  async getTodayEvents() {
    return this.request('/calendar/events/today');
  }

  async createEvent(data: any) {
    return this.request('/calendar/events', { method: 'POST', body: data });
  }

  async updateEvent(id: number, data: any) {
    return this.request(`/calendar/events/${id}`, { method: 'PUT', body: data });
  }

  async deleteEvent(id: number) {
    return this.request(`/calendar/events/${id}`, { method: 'DELETE' });
  }

  // Finances
  async getTransactions(params?: Record<string, any>) {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/finances/transactions${query}`);
  }

  async getTransactionsSummary(month?: number, year?: number) {
    const params = new URLSearchParams();
    if (month) params.set('month', month.toString());
    if (year) params.set('year', year.toString());
    return this.request(`/finances/transactions/summary?${params}`);
  }

  async createTransaction(data: any) {
    return this.request('/finances/transactions', { method: 'POST', body: data });
  }

  async getBudgets() {
    return this.request('/finances/budgets');
  }

  async getBudgetStatus(month?: number, year?: number) {
    const params = new URLSearchParams();
    if (month) params.set('month', month.toString());
    if (year) params.set('year', year.toString());
    return this.request(`/finances/budgets/status?${params}`);
  }

  async getSubscriptions() {
    return this.request('/finances/subscriptions');
  }

  async getUpcomingSubscriptions(days = 7) {
    return this.request(`/finances/subscriptions/upcoming?days=${days}`);
  }

  // Health
  async getHealthLogs(dateFrom?: string, dateTo?: string) {
    const params = new URLSearchParams();
    if (dateFrom) params.set('date_from', dateFrom);
    if (dateTo) params.set('date_to', dateTo);
    return this.request(`/health/logs?${params}`);
  }

  async getTodayHealth() {
    return this.request('/health/logs/today');
  }

  async updateHealthLog(date: string, data: any) {
    return this.request(`/health/logs/${date}`, { method: 'PUT', body: data });
  }

  async addWater(glasses = 1) {
    return this.request(`/health/logs/water?glasses=${glasses}`, { method: 'POST' });
  }

  async getHealthStats() {
    return this.request('/health/stats/weekly');
  }

  // Habits
  async getHabits() {
    return this.request('/habits');
  }

  async getTodayHabits() {
    return this.request('/habits/today');
  }

  async createHabit(data: any) {
    return this.request('/habits', { method: 'POST', body: data });
  }

  async completeHabit(id: number, date?: string) {
    const query = date ? `?log_date=${date}` : '';
    return this.request(`/habits/${id}/complete${query}`, { method: 'POST' });
  }

  async uncompleteHabit(id: number, date?: string) {
    const query = date ? `?log_date=${date}` : '';
    return this.request(`/habits/${id}/uncomplete${query}`, { method: 'POST' });
  }

  // Goals
  async getGoals(params?: Record<string, any>) {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/goals${query}`);
  }

  async getActiveGoals() {
    return this.request('/goals/active');
  }

  async getGoalsTree() {
    return this.request('/goals/tree');
  }

  async createGoal(data: any) {
    return this.request('/goals', { method: 'POST', body: data });
  }

  async updateGoal(id: number, data: any) {
    return this.request(`/goals/${id}`, { method: 'PUT', body: data });
  }

  async updateGoalProgress(id: number, progress: number, notes?: string) {
    const params = new URLSearchParams({ progress: progress.toString() });
    if (notes) params.set('notes', notes);
    return this.request(`/goals/${id}/progress?${params}`, { method: 'POST' });
  }

  // Notes
  async getNotes(params?: Record<string, any>) {
    const query = params ? '?' + new URLSearchParams(params).toString() : '';
    return this.request(`/notes${query}`);
  }

  async getInbox() {
    return this.request('/notes/inbox');
  }

  async getJournal() {
    return this.request('/notes/journal');
  }

  async createNote(data: any) {
    return this.request('/notes', { method: 'POST', body: data });
  }

  async createQuickNote(content: string) {
    return this.request(`/notes/quick?content=${encodeURIComponent(content)}`, { method: 'POST' });
  }

  async updateNote(id: number, data: any) {
    return this.request(`/notes/${id}`, { method: 'PUT', body: data });
  }

  async deleteNote(id: number) {
    return this.request(`/notes/${id}`, { method: 'DELETE' });
  }

  // AI
  async chat(message: string, mode = 'general', context?: any) {
    return this.request('/ai/chat', {
      method: 'POST',
      body: { message, mode, context },
    });
  }

  async getDailyBriefing() {
    return this.request('/ai/daily-briefing');
  }

  async planDay() {
    return this.request('/ai/plan-day', { method: 'POST' });
  }

  async breakGoal(goalTitle: string, description?: string, targetDate?: string) {
    const params = new URLSearchParams({ goal_title: goalTitle });
    if (description) params.set('goal_description', description);
    if (targetDate) params.set('target_date', targetDate);
    return this.request(`/ai/break-goal?${params}`, { method: 'POST' });
  }

  async getWeekSummary() {
    return this.request('/ai/week-summary', { method: 'POST' });
  }

  async getAntiProcrastination(taskTitle?: string) {
    const query = taskTitle ? `?task_title=${encodeURIComponent(taskTitle)}` : '';
    return this.request(`/ai/anti-procrastination${query}`, { method: 'POST' });
  }

  // Settings
  async getSettings() {
    return this.request('/settings');
  }

  async updateSettings(data: any) {
    return this.request('/settings', { method: 'PUT', body: data });
  }

  // Weather
  async getCurrentWeather(city?: string) {
    const query = city ? `?city=${encodeURIComponent(city)}` : '';
    return this.request(`/weather/current${query}`);
  }

  async getWeatherForecast(city?: string, days = 3) {
    const params = new URLSearchParams({ days: days.toString() });
    if (city) params.set('city', city);
    return this.request(`/weather/forecast?${params}`);
  }
}

export const api = new ApiClient(API_URL);
export default api;
