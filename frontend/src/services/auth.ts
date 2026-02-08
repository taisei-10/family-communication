import api from './api';
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types';

// ログイン
export const login = async (credentials: LoginRequest): Promise<TokenResponse> => {
  // FormDataに変換（FastAPIのOAuth2PasswordRequestForm形式）
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);
  
  const response = await api.post<TokenResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  
  // トークンをlocalStorageに保存
  localStorage.setItem('access_token', response.data.access_token);
  
  return response.data;
};

// ユーザー登録
export const register = async (userData: RegisterRequest): Promise<User> => {
  const response = await api.post<User>('/auth/register', userData);
  return response.data;
};

// ログアウト
export const logout = () => {
  // トークンを削除
  localStorage.removeItem('access_token');
};

// 自分のプロフィールを取得
export const getMe = async (): Promise<User> => {
  const response = await api.get<User>('/users/me');
  return response.data;
};

// ログイン状態を確認
export const isAuthenticated = (): boolean => {
  return !!localStorage.getItem('access_token');
};