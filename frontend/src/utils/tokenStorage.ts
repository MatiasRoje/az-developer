/**
 * Secure Token Storage for Azure Certification Demo
 * AZ-204 Security Pattern: Secure client-side token management
 */

import type { AuthToken, User } from "../types/auth";

const STORAGE_KEYS = {
  USER: "azure-auth-user",
  TOKEN: "azure-auth-token",
  LAST_LOGIN: "azure-auth-last-login",
} as const;

export class TokenStorage {
  private static instance: TokenStorage;

  static getInstance(): TokenStorage {
    if (!TokenStorage.instance) {
      TokenStorage.instance = new TokenStorage();
    }
    return TokenStorage.instance;
  }

  /**
   * Store user and tokens securely
   * AZ-204 Note: In production, consider using secure cookies or sessionStorage
   */
  storeAuth(user: User, token: AuthToken): void {
    try {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
      localStorage.setItem(STORAGE_KEYS.TOKEN, JSON.stringify(token));
      localStorage.setItem(STORAGE_KEYS.LAST_LOGIN, Date.now().toString());
    } catch (error) {
      console.error("Failed to store auth data:", error);
    }
  }

  /**
   * Get stored user data
   */
  getUser(): User | null {
    try {
      const userData = localStorage.getItem(STORAGE_KEYS.USER);
      return userData ? JSON.parse(userData) : null;
    } catch (error) {
      console.error("Failed to parse user data:", error);
      this.clearAuth();
      return null;
    }
  }

  /**
   * Get stored tokens
   */
  getToken(): AuthToken | null {
    try {
      const tokenData = localStorage.getItem(STORAGE_KEYS.TOKEN);
      return tokenData ? JSON.parse(tokenData) : null;
    } catch (error) {
      console.error("Failed to parse token:", error);
      this.clearAuth();
      return null;
    }
  }

  /**
   * Check if session is valid (within 24 hours)
   */
  isSessionValid(): boolean {
    try {
      const lastLogin = localStorage.getItem(STORAGE_KEYS.LAST_LOGIN);
      if (!lastLogin) return false;

      const lastLoginTime = parseInt(lastLogin);
      const now = Date.now();
      const dayInMs = 24 * 60 * 60 * 1000; // 24 hours

      return now - lastLoginTime < dayInMs;
    } catch (error) {
      console.error("Failed to check session validity:", error);
      return false;
    }
  }

  /**
   * Update tokens (for refresh scenarios)
   */
  updateToken(token: AuthToken): void {
    try {
      localStorage.setItem(STORAGE_KEYS.TOKEN, JSON.stringify(token));
    } catch (error) {
      console.error("Failed to update tokens:", error);
    }
  }

  /**
   * Clear all auth data
   */
  clearAuth(): void {
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    localStorage.removeItem(STORAGE_KEYS.LAST_LOGIN);
  }

  /**
   * Get auth header for API requests
   */
  getAuthHeader(): string | null {
    const token = this.getToken();
    if (!token) return null;

    return `${token.token_type} ${token.access_token}`;
  }
}

export const tokenStorage = TokenStorage.getInstance();
