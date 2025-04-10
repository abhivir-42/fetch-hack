import React from 'react';
import Header from './Header';
import Footer from './Footer';

interface MainLayoutProps {
  children: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-background to-white">
      <Header />
      <main className="flex-grow container mx-auto px-4 py-8 md:py-12 transition-all duration-300">
        {children}
      </main>
      <Footer />
    </div>
  );
} 