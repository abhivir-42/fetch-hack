export default function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-gradient-to-r from-gray-50 to-gray-100 mt-auto border-t border-gray-200">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-gray-600 font-medium">
              © {currentYear} Fetch Fund. All rights reserved.
            </p>
          </div>
          <div className="flex space-x-6">
            <a href="#" className="text-gray-600 hover:text-primary transition-colors duration-200">
              Terms
            </a>
            <a href="#" className="text-gray-600 hover:text-primary transition-colors duration-200">
              Privacy
            </a>
            <a href="#" className="text-gray-600 hover:text-primary transition-colors duration-200">
              Contact
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
} 