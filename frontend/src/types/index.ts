// ユーザー型
export interface User {
  id: number;
  username: string;
  email?: string;
  full_name?: string;
  family_id?: number;
  created_at: string;
  updated_at?: string;
}

// 家族型
export interface Family {
  id: number;
  name: string;
  created_at: string;
  members: User[];
}

// スケジュール型
export interface Schedule {
  id: number;
  user_id: number;
  family_id: number;
  schedule_type: "return" | "meal" | "car" | "event";
  title?: string;
  description?: string;
  date: string;
  start_time?: string;
  end_time?: string;
  
  // 食事情報
  breakfast?: boolean;
  lunch?: boolean;
  dinner?: boolean;
  
  // 車情報
  car_name?: string;
  
  user: User;
  created_at: string;
  updated_at?: string;
}

// ログインリクエスト
export interface LoginRequest {
  username: string;
  password: string;
}

// ユーザー登録リクエスト
export interface RegisterRequest {
  username: string;
  password: string;
  email?: string;
  full_name?: string;
}

// トークンレスポンス
export interface TokenResponse {
  access_token: string;
  token_type: string;
}