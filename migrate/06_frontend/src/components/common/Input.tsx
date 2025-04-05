import React, { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  fullWidth = true,
  className = '',
  ...props
}) => {
  const inputClasses = `
    block rounded-md border-0 py-1.5 text-gray-900 dark:text-white 
    shadow-sm ring-1 ring-inset focus:ring-2 focus:ring-inset 
    ${error 
      ? 'ring-red-500 focus:ring-red-500' 
      : 'ring-gray-300 dark:ring-gray-700 focus:ring-indigo-600'
    }
    placeholder:text-gray-400
    bg-white dark:bg-gray-700
    sm:text-sm sm:leading-6
    ${fullWidth ? 'w-full' : 'w-auto'}
    ${className}
  `;

  return (
    <div className={fullWidth ? 'w-full' : 'w-auto'}>
      {label && (
        <label 
          htmlFor={props.id} 
          className="block text-sm font-medium leading-6 text-gray-900 dark:text-gray-200 mb-1"
        >
          {label}
        </label>
      )}
      <input className={inputClasses} {...props} />
      {error && (
        <p className="mt-1 text-sm text-red-600 dark:text-red-500">{error}</p>
      )}
    </div>
  );
};

export default Input; 