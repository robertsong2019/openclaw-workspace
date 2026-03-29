/**
 * Collaborative Creation Agent Example
 * 
 * Demonstrates the CollaborativeCreationAgent's ability to coordinate
 * multiple specialized agents for creative tasks.
 */

import { CollaborativeCreationAgent, CollaborativeConfig } from '../src/agents/CollaborativeCreationAgent';

async function demonstrateCollaborativeAgent() {
  console.log('🤝 Collaborative Creation Agent Example');
  console.log('='.repeat(50));
  
  // Create a collaborative creation agent
  const config: CollaborativeConfig = {
    name: 'collaborative-creator',
    capabilities: ['coordination', 'quality_control', 'innovation'],
    maxAgents: 5,
    enableQualityControl: true,
    enableConflictResolution: true,
    enableInnovationBoost: true
  };
  
  const agent = new CollaborativeCreationAgent(config);
  
  await agent.start();
  
  // Test creative tasks
  const creativeTasks = [
    {
      input: 'Create a comprehensive blog post about the future of artificial intelligence in healthcare',
      type: 'content_creation' as const,
      description: 'Healthcare AI blog post creation'
    },
    {
      input: 'Generate a Python script for data analysis with machine learning',
      type: 'code_generation' as const,
      description: 'Data analysis code generation'
    },
    {
      input: 'Design a user interface for a mobile fitness tracking app',
      type: 'design' as const,
      description: 'Mobile app UI design'
    },
    {
      input: 'Research and summarize the latest developments in quantum computing',
      type: 'research' as const,
      description: 'Quantum computing research'
    }
  ];
  
  console.log('\n🎨 Testing collaborative creative tasks:');
  
  for (const task of creativeTasks) {
    console.log(`\n🔍 ${task.description}`);
    console.log(`Task: "${task.input}"`);
    
    try {
      const response = await agent.process(task.input);
      console.log(`Coordination response: ${response}`);
      
      // Get collaboration status
      setTimeout(async () => {
        try {
          const status = await agent.getCollaborationStatus();
          console.log(`Active tasks: ${status.activeTasks.length}`);
          console.log(`Available agents: ${status.availableAgents.join(', ')}`);
          console.log(`Total collaborations: ${status.totalCollaborations}`);
        } catch (statusError) {
          console.log('Status check error:', statusError);
        }
      }, 2000);
      
    } catch (error) {
      console.error(`Error processing task: ${error}`);
    }
    
    // Wait for task completion
    await new Promise(resolve => setTimeout(resolve, 3000));
  }
  
  // Test innovation request
  console.log('\n💡 Testing innovation request:');
  try {
    const innovationResponse = await agent.requestInnovation();
    console.log(`Innovation response: ${innovationResponse}`);
  } catch (error) {
    console.error(`Innovation request error: ${error}`);
  }
  
  // Display collaboration summary
  console.log('\n📊 Collaboration Summary:');
  
  try {
    const finalStatus = await agent.getCollaborationStatus();
    console.log(`Total tasks processed: ${finalStatus.activeTasks.length + finalStatus.completedOutputs.length}`);
    console.log(`Completed outputs: ${finalStatus.completedOutputs.length}`);
    console.log(`Available agents: ${finalStatus.availableAgents.length}`);
    
    if (finalStatus.completedOutputs.length > 0) {
      console.log('\n🎯 Recent outputs:');
      finalStatus.completedOutputs.slice(0, 3).forEach((output, index) => {
        console.log(`${index + 1}. Task ${output.taskId} - Quality: ${output.qualityScore.toFixed(2)}, Contributors: ${output.contributors.length}`);
      });
    }
  } catch (error) {
    console.error('Error getting collaboration status:', error);
  }
  
  await agent.stop();
  console.log('\n✅ Collaborative Creation Agent demonstration completed');
}

// Run the demonstration
if (require.main === module) {
  demonstrateCollaborativeAgent().catch(console.error);
}

export { demonstrateCollaborativeAgent };