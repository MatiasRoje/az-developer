import React, { useReducer, useEffect } from "react";
import type { AuthState, AuthAction, User } from "../../types/auth";
import { AuthContext } from "./authContext";

const initialState: AuthState = {
  user: null,
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
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case "LOGIN_ERROR":
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case "LOGOUT":
      return {
        ...state,
        user: null,
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

// NOTE: Mock authentication service (replace with Azure Functions later)
const mockAuthService = {
  async login(email: string, password: string): Promise<User> {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (email === "demo@azure.com" && password === "Testing123") {
      return {
        id: "1",
        email: "demo@azure.com",
        name: "Azure Developer",
      };
    }
    
    throw new Error("Invalid email or password");
  },

  async register(email: string, password: string, name: string): Promise<User> {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return {
      id: Date.now().toString(),
      email,
      name,
    };
  },
};

export const AuthContextProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    const savedUser = localStorage.getItem("azure-auth-user");
    if (savedUser) {
      try {
        const user = JSON.parse(savedUser);
        dispatch({ type: "LOGIN_SUCCESS", payload: user });
      } catch (error) {
        console.error("Error parsing saved user:", error);
        localStorage.removeItem("azure-auth-user");
      }
    }
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: "LOGIN_START" });
    
    try {
      const user = await mockAuthService.login(email, password);
      localStorage.setItem("azure-auth-user", JSON.stringify(user));
      dispatch({ type: "LOGIN_SUCCESS", payload: user });
    } catch (error) {
      dispatch({ 
        type: "LOGIN_ERROR", 
        payload: error instanceof Error ? error.message : "Login failed"
      });
    }
  };

  const register = async (email: string, password: string, name: string) => {
    dispatch({ type: "LOGIN_START" });
    
    try {
      const user = await mockAuthService.register(email, password, name);
      localStorage.setItem("azure-auth-user", JSON.stringify(user));
      dispatch({ type: "LOGIN_SUCCESS", payload: user });
    } catch (error) {
      dispatch({ 
        type: "LOGIN_ERROR", 
        payload: error instanceof Error ? error.message : "Registration failed"
      });
    }
  };

  const logout = () => {
    localStorage.removeItem("azure-auth-user");
    dispatch({ type: "LOGOUT" });
  };

  const clearError = () => {
    dispatch({ type: "CLEAR_ERROR" });
  };

  return (
    <AuthContext.Provider value={{
      ...state,
      login,
      register,
      logout,
      clearError,
    }}>
      {children}
    </AuthContext.Provider>
  );
}; 