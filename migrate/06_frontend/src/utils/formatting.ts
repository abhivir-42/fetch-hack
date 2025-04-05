/**
 * Format a number as currency with USD symbol and 2 decimal places
 * @param value - The number to format
 * @param options - Formatting options
 * @returns Formatted currency string
 */
export const formatCurrency = (
  value: number, 
  options: { 
    currency?: string;
    minimumFractionDigits?: number;
    maximumFractionDigits?: number;
  } = {}
): string => {
  const { 
    currency = 'USD', 
    minimumFractionDigits = 2, 
    maximumFractionDigits = 2 
  } = options;
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits,
    maximumFractionDigits,
  }).format(value);
};

/**
 * Format a number as a percentage with a + sign for positive values
 * @param value - The number to format as a percentage
 * @param options - Formatting options
 * @returns Formatted percentage string
 */
export const formatPercentage = (
  value: number,
  options: {
    showPlusSign?: boolean;
    decimalPlaces?: number;
  } = {}
): string => {
  const { showPlusSign = true, decimalPlaces = 2 } = options;
  
  const sign = value > 0 && showPlusSign ? '+' : '';
  return `${sign}${value.toFixed(decimalPlaces)}%`;
};

/**
 * Format a date string in a user-friendly way
 * @param dateString - ISO date string to format
 * @param options - Formatting options
 * @returns Formatted date string
 */
export const formatDate = (
  dateString: string,
  options: {
    includeTime?: boolean;
    format?: 'short' | 'medium' | 'long';
  } = {}
): string => {
  const { includeTime = false, format = 'medium' } = options;
  const date = new Date(dateString);
  
  const dateOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: format === 'short' ? 'numeric' : format === 'medium' ? 'short' : 'long',
    day: 'numeric',
    hour: includeTime ? '2-digit' : undefined,
    minute: includeTime ? '2-digit' : undefined,
  };
  
  return new Intl.DateTimeFormat('en-US', dateOptions).format(date);
};

/**
 * Truncate text to a specified length with an ellipsis
 * @param text - The text to truncate
 * @param maxLength - Maximum length before truncating
 * @returns Truncated text with ellipsis if needed
 */
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Format a number to have a specific number of decimal places
 * @param value - The number to format
 * @param options - Formatting options
 * @returns Formatted number string
 */
export const formatNumber = (
  value: number,
  options: {
    minimumFractionDigits?: number;
    maximumFractionDigits?: number;
  } = {}
): string => {
  const { 
    minimumFractionDigits = 0, 
    maximumFractionDigits = 2 
  } = options;
  
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits,
    maximumFractionDigits,
  }).format(value);
}; 