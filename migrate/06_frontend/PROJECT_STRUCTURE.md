# CryptoFund Frontend Project Structure

This document outlines the organization of the CryptoFund frontend web application.

## Directory Structure

```
migrate/06_frontend/
├── public/                    # Static assets
│   ├── index.html             # HTML entry point
│   ├── favicon.ico            # Favicon
│   └── assets/                # Images, icons, etc.
├── src/                       # Source code
│   ├── api/                   # API integration services
│   │   ├── auth.ts            # Authentication API
│   │   ├── wallet.ts          # Wallet API
│   │   ├── market.ts          # Market data API
│   │   ├── transactions.ts    # Transaction API
│   │   └── agents.ts          # Agent interaction API
│   ├── components/            # Reusable UI components
│   │   ├── common/            # Generic components
│   │   ├── auth/              # Authentication components
│   │   ├── dashboard/         # Dashboard components
│   │   ├── wallet/            # Wallet components
│   │   ├── charts/            # Data visualization components
│   │   └── forms/             # Input forms
│   ├── contexts/              # React contexts
│   │   ├── AuthContext.tsx    # Authentication state
│   │   ├── ThemeContext.tsx   # Theme state (dark/light)
│   │   └── WalletContext.tsx  # Wallet connection state
│   ├── hooks/                 # Custom React hooks
│   │   ├── useAuth.ts         # Authentication hook
│   │   ├── useWallet.ts       # Wallet hook
│   │   └── useTheme.ts        # Theme hook
│   ├── layouts/               # Page layouts
│   │   ├── MainLayout.tsx     # Main application layout
│   │   └── AuthLayout.tsx     # Authentication layout
│   ├── pages/                 # Page components
│   │   ├── Login.tsx          # Login page
│   │   ├── Dashboard.tsx      # Main dashboard
│   │   ├── Transactions.tsx   # Transaction history
│   │   ├── Settings.tsx       # User settings
│   │   └── NotFound.tsx       # 404 page
│   ├── styles/                # Global styles
│   │   ├── tailwind.css       # Tailwind imports
│   │   └── globals.css        # Global CSS
│   ├── types/                 # TypeScript type definitions
│   │   ├── api.ts             # API response types
│   │   ├── wallet.ts          # Wallet types
│   │   └── agents.ts          # Agent types
│   ├── utils/                 # Utility functions
│   │   ├── formatting.ts      # Data formatting
│   │   ├── validation.ts      # Form validation
│   │   └── storage.ts         # Local storage helpers
│   ├── App.tsx                # Main App component
│   ├── index.tsx              # Application entry point
│   └── routes.tsx             # Application routes
├── package.json               # Dependencies and scripts
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.js         # Tailwind CSS configuration
├── postcss.config.js          # PostCSS configuration
├── vite.config.ts             # Vite configuration
└── README.md                  # Project documentation
```

## Component Organization

### Common Components
Generic, reusable UI components used throughout the application.

### Page Components
Top-level components rendered for each route in the application.

### Feature Components
Components specific to certain features, organized in feature-specific directories.

## State Management

The application uses React Context API for state management, with dedicated contexts for:
- Authentication state
- Theme preferences
- Wallet connections

## API Integration

API services are organized by domain:
- Authentication
- Wallet management
- Market data
- Transaction management
- Agent interaction

## Styling Approach

The application uses Tailwind CSS for styling, with:
- A consistent color scheme
- Responsive design patterns
- Dark/light mode support 