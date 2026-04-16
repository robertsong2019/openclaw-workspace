"""
Test script for OpenClaw Local Embedding Memory Plugin
Tests the plugin integration with OpenClaw
"""

import os
import sys
import json

# Add the plugin directory to path
sys.path.insert(0, '/root/.openclaw/workspace/experiments/local-embedding-memory')

from openclaw_plugin import create_plugin, PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_DESCRIPTION, PLUGIN_CAPABILITIES

def test_plugin_initialization():
    """Test 1: Plugin initialization"""
    print("🧪 Test 1: Plugin Initialization")
    print("=" * 50)
    
    # Create plugin instance
    plugin = create_plugin("/root/.openclaw/workspace")
    
    # Initialize plugin
    result = plugin.initialize()
    
    print(f"✓ Plugin name: {PLUGIN_NAME}")
    print(f"✓ Plugin version: {PLUGIN_VERSION}")
    print(f"✓ Plugin description: {PLUGIN_DESCRIPTION}")
    print(f"✓ Plugin capabilities: {', '.join(PLUGIN_CAPABILITIES)}")
    print(f"✓ Init status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"✓ Total memories: {result['total_memories']}")
        print(f"✓ Last index time: {result['last_index_time']}")
        print("✅ Test 1 PASSED: Plugin initialized successfully")
        return True
    elif result['status'] == 'warning':
        print(f"⚠️ Warning: {result['message']}")
        print("✅ Test 1 PASSED: Plugin initialized with warnings")
        return True
    else:
        print(f"❌ Test 1 FAILED: {result['message']}")
        return False

def test_update_index():
    """Test 2: Update embedding index"""
    print("\n🧪 Test 2: Update Embedding Index")
    print("=" * 50)
    
    plugin = create_plugin("/root/.openclaw/workspace")
    
    # Initialize first
    init_result = plugin.initialize()
    if init_result['status'] == 'error':
        print(f"❌ Test 2 FAILED: Initialization failed")
        return False
    
    # Update index
    result = plugin.update_index()
    
    print(f"✓ Update status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"✓ Total memories indexed: {result['total_memories']}")
        print(f"✓ Index time: {result['index_time']}")
        print("✅ Test 2 PASSED: Index updated successfully")
        return True
    else:
        print(f"❌ Test 2 FAILED: {result['message']}")
        return False

def test_semantic_search():
    """Test 3: Semantic memory search"""
    print("\n🧪 Test 3: Semantic Memory Search")
    print("=" * 50)
    
    plugin = create_plugin("/root/.openclaw/workspace")
    
    # Initialize
    init_result = plugin.initialize()
    if init_result['status'] == 'error':
        print(f"❌ Test 3 FAILED: Initialization failed")
        return False
    
    # Ensure index exists
    if not os.path.exists(plugin.index_path):
        update_result = plugin.update_index()
        if update_result['status'] != 'success':
            print(f"❌ Test 3 FAILED: Index creation failed")
            return False
    
    # Test semantic search
    test_queries = [
        "AI Agent memory systems",
        "Catalyst agent mesh",
        "multi-agent programming",
        "pipeline execution"
    ]
    
    successful_searches = 0
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        result = plugin.search_memory(query, top_k=3, min_score=0.5)
        
        if result['status'] == 'success':
            print(f"✓ Results found: {result['total_results']}")
            for i, mem_result in enumerate(result['results'][:2], 1):
                print(f"  {i}. Score: {mem_result['score']:.3f} | Source: {mem_result['source']}")
            successful_searches += 1
        else:
            print(f"✗ Search failed: {result['message']}")
    
    if successful_searches == len(test_queries):
        print(f"\n✅ Test 3 PASSED: All {len(test_queries)} searches successful")
        return True
    else:
        print(f"\n⚠️ Test 3 PARTIAL: {successful_searches}/{len(test_queries)} searches successful")
        return successful_searches > 0

def test_plugin_stats():
    """Test 4: Plugin statistics"""
    print("\n🧪 Test 4: Plugin Statistics")
    print("=" * 50)
    
    plugin = create_plugin("/root/.openclaw/workspace")
    
    # Get stats
    result = plugin.get_stats()
    
    print(f"✓ Stats status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"✓ Memory files: {result['memory_files']}")
        print(f"✓ Total size: {result['total_size_mb']} MB")
        print(f"✓ Plugin initialized: {result['plugin_initialized']}")
        
        if result.get('index_info'):
            print(f"✓ Index chunks: {result['index_info']['chunks']}")
            print(f"✓ Embedding model: {result['index_info']['embedding_model']}")
        
        print("✅ Test 4 PASSED: Plugin statistics retrieved successfully")
        return True
    else:
        print(f"❌ Test 4 FAILED: {result['message']}")
        return False

def test_plugin_health():
    """Test 5: Plugin health check"""
    print("\n🧪 Test 5: Plugin Health Check")
    print("=" * 50)
    
    plugin = create_plugin("/root/.openclaw/workspace")
    plugin.initialize()  # Must initialize before health check
    
    # Get health
    result = plugin.get_health()
    
    print(f"✓ Health status: {result['status']}")
    print(f"✓ Plugin initialized: {result['plugin_initialized']}")
    print(f"✓ Index exists: {result['index_exists']}")
    print(f"✓ Memory files exist: {result['memory_files_exist']}")
    
    if result['issues']:
        print(f"⚠️ Issues: {', '.join(result['issues'])}")
    if result['warnings']:
        print(f"⚠️ Warnings: {', '.join(result['warnings'])}")
    
    if result['status'] in ['healthy', 'degraded']:
        print("✅ Test 5 PASSED: Plugin health check successful")
        return True
    else:
        print("❌ Test 5 FAILED: Plugin unhealthy")
        return False

def test_context_search():
    """Test 6: Search with context"""
    print("\n🧪 Test 6: Search with Context")
    print("=" * 50)
    
    plugin = create_plugin("/root/.openclaw/workspace")
    
    # Initialize and ensure index exists
    init_result = plugin.initialize()
    if init_result['status'] == 'error':
        print(f"❌ Test 6 FAILED: Initialization failed")
        return False
    
    if not os.path.exists(plugin.index_path):
        update_result = plugin.update_index()
        if update_result['status'] != 'success':
            print(f"❌ Test 6 FAILED: Index creation failed")
            return False
    
    # Test search with context
    result = plugin.search_with_context("Catalyst agent", context_window=2, top_k=2)
    
    print(f"✓ Search status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"✓ Total results: {result['total_results']}")
        print(f"✓ Context enhanced: {result['context_enhanced']}")
        
        if result['results']:
            for i, mem_result in enumerate(result['results'], 1):
                print(f"  {i}. Score: {mem_result['score']:.3f} | Context: {mem_result.get('context_available', False)}")
        
        print("✅ Test 6 PASSED: Context search successful")
        return True
    else:
        print(f"❌ Test 6 FAILED: {result['message']}")
        return False

def test_recent_memories():
    """Test 7: Recent memories retrieval"""
    print("\n🧪 Test 7: Recent Memories Retrieval")
    print("=" * 50)
    
    plugin = create_plugin("/root/.openclaw/workspace")
    
    # Get recent memories
    result = plugin.recent_memories(limit=5)
    
    print(f"✓ Retrieval status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"✓ Total chunks: {result['total_chunks']}")
        print(f"✓ Returned chunks: {result['returned_chunks']}")
        
        if result['recent_memories']:
            print(f"✓ Sample memory source: {result['recent_memories'][0].get('source', 'unknown')}")
        
        print("✅ Test 7 PASSED: Recent memories retrieved successfully")
        return True
    else:
        print(f"❌ Test 7 FAILED: {result['message']}")
        return False

def run_all_tests():
    """Run all plugin tests"""
    print("🚀 Starting OpenClaw Local Embedding Memory Plugin Tests")
    print("=" * 50)
    
    tests = [
        test_plugin_initialization,
        test_update_index,
        test_semantic_search,
        test_plugin_stats,
        test_plugin_health,
        test_context_search,
        test_recent_memories
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append((test_func.__name__, result))
        except Exception as e:
            print(f"❌ Test {test_func.__name__} threw exception: {str(e)}")
            results.append((test_func.__name__, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PLUGIN TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All plugin tests passed! The OpenClaw integration is working correctly.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Review the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)