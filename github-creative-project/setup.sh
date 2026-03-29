#!/bin/bash

# Setup script for 12-Factor Agents Explorer
# This script helps users initialize the development environment

set -e

echo "🚀 Setting up 12-Factor Agents Explorer..."
echo "============================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18.0.0 or higher."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2)
REQUIRED_VERSION="18.0.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$NODE_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Node.js version $NODE_VERSION is not supported. Please install version $REQUIRED_VERSION or higher."
    exit 1
fi

echo "✅ Node.js version $NODE_VERSION detected"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

echo "✅ npm detected"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the project
echo "🔨 Building the project..."
npm run build

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p docs
mkdir -p tests
mkdir -p examples/comprehensive-demo

# Run a basic test to ensure everything works
echo "🧪 Running basic tests..."
npm test || echo "⚠️  Some tests failed, but setup continues..."

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. 📖 Read the README.md for detailed usage instructions"
echo "2. 🎯 Run the comprehensive demo: npm run examples"
echo "3. 🧪 Run individual agent demos:"
echo "   - npm run dev examples/hello-agent/multimodal-demo.ts"
echo "   - npm run dev examples/hello-agent/adaptive-demo.ts"
echo "   - npm run dev examples/hello-agent/collaborative-demo.ts"
echo "4. 📚 Check the docs/ directory for generated documentation"
echo "5. 🔧 Start developing: npm run dev"
echo ""
echo "Happy coding! 🚀"