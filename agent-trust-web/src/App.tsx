import React, { useState, useEffect, useCallback } from 'react';
import { trustNetwork } from './trustNetwork';
import {
  NetworkGraph,
  ControlPanel,
  StatsPanel,
  AgentDetailsPanel,
  Header,
  Tooltip,
} from './components';
import type { AgentBehavior } from './types';

function App() {
  const [networkData, setNetworkData] = useState(trustNetwork.getNetworkData());
  const [selectedAgentId, setSelectedAgentId] = useState<string | null>(null);
  const [hoveredAgentId, setHoveredAgentId] = useState<string | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [isSimulating, setIsSimulating] = useState(false);

  // Refresh network data
  const refreshData = useCallback(() => {
    setNetworkData(trustNetwork.getNetworkData());
  }, []);

  // Initial data load
  useEffect(() => {
    refreshData();
  }, [refreshData]);

  // Handle simulation
  const handleSimulate = (steps: number) => {
    setIsSimulating(true);
    // Use setTimeout to allow UI to update
    setTimeout(() => {
      trustNetwork.simulate(steps);
      refreshData();
      setIsSimulating(false);
    }, 100);
  };

  // Handle reset
  const handleReset = () => {
    trustNetwork.reset();
    setSelectedAgentId(null);
    refreshData();
  };

  // Handle add agent
  const handleAddAgent = (name: string, behavior: AgentBehavior) => {
    const id = name.toLowerCase().replace(/\s+/g, '-');
    trustNetwork.addAgent({ id, name, behavior });
    refreshData();
  };

  // Handle delete agent
  const handleDeleteAgent = (agentId: string) => {
    trustNetwork.removeAgent(agentId);
    if (selectedAgentId === agentId) {
      setSelectedAgentId(null);
    }
    refreshData();
  };

  // Handle node click
  const handleNodeClick = (agentId: string) => {
    setSelectedAgentId(agentId);
  };

  // Handle node hover
  const handleNodeHover = useCallback((agentId: string | null, event?: React.MouseEvent) => {
    setHoveredAgentId(agentId);
    if (event) {
      setTooltipPosition({ x: event.clientX, y: event.clientY });
    }
  }, []);

  // Handle export
  const handleExport = () => {
    const config = trustNetwork.exportConfig();
    const blob = new Blob([config], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `trust-network-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Handle import
  const handleImport = (data: string) => {
    try {
      trustNetwork.importConfig(data);
      setSelectedAgentId(null);
      refreshData();
    } catch (e) {
      console.error('Failed to import:', e);
      alert('Failed to import network configuration');
    }
  };

  const hoveredAgent = networkData.agents.find(a => a.id === hoveredAgentId);

  return (
    <div className="w-full h-screen flex flex-col bg-[#0d1117]">
      <Header onExport={handleExport} onImport={handleImport} />

      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel: Controls & Stats */}
        <div className="w-72 flex flex-col border-r border-[#30363d]">
          <ControlPanel
            onSimulate={handleSimulate}
            onReset={handleReset}
            onAddAgent={handleAddAgent}
            stepCount={networkData.stepCount}
            isSimulating={isSimulating}
          />
          <div className="flex-1 overflow-hidden">
            <StatsPanel stats={networkData.stats} metrics={networkData.metrics} />
          </div>
        </div>

        {/* Center: Network Graph */}
        <div className="flex-1 relative" id="graph-container">
          <NetworkGraph
            agents={networkData.agents}
            relations={networkData.relations}
            onNodeClick={handleNodeClick}
            onNodeHover={(agentId) => handleNodeHover(agentId)}
          />
          {hoveredAgent && <Tooltip agent={hoveredAgent} position={tooltipPosition} />}
        </div>

        {/* Right Panel: Agent Details */}
        <div className="w-80">
          <AgentDetailsPanel
            agents={networkData.agents}
            selectedAgentId={selectedAgentId}
            onAgentSelect={setSelectedAgentId}
            onAgentDelete={handleDeleteAgent}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
