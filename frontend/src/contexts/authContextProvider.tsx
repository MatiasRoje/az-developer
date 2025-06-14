import React, { useReducer, useEffect } from "react";
import { useNavigate } from "react-router";
import type { AuthState, AuthAction } from "../types/auth";
import { AuthContext } from "./authContext";
import { authService } from "../services/authService";
import { tokenStorage } from "../utils/tokenStorage";

const initialState: AuthState = {
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

// Auth reducer for state management
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case "LOGIN_START":
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case "LOGIN_SUCCESS":
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case "LOGIN_ERROR":
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case "TOKEN_REFRESH":
      return {
        ...state,
        token: action.token,
      };
    case "LOGOUT":
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case "CLEAR_ERROR":
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

export const AuthContextProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const navigate = useNavigate();

  // Check for existing session on app load
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const user = tokenStorage.getUser();
        const token = tokenStorage.getToken();

        if (user && token && tokenStorage.isSessionValid()) {
          // Check if token is still valid with backend
          const isValid = await authService.validateToken(token.access_token);

          if (isValid && !authService.isTokenExpired(token)) {
            dispatch({
              type: "LOGIN_SUCCESS",
              payload: { user, token },
            });
          } else {
            // Token expired or invalid, clear storage
            console.log("Token expired or invalid");
          }
        }
      } catch (error) {
        console.error("Error initializing auth:", error);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: "LOGIN_START" });

    try {
      const { user, token } = await authService.login(email, password);

      // Store auth data securely
      tokenStorage.storeAuth(user, token);

      dispatch({ type: "LOGIN_SUCCESS", payload: { user, token } });

      // Navigate to dashboard after successful login
      navigate("/dashboard");
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Login failed";
      dispatch({ type: "LOGIN_ERROR", payload: errorMessage });
    }
  };

  // TODO: Implement registration
  // const register = async (email: string, password: string, name: string) => {
  //   dispatch({ type: "LOGIN_START" });

  //   try {
  //     const { user, token } = await authService.register(email, password, name);

  //     tokenStorage.storeAuth(user, tokens);

  //     dispatch({ type: "LOGIN_SUCCESS", payload: { user, tokens } });
  //   } catch (error) {
  //     const errorMessage =
  //       error instanceof Error ? error.message : "Registration failed";
  //     dispatch({ type: "LOGIN_ERROR", payload: errorMessage });
  //   }
  // };

  const logout = () => {
    tokenStorage.clearAuth();
    dispatch({ type: "LOGOUT" });

    // Navigate to home page after logout
    navigate("/");
  };

  const clearError = () => {
    dispatch({ type: "CLEAR_ERROR" });
  };

  return (
    <AuthContext.Provider
      value={{
        ...state,
        login,
        logout,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
