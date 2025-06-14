import React, { useOptimistic, useTransition } from "react";
import { useAuth } from "../hooks/useAuth";

type AuthFormProps = {
  mode: "login" | "register";
  onToggleMode: () => void;
};

export const AuthForm: React.FC<AuthFormProps> = ({ mode, onToggleMode }) => {
  const { login, error, clearError } = useAuth();
  const [isPending, startTransition] = useTransition();

  // Optimistic state for immediate UI feedback
  const [optimisticState, setOptimisticState] = useOptimistic(
    { isSubmitting: false },
    (currentState, newState: { isSubmitting?: boolean }) => ({
      ...currentState,
      ...newState,
    })
  );

  const handleSubmit = async (formData: FormData) => {
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    clearError();

    // Start optimistic update
    setOptimisticState({ isSubmitting: true });

    // Start transition for the actual login/register
    startTransition(async () => {
      try {
        if (mode === "login") {
          await login(email, password);
        } else {
          // await register(email, password, name);
        }
        // Success state will be handled by navigation in auth context
      } catch (error) {
        // Error handling is managed by the auth context
        console.error("Error logging in", error);
        setOptimisticState({ isSubmitting: false });
      }
    });
  };

  const isLoading = isPending || optimisticState.isSubmitting;

  return (
    <div className="azure-card max-w-md mx-auto p-8">
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-neutral-900 mb-2">
          {mode === "login" ? "Welcome Back" : "Create Account"}
        </h2>
        <p className="text-neutral-600">
          {mode === "login"
            ? "Sign in to access your image gallery"
            : "Join the Azure Developer Certification Suite"}
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6">
          {error}
        </div>
      )}

      <form action={handleSubmit} className="space-y-6">
        {mode === "register" && (
          <div>
            <label
              htmlFor="name"
              className="block text-sm font-medium text-neutral-700 mb-2"
            >
              Full Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              className="azure-input w-full"
              required
              disabled={isLoading}
              placeholder="Enter your full name"
            />
          </div>
        )}

        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-neutral-700 mb-2"
          >
            Email Address
          </label>
          <input
            type="email"
            id="email"
            name="email"
            className="azure-input w-full"
            required
            disabled={isLoading}
            placeholder="Enter your email"
          />
        </div>

        <div>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-neutral-700 mb-2"
          >
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            className="azure-input w-full"
            required
            disabled={isLoading}
            placeholder="Enter your password"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="azure-button-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              {mode === "login" ? "Signing In..." : "Creating Account..."}
            </span>
          ) : mode === "login" ? (
            "Sign In"
          ) : (
            "Create Account"
          )}
        </button>
      </form>

      <div className="mt-6 text-center">
        <p className="text-neutral-600">
          {mode === "login"
            ? "Don't have an account? "
            : "Already have an account? "}
          <button
            onClick={onToggleMode}
            disabled={isLoading}
            className="text-azure-600 hover:text-azure-700 font-medium hover:cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {mode === "login" ? "Sign up" : "Sign in"}
          </button>
        </p>
      </div>

      {mode === "login" && (
        <div className="mt-4 p-4 bg-azure-50 rounded-md">
          <p className="text-sm text-azure-700">
            <strong>Demo credentials:</strong>
            <br />
            Email: demo@azure.com
            <br />
            Password: Testing123
          </p>
        </div>
      )}
    </div>
  );
};
