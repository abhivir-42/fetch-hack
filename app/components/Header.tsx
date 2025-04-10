import Image from 'next/image';
import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-3">
          <Image 
            src="/fetch_fund_logo.png" 
            alt="Fetch Fund Logo" 
            width={40} 
            height={40}
            priority
          />
          <h1 className="text-xl font-bold text-primary">Fetch Fund</h1>
        </Link>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <Link href="/" className="text-gray-600 hover:text-primary">
                Home
              </Link>
            </li>
            <li>
              <Link href="/dashboard" className="text-gray-600 hover:text-primary">
                Dashboard
              </Link>
            </li>
            <li>
              <Link href="/trade" className="text-gray-600 hover:text-primary">
                Trade
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
} 