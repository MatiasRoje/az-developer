import { useState } from "react";
import { AuthForm } from "../components/AuthForm";

export const LandingPage: React.FC = () => {
  const [authMode, setAuthMode] = useState<"login" | "register">("login");

  return (
    <section className="container mx-auto px-4 py-16">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-neutral-900 mb-4">
          Welcome to Your Azure Learning Journey
        </h2>
        <p className="text-xl text-neutral-600 max-w-2xl mx-auto">
          Practice with real Azure services including Functions, Blob Storage,
          and Cosmos DB. Build production-ready microservices while preparing
          for AZ-204 and AZ-400 certifications.
        </p>
      </div>

      <AuthForm
        mode={authMode}
        onToggleMode={() =>
          setAuthMode(authMode === "login" ? "register" : "login")
        }
      />
    </section>
  );
};
