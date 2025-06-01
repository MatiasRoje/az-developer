import React from "react";
import { AuthContextProvider } from "./contexts/authContextProvider";
import { Navbar } from "./components/Navbar";
import { useAuth } from "./hooks/useAuth";
import { LandingPage } from "./pages/LandingPage";
import { DashboardPage } from "./pages/DashboardPage";

const AppContent: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <main className="min-h-screen bg-neutral-50">
      <Navbar />
      {isAuthenticated ? <DashboardPage /> : <LandingPage />}
    </main>
  );
};

const App: React.FC = () => {
  return (
    <AuthContextProvider>
      <AppContent />
    </AuthContextProvider>
  );
};

export default App;
