import api from './api';
import type { Family, FamilyCreateRequest, FamilyMember } from '../types';

/**
 * 家族グループを作成
 */
export const createFamily = async (data: FamilyCreateRequest): Promise<Family> => {
  console.log('[FAMILY API] 家族作成:', data);
  const response = await api.post<Family>('/families/', data);
  return response.data;
};

/**
 * 自分が所属する家族グループを取得
 */
export const getMyFamily = async (): Promise<Family> => {
  console.log('[FAMILY API] 家族情報取得');
  const response = await api.get<Family>('/families/me');
  return response.data;
};

/**
 * 招待コードで家族グループに参加
 */
export const joinFamilyByInviteCode = async (inviteCode: string): Promise<Family> => {
  console.log('[FAMILY API] 招待コードで家族参加:', inviteCode);
  const response = await api.post<Family>(`/families/join/${inviteCode}`);
  return response.data;
};

/**
 * family_idで家族グループに参加
 */
export const joinFamily = async (familyId: number): Promise<Family> => {
  console.log('[FAMILY API] 家族参加:', familyId);
  const response = await api.post<Family>(`/families/${familyId}/members`);
  return response.data;
};

/**
 * 家族グループから離脱
 */
export const leaveFamily = async (familyId: number): Promise<void> => {
  console.log('[FAMILY API] 家族離脱:', familyId);
  await api.delete(`/families/${familyId}/members/me`);
};