export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  description: string;
  status: AgentStatus;
  lastActive?: string;
  metadata?: Record<string, any>;
}

export type AgentType = 
  | 'main'
  | 'heartbeat'
  | 'swap'
  | 'market'
  | 'news'
  | 'analysis'
  | 'topup'
  | 'reward';

export type AgentStatus = 'online' | 'offline' | 'error' | 'pending';

export interface AgentMessage {
  agentId: string;
  timestamp: string;
  content: string;
  type: 'info' | 'warning' | 'error' | 'success';
  data?: Record<string, any>;
}

export interface AgentDecision {
  agentId: string;
  timestamp: string;
  action: string;
  reasoning: string;
  confidence: number;
  parameters: Record<string, any>;
} 