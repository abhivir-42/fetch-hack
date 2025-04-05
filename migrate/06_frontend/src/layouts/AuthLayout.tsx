import React, { ReactNode } from 'react';
import { useTheme } from '../contexts/ThemeContext';

// Icons
const SunIcon = () => <span>☀️</span>;
const MoonIcon = () => <span>🌙</span>;

interface AuthLayoutProps {
  children: ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <header className="p-4 flex justify-end">
        <button
          onClick={toggleTheme}
          className="p-2 rounded-full bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 shadow-sm"
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
        </button>
      </header>
      
      <main className="flex-grow flex items-center justify-center">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">CryptoFund</h1>
            <p className="mt-2 text-gray-600 dark:text-gray-400">AI-Powered Crypto Hedge Fund Manager</p>
          </div>
          
          {children}
        </div>
      </main>
      
      <footer className="p-4 text-center text-sm text-gray-500 dark:text-gray-400">
        &copy; {new Date().getFullYear()} CryptoFund. All rights reserved.
      </footer>
    </div>
  );
};

export default AuthLayout; 