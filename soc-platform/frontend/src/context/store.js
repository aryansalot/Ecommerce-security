import create from 'zustand';

export const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('user')) || null,
  token: localStorage.getItem('token') || null,
  isAuthenticated: !!localStorage.getItem('token'),
  
  login: (user, token) => {
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('token', token);
    set({ user, token, isAuthenticated: true });
  },
  
  logout: () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    set({ user: null, token: null, isAuthenticated: false });
  }
}));

export const useDashboardStore = create((set) => ({
  dashboardData: null,
  loading: false,
  error: null,
  
  setDashboardData: (data) => set({ dashboardData: data }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error })
}));
