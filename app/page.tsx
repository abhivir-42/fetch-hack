import Image from 'next/image';
import Link from 'next/link';
import MainLayout from './components/MainLayout';

export default function Home() {
  return (
    <MainLayout>
      <section className="pt-8 pb-16 md:pt-16 md:pb-24">
        <div className="flex flex-col md:flex-row items-center">
          <div className="md:w-1/2 mb-10 md:mb-0">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              AI-Powered Crypto <span className="gradient-text">Trading Decisions</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              Fetch Fund uses advanced AI agents to analyze market sentiment and make data-driven
              trading recommendations for your crypto investments.
            </p>
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
              <Link 
                href="/trade" 
                className="btn btn-primary px-8 py-3 text-center"
              >
                Start Trading
              </Link>
              <Link 
                href="/dashboard" 
                className="btn btn-outline px-8 py-3 text-center"
              >
                View Dashboard
              </Link>
            </div>
          </div>
          <div className="md:w-1/2 flex justify-center">
            <div className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-primary to-secondary rounded-lg blur opacity-20 group-hover:opacity-30 transition-all duration-1000"></div>
              <Image
                src="/fetch_fund_logo.png"
                alt="Fetch Fund"
                width={420}
                height={420}
                className="rounded-lg shadow-lg relative transform transition-all duration-500 group-hover:scale-[1.02]"
              />
            </div>
          </div>
        </div>
      </section>

      <section className="py-16 bg-gradient-to-b from-gray-50 to-white rounded-xl shadow-sm">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">How It Works</h2>
          <p className="text-gray-600 max-w-3xl mx-auto text-lg">
            Our platform leverages multiple AI agents to analyze market data, news, and sentiment
            to provide you with the most informed trading decisions.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
          <div className="card group hover:bg-gray-50 transition-all duration-300 p-8">
            <div className="w-16 h-16 rounded-full bg-tertiary flex items-center justify-center mx-auto mb-6 transition-all duration-300 group-hover:bg-secondary/20">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary transition-colors duration-300 group-hover:text-secondary" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center">Real-time Analysis</h3>
            <p className="text-gray-600 text-center">
              Our agents constantly monitor market conditions, news, and sentiment indicators to provide up-to-date insights.
            </p>
          </div>

          <div className="card group hover:bg-gray-50 transition-all duration-300 p-8">
            <div className="w-16 h-16 rounded-full bg-tertiary flex items-center justify-center mx-auto mb-6 transition-all duration-300 group-hover:bg-secondary/20">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary transition-colors duration-300 group-hover:text-secondary" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center">AI Decision Making</h3>
            <p className="text-gray-600 text-center">
              Multiple AI models evaluate data and collaborate to reach the optimal trading decision with high confidence.
            </p>
          </div>

          <div className="card group hover:bg-gray-50 transition-all duration-300 p-8">
            <div className="w-16 h-16 rounded-full bg-tertiary flex items-center justify-center mx-auto mb-6 transition-all duration-300 group-hover:bg-secondary/20">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-primary transition-colors duration-300 group-hover:text-secondary" viewBox="0 0 20 20" fill="currentColor">
                <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center">Automated Trading</h3>
            <p className="text-gray-600 text-center">
              Execute trades automatically or receive notifications about recommended actions based on real-time analysis.
            </p>
          </div>
        </div>
      </section>
      
      <section className="py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-gray-600 max-w-2xl mx-auto text-lg mb-8">
            Take control of your crypto investments with AI-powered insights today.
          </p>
          <Link href="/trade" className="btn btn-primary px-8 py-3 text-lg">
            Start Now
          </Link>
        </div>
      </section>
    </MainLayout>
  );
}