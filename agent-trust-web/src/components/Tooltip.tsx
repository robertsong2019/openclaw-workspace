import React from 'react';

interface TooltipProps {
  agent: {
    name: string;
    behavior: string;
    trustScore: number;
    interactions: number;
    successRate: number;
  } | null;
  position: { x: number; y: number };
}

const behaviorColors: Record<string, string> = {
  cooperative: '#3fb950',
  neutral: '#d29922',
  malicious: '#f85149',
  adversarial: '#bc8cff',
};

export const Tooltip: React.FC<TooltipProps> = ({ agent, position }) => {
  if (!agent) return null;

  return (
    <div
      className="tooltip show"
      style={{
        left: `${position.x + 12}px`,
        top: `${position.y - 10}px`,
      }}
    >
      <div className="font-semibold text-sm mb-2" style={{ color: behaviorColors[agent.behavior] }}>
        {agent.name}
      </div>
      <div className="flex justify-between gap-3 text-xs text-[#8b949e] mb-1">
        <span>Behavior</span>
        <span className="text-[#c9d1d9]">{agent.behavior}</span>
      </div>
      <div className="flex justify-between gap-3 text-xs text-[#8b949e] mb-1">
        <span>Trust Score</span>
        <span className="text-[#c9d1d9] font-numeric">{(agent.trustScore * 100).toFixed(1)}%</span>
      </div>
      <div className="flex justify-between gap-3 text-xs text-[#8b949e] mb-1">
        <span>Interactions</span>
        <span className="text-[#c9d1d9] font-numeric">{agent.interactions}</span>
      </div>
      <div className="flex justify-between gap-3 text-xs text-[#8b949e]">
        <span>Success Rate</span>
        <span className="text-[#c9d1d9] font-numeric">{(agent.successRate * 100).toFixed(1)}%</span>
      </div>
    </div>
  );
};
