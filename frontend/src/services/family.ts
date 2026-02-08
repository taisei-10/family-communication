import api from './api';
import type { Family } from '../types';

// 家族グループを作成
export const createFamily = async (name: string): Promise<Family> => {
  const response = await api.post<Family>('/families/', { name });
  return response.data;
};

// 自分の家族情報を取得
export const getMyFamily = async (): Promise<Family> => {
  const response = await api.get<Family>('/families/me');
  return response.data;
};

// 家族グループに参加
export const joinFamily = async (familyId: number): Promise<Family> => {
  const response = await api.post<Family>(`/families/${familyId}/members`);
  return response.data;
};

// 家族グループから離脱
export const leaveFamily = async (familyId: number): Promise<void> => {
  await api.delete(`/families/${familyId}/members/me`);
};