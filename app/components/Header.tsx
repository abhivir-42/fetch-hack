'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();
  
  const isActive = (path: string) => {
    return pathname === path;
  };

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-3 group">
          <div className="relative overflow-hidden rounded-full h-10 w-10 bg-primary/5 flex items-center justify-center transition-all duration-300 group-hover:bg-primary/10">
            <Image 
              src="/fetch_fund_logo.png" 
              alt="Fetch Fund Logo" 
              width={36} 
              height={36}
              className="transition-transform duration-500 group-hover:scale-110"
              priority
            />
          </div>
          <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Fetch Fund</h1>
        </Link>
        <nav className="hidden md:block">
          <ul className="flex space-x-8">
            <li>
              <Link 
                href="/" 
                className={`px-2 py-1 font-medium transition-colors duration-200 border-b-2 ${
                  isActive('/') 
                    ? 'border-primary text-primary' 
                    : 'border-transparent text-gray-600 hover:text-primary hover:border-primary/30'
                }`}
              >
                Home
              </Link>
            </li>
            <li>
              <Link 
                href="/dashboard" 
                className={`px-2 py-1 font-medium transition-colors duration-200 border-b-2 ${
                  isActive('/dashboard') 
                    ? 'border-primary text-primary' 
                    : 'border-transparent text-gray-600 hover:text-primary hover:border-primary/30'
                }`}
              >
                Dashboard
              </Link>
            </li>
            <li>
              <Link 
                href="/trade" 
                className={`px-2 py-1 font-medium transition-colors duration-200 border-b-2 ${
                  isActive('/trade') 
                    ? 'border-primary text-primary' 
                    : 'border-transparent text-gray-600 hover:text-primary hover:border-primary/30'
                }`}
              >
                Trade
              </Link>
            </li>
          </ul>
        </nav>
        
        {/* Mobile menu button - you would implement the mobile menu functionality separately */}
        <button className="md:hidden text-gray-600 hover:text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </header>
  );
} 