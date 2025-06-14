export type User = {
  id: string;
  email: string;
  name: string;
};

export type AuthToken = {
  access_token: string;
  token_type: string;
  expires_in: number;
  expires_at: number;
};

export type AuthState = {
  user: User | null;
  token: AuthToken | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
};

export type AuthAction =
  | { type: "LOGIN_START" }
  | { type: "LOGIN_SUCCESS"; payload: { user: User; token: AuthToken } }
  | { type: "LOGIN_ERROR"; payload: string }
  | { type: "TOKEN_REFRESH"; token: AuthToken }
  | { type: "LOGOUT" }
  | { type: "CLEAR_ERROR" };
