import React, { useState, useEffect } from 'react';
import type { Agent, AgentMetrics } from '../types';
import { trustNetwork } from '../trustNetwork';

interface AgentDetailsPanelProps {
  agents: Agent[];
  selectedAgentId: string | null;
  onAgentSelect: (agentId: string | null) => void;
  onAgentDelete?: (agentId: string) => void;
}

const behaviorColors: Record<string, string> = {
  cooperative: '#3fb950',
  neutral: '#d29922',
  malicious: '#f85149',
  adversarial: '#bc8cff',
};

export const AgentDetailsPanel: React.FC<AgentDetailsPanelProps> = ({
  agents,
  selectedAgentId,
  onAgentSelect,
  onAgentDelete,
}) => {
  const [metrics, setMetrics] = useState<AgentMetrics | null>(null);
  const selectedAgent = agents.find(a => a.id === selectedAgentId);

  useEffect(() => {
    if (selectedAgentId) {
      setMetrics(trustNetwork.getAgentMetrics(selectedAgentId));
    } else {
      setMetrics(null);
    }
  }, [selectedAgentId, agents]);

  const sortedAgents = [...agents].sort((a, b) => b.trustScore - a.trustScore);

  return (
    <div className="panel-right bg-[#161b22] border-l border-[#30363d] p-4 overflow-y-auto h-full">
      {/* Selected Agent Details */}
      {selectedAgent && (
        <div className="mb-6">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-xs uppercase tracking-wider text-[#8b949e]">Selected Agent</h3>
            <button
              className="text-xs text-[#f85149] hover:underline"
              onClick={() => onAgentSelect(null)}
            >
              Close
            </button>
          </div>
          <div className="card mb-3">
            <div className="flex items-center gap-2 mb-3">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: behaviorColors[selectedAgent.behavior] }}
              ></div>
              <div className="font-semibold">{selectedAgent.name}</div>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <div className="text-xs text-[#8b949e]">Behavior</div>
                <div>{selectedAgent.behavior}</div>
              </div>
              <div>
                <div className="text-xs text-[#8b949e]">Trust Score</div>
                <div>{(selectedAgent.trustScore * 100).toFixed(1)}%</div>
              </div>
              <div>
                <div className="text-xs text-[#8b949e]">Interactions</div>
                <div>{selectedAgent.interactions}</div>
              </div>
              <div>
                <div className="text-xs text-[#8b949e]">Success Rate</div>
                <div>{(selectedAgent.successRate * 100).toFixed(1)}%</div>
              </div>
            </div>
            {metrics && (
              <div className="mt-3 pt-3 border-t border-[#30363d]">
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <div className="text-xs text-[#8b949e]">Trend</div>
                    <div className={metrics.trend === 'rising' ? 'text-[#3fb950]' : metrics.trend === 'falling' ? 'text-[#f85149]' : ''}>
                      {metrics.trend}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-[#8b949e]">Reliability</div>
                    <div className={
                      metrics.reliability === 'high' ? 'text-[#3fb950]' :
                      metrics.reliability === 'low' ? 'text-[#f85149]' : ''
                    }>
                      {metrics.reliability}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
          {onAgentDelete && (
            <button
              className="btn btn-danger w-full text-xs"
              onClick={() => onAgentDelete(selectedAgent.id)}
            >
              Delete Agent
            </button>
          )}
        </div>
      )}

      {/* Agent Leaderboard */}
      <div>
        <h3 className="text-xs uppercase tracking-wider text-[#8b949e] mb-3">Agent Leaderboard</h3>
        <div className="space-y-1">
          {sortedAgents.map(agent => (
            <div
              key={agent.id}
              className={`agent-row ${selectedAgentId === agent.id ? 'bg-[#30363d]' : ''}`}
              onClick={() => onAgentSelect(agent.id)}
            >
              <div
                className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                style={{ backgroundColor: behaviorColors[agent.behavior] }}
              ></div>
              <div className="flex-1 text-sm truncate">{agent.name}</div>
              <div className="text-xs text-[#8b949e] font-numeric">
                {(agent.trustScore * 100).toFixed(0)}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
