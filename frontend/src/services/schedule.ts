import api from './api';
import type { Schedule } from '../types';

// スケジュール作成用の型
interface ScheduleCreateRequest {
  schedule_type: 'return' | 'meal' | 'car' | 'event';
  title?: string;
  description?: string;
  date: string;  // YYYY-MM-DD 形式
  start_time?: string;  // HH:MM:SS 形式
  end_time?: string;
  breakfast?: boolean;
  lunch?: boolean;
  dinner?: boolean;
  car_name?: string;
}

// スケジュールを作成
export const createSchedule = async (data: ScheduleCreateRequest): Promise<Schedule> => {
  const response = await api.post<Schedule>('/schedules/', data);
  return response.data;
};

// 家族全員のスケジュールを取得
export const getSchedules = async (
  scheduleType?: string,
  startDate?: string,
  endDate?: string
): Promise<Schedule[]> => {
  const params = new URLSearchParams();
  
  if (scheduleType) params.append('schedule_type', scheduleType);
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  
  const response = await api.get<Schedule[]>(`/schedules/?${params.toString()}`);
  return response.data;
};

// 自分のスケジュールのみ取得
export const getMySchedules = async (scheduleType?: string): Promise<Schedule[]> => {
  const params = new URLSearchParams();
  if (scheduleType) params.append('schedule_type', scheduleType);
  
  const response = await api.get<Schedule[]>(`/schedules/me?${params.toString()}`);
  return response.data;
};

// 特定のスケジュールを取得
export const getSchedule = async (scheduleId: number): Promise<Schedule> => {
  const response = await api.get<Schedule>(`/schedules/${scheduleId}`);
  return response.data;
};

// スケジュールを更新
export const updateSchedule = async (
  scheduleId: number,
  data: ScheduleCreateRequest
): Promise<Schedule> => {
  const response = await api.put<Schedule>(`/schedules/${scheduleId}`, data);
  return response.data;
};

// スケジュールを削除
export const deleteSchedule = async (scheduleId: number): Promise<void> => {
  await api.delete(`/schedules/${scheduleId}`);
};