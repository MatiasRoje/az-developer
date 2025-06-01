import { useAuth } from "../hooks/useAuth";

export const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();

  return isAuthenticated ? (
    <nav className="bg-white shadow-sm border-b border-neutral-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-neutral-900">
            Azure Developer Certification Suite
          </h1>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <span className="text-neutral-700 font-medium">{user?.name}</span>
            </div>
            <button onClick={logout} className="azure-button-secondary">
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </nav>
  ) : (
    <nav className="bg-white shadow-sm border-b border-neutral-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-neutral-900">
            Azure Developer Certification Suite
          </h1>
        </div>
      </div>
    </nav>
  );
};
