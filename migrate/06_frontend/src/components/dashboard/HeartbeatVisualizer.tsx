import React, { useEffect, useRef } from 'react';
import { HeartbeatData } from '../../types/api';
import Card from '../common/Card';
import { HeartIcon, ExclamationTriangleIcon, XCircleIcon } from '@heroicons/react/24/solid';

interface HeartbeatVisualizerProps {
  heartbeatData: HeartbeatData | null;
  isLoading: boolean;
  error: string | null;
}

const HeartbeatVisualizer: React.FC<HeartbeatVisualizerProps> = ({
  heartbeatData,
  isLoading,
  error,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  // Heartbeat animation
  useEffect(() => {
    if (!heartbeatData || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    let frameId: number;
    let t = 0;
    
    // Resize canvas to match parent dimensions
    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    
    // Initial resize
    resize();
    
    // Set up resize listener
    window.addEventListener('resize', resize);
    
    // Define colors based on status
    const getLineColor = () => {
      switch (heartbeatData.status) {
        case 'healthy':
          return '#10B981'; // green-500
        case 'warning':
          return '#F59E0B'; // amber-500
        case 'error':
          return '#EF4444'; // red-500
        default:
          return '#6B7280'; // gray-500
      }
    };
    
    // Heartbeat line animation
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const w = canvas.width;
      const h = canvas.height;
      const baseY = h / 2;
      const amplitude = h / 4;
      const frequency = 0.05;
      const lineWidth = 3;
      
      // Set line style
      ctx.lineWidth = lineWidth;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.strokeStyle = getLineColor();
      
      // Begin drawing path
      ctx.beginPath();
      ctx.moveTo(0, baseY);
      
      // Draw heartbeat line
      for (let x = 0; x < w; x++) {
        // Create a heartbeat effect with periodic spikes
        let y = baseY;
        
        // Normal sine wave
        y += Math.sin((x + t) * frequency) * (amplitude / 3);
        
        // Add heartbeat spike every so often
        const spikeInterval = w / 3;
        const distanceToSpike1 = Math.abs(x - (w / 3 + t % spikeInterval));
        const distanceToSpike2 = Math.abs(x - (2 * w / 3 + t % spikeInterval));
        
        if (distanceToSpike1 < 20) {
          const spikeHeight = (1 - distanceToSpike1 / 20) * amplitude;
          y -= spikeHeight;
        } else if (distanceToSpike2 < 30) {
          const spikeHeight = (1 - distanceToSpike2 / 30) * amplitude * 0.8;
          y -= spikeHeight;
        }
        
        ctx.lineTo(x, y);
      }
      
      // Stroke the path
      ctx.stroke();
      
      // Update animation state
      t += 2;
      
      // Continue animation loop
      frameId = requestAnimationFrame(animate);
    };
    
    // Start animation
    animate();
    
    // Clean up
    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(frameId);
    };
  }, [heartbeatData]);
  
  // Get status icon and color
  const getStatusDisplay = () => {
    if (isLoading) {
      return { 
        icon: <HeartIcon className="h-8 w-8 text-gray-400 animate-pulse" />,
        color: 'bg-gray-100 dark:bg-gray-700',
        text: 'Loading...'
      };
    }
    
    if (error) {
      return {
        icon: <XCircleIcon className="h-8 w-8 text-red-500" />,
        color: 'bg-red-100 dark:bg-red-900',
        text: error
      };
    }
    
    if (!heartbeatData) {
      return {
        icon: <ExclamationTriangleIcon className="h-8 w-8 text-amber-500" />,
        color: 'bg-amber-100 dark:bg-amber-900',
        text: 'No heartbeat data'
      };
    }
    
    switch (heartbeatData.status) {
      case 'healthy':
        return {
          icon: <HeartIcon className="h-8 w-8 text-green-500 animate-pulse" />,
          color: 'bg-green-100 dark:bg-green-900',
          text: heartbeatData.response.message
        };
      case 'warning':
        return {
          icon: <ExclamationTriangleIcon className="h-8 w-8 text-amber-500" />,
          color: 'bg-amber-100 dark:bg-amber-900',
          text: heartbeatData.response.message
        };
      case 'error':
        return {
          icon: <XCircleIcon className="h-8 w-8 text-red-500" />,
          color: 'bg-red-100 dark:bg-red-900',
          text: heartbeatData.response.message
        };
      default:
        return {
          icon: <HeartIcon className="h-8 w-8 text-gray-500" />,
          color: 'bg-gray-100 dark:bg-gray-700',
          text: 'Unknown status'
        };
    }
  };
  
  const { icon, color, text } = getStatusDisplay();
  
  // Format date string
  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <Card title="System Heartbeat" className="mb-6">
      <div className="mb-4">
        <div className={`flex items-center p-4 rounded-lg ${color}`}>
          <div className="mr-4">{icon}</div>
          <div>
            <div className="font-medium text-gray-900 dark:text-white">
              {text}
            </div>
            {heartbeatData && (
              <div className="text-sm text-gray-600 dark:text-gray-300">
                Last updated: {formatTimestamp(heartbeatData.timestamp)}
              </div>
            )}
          </div>
        </div>
      </div>
      
      <div className="h-32 w-full">
        <canvas ref={canvasRef} className="w-full h-full"></canvas>
      </div>
      
      {heartbeatData && (
        <div className="mt-4 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Trading Enabled:</span>
            <span className={heartbeatData.response.tradingEnabled ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}>
              {heartbeatData.response.tradingEnabled ? 'Yes' : 'No'}
            </span>
          </div>
        </div>
      )}
    </Card>
  );
};

export default HeartbeatVisualizer; 