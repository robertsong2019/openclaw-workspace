/**
 * Multimodal Agent Example
 * 
 * Demonstrates the MultimodalAgent's ability to process and understand 
 * input across different modalities.
 */

import { MultimodalAgent, MultimodalAgentConfig } from '../src/agents/MultimodalAgent';

async function demonstrateMultimodalAgent() {
  console.log('🎭 Multimodal Agent Example');
  console.log('='.repeat(50));
  
  // Create a multimodal agent
  const config: MultimodalAgentConfig = {
    name: 'multimodal-assistant',
    capabilities: ['text_analysis', 'image_recognition', 'audio_processing'],
    enableVision: true,
    enableAudio: true,
    enableText: true,
    confidenceThreshold: 0.7
  };
  
  const agent = new MultimodalAgent(config);
  
  await agent.start();
  
  // Test cases for different modalities
  const testCases = [
    {
      type: 'text',
      input: 'Can you help me analyze this image of a sunset over the mountains?',
      description: 'Text input asking for image analysis'
    },
    {
      type: 'text', 
      input: 'I need to create a presentation about climate change and its effects',
      description: 'Text input requesting creative content'
    },
    {
      type: 'text',
      input: 'What do you think about the new AI technology developments?',
      description: 'Text input requesting opinion/analysis'
    }
  ];
  
  console.log('\n📝 Processing text inputs:');
  
  for (const testCase of testCases) {
    console.log(`\n🔍 ${testCase.description}`);
    console.log(`Input: "${testCase.input}"`);
    
    try {
      const response = await agent.process(testCase.input);
      console.log(`Response: ${response}`);
      
      // Show the intent understanding
      const history = (agent as any).getIntentHistory();
      if (history.length > 0) {
        const lastIntent = history[history.length - 1];
        console.log(`Intent: ${lastIntent.primary} (confidence: ${lastIntent.confidence})`);
        console.log(`Entities: ${Array.from(lastIntent.entities.keys()).join(', ')}`);
      }
    } catch (error) {
      console.error(`Error processing input: ${error}`);
    }
  }
  
  // Test multimodal processing
  console.log('\n🔄 Testing multimodal processing:');
  
  const multimodalInputs = [
    {
      type: 'text' as const,
      content: 'The sunset was beautiful',
      metadata: {
        timestamp: new Date(),
        confidence: 0.9
      }
    }
  ];
  
  try {
    const response = await (agent as any).processMultimodal(multimodalInputs);
    console.log(`Multimodal response: ${response}`);
  } catch (error) {
    console.error(`Multimodal processing error: ${error}`);
  }
  
  await agent.stop();
  console.log('\n✅ Multimodal Agent demonstration completed');
}

// Run the demonstration
if (require.main === module) {
  demonstrateMultimodalAgent().catch(console.error);
}

export { demonstrateMultimodalAgent };