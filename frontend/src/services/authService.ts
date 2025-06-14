/**
 * Auth Service for Azure Certification Demo
 * AZ-204 Focus: Frontend integration with API Gateway
 * Connects to FastAPI Gateway -> Auth Service
 */

import type { User, AuthToken } from "../types/auth";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8080";

class AuthServiceError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "AuthServiceError";
  }
}

export class AuthService {
  private static instance: AuthService;

  static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  /**
   * Login user with email/password
   * AZ-204 Pattern: Basic Auth -> JWT token exchange
   */
  async login(
    email: string,
    password: string
  ): Promise<{ user: User; token: AuthToken }> {
    try {
      // Create Basic Auth header
      const credentials = btoa(`${email}:${password}`);

      const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: {
          Authorization: `Basic ${credentials}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: "Login failed" }));
        throw new AuthServiceError(
          errorData.detail || `Login failed: ${response.statusText}`,
          response.status
        );
      }

      const tokenData = await response.json();

      // Calculate expiration timestamp
      const expires_at = Date.now() + tokenData.expires_in * 1000;

      const token: AuthToken = {
        access_token: tokenData.access_token,
        token_type: tokenData.token_type,
        expires_in: tokenData.expires_in,
        expires_at,
      };

      // Extract user info from JWT payload (for demo purposes)
      // AZ-204 Note: In production, validate JWT signature
      const user = this.extractUserFromToken(tokenData.access_token, email);

      return { user, token };
    } catch (error) {
      if (error instanceof AuthServiceError) {
        throw error;
      }
      throw new AuthServiceError(
        "Network error: Unable to connect to auth service"
      );
    }
  }

  /**
   * Validate token with backend
   * AZ-204 Pattern: Token validation through API Gateway
   */
  async validateToken(token: string): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/validate`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      return response.ok;
    } catch (error) {
      console.error("Token validation failed:", error);
      return false;
    }
  }

  /**
   * TODO: Implement registration
   * Register new user
   * AZ-204 Note: Registration would typically go through Azure AD B2C
   */
  // async register(
  //   email: string,
  //   password: string,
  //   name: string
  // ): Promise<{ user: User; token: AuthToken }> {
  // Send the request to the backend
  // Return the user and token
  // If the request fails, throw an error
  // If the request is successful, return the user and token
  // }

  /**
   * Check if token is expired
   */
  isTokenExpired(token: AuthToken): boolean {
    const now = Date.now();
    const expirationBuffer = 5 * 60 * 1000; // 5 minutes buffer
    return now >= token.expires_at - expirationBuffer;
  }

  /**
   * Extract user info from JWT token (simple decode for demo)
   * AZ-204 Note: In production, use proper JWT library and validate signature
   */
  private extractUserFromToken(token: string, email: string): User {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      console.log("payload", payload);
      return {
        id: payload.sub || payload.email || email,
        email: payload.email || email,
        name: payload.username || email.split("@")[0],
      };
    } catch (error) {
      console.error("Error extracting user from token:", error);
      // Fallback user object
      return {
        id: email,
        email,
        name: email.split("@")[0],
      };
    }
  }
}

export const authService = AuthService.getInstance();
