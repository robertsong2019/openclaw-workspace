/**
 * Adaptive Agent Example
 * 
 * Demonstrates the AdaptiveAgent's ability to learn and improve over time
 * based on experience and feedback.
 */

import { AdaptiveAgent, AdaptiveConfig } from '../src/agents/AdaptiveAgent';

async function demonstrateAdaptiveAgent() {
  console.log('🧠 Adaptive Agent Example');
  console.log('='.repeat(50));
  
  // Create an adaptive agent
  const config: AdaptiveConfig = {
    name: 'adaptive-learner',
    capabilities: ['pattern_learning', 'knowledge_adaptation', 'continuous_improvement'],
    maxMemorySize: 100,
    learningRate: 0.15,
    forgettingRate: 0.03,
    enableTransferLearning: true
  };
  
  const agent = new AdaptiveAgent(config);
  
  await agent.start();
  
  // Test scenarios that demonstrate learning
  const testScenarios = [
    {
      input: 'Hello, how are you today?',
      description: 'Basic greeting interaction'
    },
    {
      input: 'Can you help me write a simple function in Python?',
      description: 'Programming assistance request'
    },
    {
      input: 'What machine learning algorithms do you know?',
      description: 'Technical knowledge inquiry'
    },
    {
      input: 'Explain quantum computing in simple terms',
      description: 'Complex topic explanation request'
    },
    {
      input: 'Help me create a basic web page with HTML',
      description: 'Web development assistance'
    }
  ];
  
  console.log('\n📚 Testing adaptive learning scenarios:');
  
  for (const scenario of testScenarios) {
    console.log(`\n🔍 ${scenario.description}`);
    console.log(`Input: "${scenario.input}"`);
    
    try {
      const startTime = Date.now();
      const response = await agent.process(scenario.input);
      const responseTime = Date.now() - startTime;
      
      console.log(`Response: ${response}`);
      console.log(`Response time: ${responseTime}ms`);
      
      // Simulate feedback based on response quality
      const feedback = Math.random() > 0.3 ? 0.8 + Math.random() * 0.2 : 0.3 + Math.random() * 0.4;
      await agent.provideFeedback(feedback);
      console.log(`Feedback provided: ${feedback.toFixed(2)}`);
      
    } catch (error) {
      console.error(`Error processing scenario: ${error}`);
    }
    
    // Small delay between requests
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  
  // Display performance metrics
  console.log('\n📊 Performance Metrics:');
  const metrics = agent.getPerformanceMetrics();
  console.log(`Total tasks processed: ${metrics.totalTasks}`);
  console.log(`Successful tasks: ${metrics.successfulTasks}`);
  console.log(`Success rate: ${(metrics.learningEfficiency * 100).toFixed(1)}%`);
  console.log(`Average response time: ${metrics.averageResponseTime.toFixed(0)}ms`);
  
  // Display knowledge summary
  console.log('\n🧠 Learned Knowledge Items:');
  const knowledge = agent.getKnowledgeSummary();
  knowledge.slice(0, 5).forEach((item, index) => {
    console.log(`${index + 1}. ${item.type} (confidence: ${item.confidence.toFixed(2)}, used: ${item.usageCount} times)`);
  });
  
  // Test knowledge transfer
  console.log('\n🔄 Testing knowledge transfer:');
  
  const transferTest = 'Now help me with a related task: machine learning for image recognition';
  try {
    const transferResponse = await agent.process(transferTest);
    console.log(`Transfer test response: ${transferResponse}`);
  } catch (error) {
    console.error(`Transfer test error: ${error}`);
  }
  
  await agent.stop();
  console.log('\n✅ Adaptive Agent demonstration completed');
}

// Run the demonstration
if (require.main === module) {
  demonstrateAdaptiveAgent().catch(console.error);
}

export { demonstrateAdaptiveAgent };