export interface User {
  id: number;
  email: string;
  username: string;
  nombre_completo: string;
  rol: 'ADMIN' | 'ANALISTA' | 'VIEWER';
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  nombre_completo: string;
  rol: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}
