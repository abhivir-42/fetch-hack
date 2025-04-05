import React from 'react';
import { BrowserRouter, useRoutes } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import { WalletProvider } from './contexts/WalletContext';
import { routes } from './routes';

// Router component
const AppRoutes: React.FC = () => {
  const routeElements = useRoutes(routes);
  return routeElements;
};

const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <WalletProvider>
          <BrowserRouter>
            <AppRoutes />
          </BrowserRouter>
        </WalletProvider>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
