import React from 'react';
import type { NetworkStats, NetworkMetrics, AgentBehavior } from '../types';

interface StatsPanelProps {
  stats: NetworkStats;
  metrics?: NetworkMetrics;
}

const behaviorColors: Record<AgentBehavior, string> = {
  cooperative: '#3fb950',
  neutral: '#d29922',
  malicious: '#f85149',
  adversarial: '#bc8cff',
};

export const StatsPanel: React.FC<StatsPanelProps> = ({ stats, metrics }) => {
  // Trust distribution
  const trustDistribution = metrics?.trustDistribution || { high: 0, medium: 0, low: 0 };

  // Behavior distribution
  const behaviorDist = stats.trustDistribution;

  return (
    <div className="bg-[#161b22] border-r border-[#30363d] p-4 overflow-y-auto h-full">
      {/* Network Stats */}
      <div className="mb-6">
        <h3 className="text-xs uppercase tracking-wider text-[#8b949e] mb-3">Network Stats</h3>
        <div className="grid grid-cols-2 gap-2">
          <div className="stat-card">
            <div className="text-xl font-bold">{stats.totalAgents}</div>
            <div className="text-xs text-[#8b949e] mt-1">Agents</div>
          </div>
          <div className="stat-card">
            <div className="text-xl font-bold">{stats.totalRelations}</div>
            <div className="text-xs text-[#8b949e] mt-1">Relations</div>
          </div>
          <div className="stat-card">
            <div className="text-xl font-bold">{(stats.averageTrust * 100).toFixed(0)}%</div>
            <div className="text-xs text-[#8b949e] mt-1">Avg Trust</div>
          </div>
          <div className="stat-card">
            <div className="text-xl font-bold">
              {metrics ? (metrics.networkHealth * 100).toFixed(0) : 0}%
            </div>
            <div className="text-xs text-[#8b949e] mt-1">Health</div>
          </div>
        </div>
      </div>

      {/* Trust Distribution */}
      <div className="mb-6">
        <h3 className="text-xs uppercase tracking-wider text-[#8b949e] mb-3">Trust Distribution</h3>
        <div className="flex gap-3 mb-2 flex-wrap">
          <div className="flex items-center gap-1 text-xs text-[#8b949e]">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#3fb950' }}></div>
            High
          </div>
          <div className="flex items-center gap-1 text-xs text-[#8b949e]">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#d29922' }}></div>
            Medium
          </div>
          <div className="flex items-center gap-1 text-xs text-[#8b949e]">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#f85149' }}></div>
            Low
          </div>
        </div>
        <div className="bar-chart">
          <div
            className="bar"
            style={{
              height: `${trustDistribution.low * 100}%`,
              backgroundColor: '#f85149',
            }}
          ></div>
          <div
            className="bar"
            style={{
              height: `${trustDistribution.medium * 100}%`,
              backgroundColor: '#d29922',
            }}
          ></div>
          <div
            className="bar"
            style={{
              height: `${trustDistribution.high * 100}%`,
              backgroundColor: '#3fb950',
            }}
          ></div>
        </div>
      </div>

      {/* Behavior Distribution */}
      <div className="mb-6">
        <h3 className="text-xs uppercase tracking-wider text-[#8b949e] mb-3">Behavior Distribution</h3>
        {Object.entries(behaviorDist).map(([behavior, count]) => (
          <div key={behavior} className="mb-2">
            <div className="flex justify-between text-xs mb-1">
              <span style={{ color: behaviorColors[behavior as AgentBehavior] }}>{behavior}</span>
              <span className="text-[#8b949e]">{count}</span>
            </div>
            <div className="progress-bar">
              <div
                className="fill"
                style={{
                  width: `${(count / stats.totalAgents) * 100}%`,
                  backgroundColor: behaviorColors[behavior as AgentBehavior],
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      {/* Network Metrics */}
      {metrics && (
        <div>
          <h3 className="text-xs uppercase tracking-wider text-[#8b949e] mb-3">Network Metrics</h3>
          <div className="space-y-3">
            <div>
              <div className="text-xs text-[#8b949e] mb-1">Avg Reputation</div>
              <div className="text-base font-semibold">
                {(metrics.averageReputation * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div className="text-xs text-[#8b949e] mb-1">Confidence Index</div>
              <div className="text-base font-semibold">
                {(metrics.confidenceIndex * 100).toFixed(1)}%
              </div>
            </div>
            <div>
              <div className="text-xs text-[#8b949e] mb-1">Volatility Index</div>
              <div className="text-base font-semibold">
                {(metrics.volatilityIndex * 100).toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
