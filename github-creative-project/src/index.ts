/**
 * Main entry point for the 12-Factor Agents Explorer
 * 
 * This module serves as the primary entry point for the AI Agent Framework,
 * providing easy access to all agent types and utilities.
 */

export { BaseAgent, type AgentConfig, type AgentMemory, type AgentState } from './agents/BaseAgent';
export { MultimodalAgent, type MultimodalAgentConfig, type MultimodalInput, type Intent } from './agents/MultimodalAgent';
export { AdaptiveAgent, type AdaptiveConfig, type LearningExperience, type KnowledgeItem } from './agents/AdaptiveAgent';
export { CollaborativeCreationAgent, type CollaborativeConfig, type CreativeTask, type AgentRole, type CollaborationProtocol, type CreativeOutput } from './agents/CollaborativeCreationAgent';

// Framework utilities
export class AgentFramework {
  private agents: Map<string, any> = new Map();
  
  /**
   * Initialize the agent framework
   */
  async initialize() {
    console.log('🚀 Initializing 12-Factor Agents Explorer Framework...');
    
    // Initialize core agents
    await this.initializeCoreAgents();
    
    console.log('✅ Framework initialized successfully');
  }
  
  private async initializeCoreAgents() {
    // This would initialize the core agent types
    // Implementation would depend on the specific requirements
  }
  
  /**
   * Get a specific agent by name
   */
  getAgent(name: string) {
    return this.agents.get(name);
  }
  
  /**
   * Create a new agent instance
   */
  createAgent(type: string, config: any) {
    // Implementation for creating new agents
    return null;
  }
  
  /**
   * Run a comprehensive demo
   */
  async runDemo() {
    console.log('🎭 Starting comprehensive framework demo...');
    
    try {
      // Import and run the comprehensive demo
      const { runComprehensiveDemo } = await import('./examples/comprehensive-demo');
      await runComprehensiveDemo();
    } catch (error) {
      console.error('Demo error:', error);
    }
  }
}

// Create a singleton instance
export const framework = new AgentFramework();

// Initialize on import
framework.initialize().catch(console.error);

// Convenience exports for common use cases
export const createMultimodalAgent = (config: any) => new MultimodalAgent(config);
export const createAdaptiveAgent = (config: any) => new AdaptiveAgent(config);
export const createCollaborativeAgent = (config: any) => new CollaborativeCreationAgent(config);

// Version information
export const version = '1.0.0';
export const description = '12-Factor Agents Explorer - Creative AI Agent Framework';

// CLI interface for command-line usage
if (require.main === module) {
  console.log(`🤖 ${description}`);
  console.log(`Version: ${version}`);
  console.log('');
  
  // Parse command line arguments
  const args = process.argv.slice(2);
  
  if (args.includes('--demo') || args.includes('-d')) {
    framework.runDemo().catch(console.error);
  } else if (args.includes('--help') || args.includes('-h')) {
    console.log('Usage:');
    console.log('  node dist/index.js [options]');
    console.log('');
    console.log('Options:');
    console.log('  -d, --demo    Run comprehensive demo');
    console.log('  -h, --help   Show this help message');
    console.log('  -v, --version Show version information');
  } else if (args.includes('--version') || args.includes('-v')) {
    console.log(version);
  } else {
    console.log('Use --help for available options');
    console.log('Use --demo to run the comprehensive demonstration');
  }
}