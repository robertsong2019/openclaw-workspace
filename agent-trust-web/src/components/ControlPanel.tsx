import React, { useState } from 'react';
import type { AgentBehavior } from '../types';

interface ControlPanelProps {
  onSimulate: (steps: number) => void;
  onReset: () => void;
  onAddAgent: (name: string, behavior: AgentBehavior) => void;
  stepCount: number;
  isSimulating?: boolean;
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  onSimulate,
  onReset,
  onAddAgent,
  stepCount,
  isSimulating = false,
}) => {
  const [agentName, setAgentName] = useState('');
  const [agentBehavior, setAgentBehavior] = useState<AgentBehavior>('cooperative');

  const handleAddAgent = () => {
    if (!agentName.trim()) return;
    onAddAgent(agentName.trim(), agentBehavior);
    setAgentName('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAddAgent();
    }
  };

  return (
    <div className="panel bg-[#161b22] border-r border-[#30363d] p-4 overflow-y-auto h-full">
      {/* Simulation Controls */}
      <div className="mb-6">
        <h3 className="text-xs uppercase tracking-wider text-[#8b949e] mb-3">Simulation</h3>
        <div className="flex gap-2 mb-2">
          <button
            className="btn btn-primary flex-1"
            onClick={() => onSimulate(1)}
            disabled={isSimulating}
          >
            Step ▶
          </button>
          <button
            className="btn btn-primary flex-1"
            onClick={() => onSimulate(10)}
            disabled={isSimulating}
          >
            ×10 ⏩
          </button>
        </div>
        <div className="flex gap-2">
          <button
            className="btn btn-secondary flex-1"
            onClick={() => onSimulate(50)}
            disabled={isSimulating}
          >
            ×50
          </button>
          <button
            className="btn btn-danger flex-1"
            onClick={onReset}
            disabled={isSimulating}
          >
            Reset
          </button>
        </div>
        <div className="mt-3 text-center text-sm text-[#8b949e]">
          Step {stepCount}
        </div>
      </div>

      {/* Add Agent */}
      <div className="mb-6">
        <h3 className="text-xs uppercase tracking-wider text-[#8b949e] mb-3">Add Agent</h3>
        <div className="mb-2">
          <label className="block text-xs text-[#8b949e] mb-1">Name</label>
          <input
            type="text"
            className="input-field"
            placeholder="Agent name..."
            value={agentName}
            onChange={(e) => setAgentName(e.target.value)}
            onKeyPress={handleKeyPress}
          />
        </div>
        <div className="mb-3">
          <label className="block text-xs text-[#8b949e] mb-1">Behavior</label>
          <select
            className="input-field"
            value={agentBehavior}
            onChange={(e) => setAgentBehavior(e.target.value as AgentBehavior)}
          >
            <option value="cooperative">🟢 Cooperative</option>
            <option value="neutral">🟡 Neutral</option>
            <option value="malicious">🔴 Malicious</option>
            <option value="adversarial">⚫ Adversarial</option>
          </select>
        </div>
        <button className="btn btn-primary w-full" onClick={handleAddAgent}>
          Add Agent
        </button>
      </div>
    </div>
  );
};
