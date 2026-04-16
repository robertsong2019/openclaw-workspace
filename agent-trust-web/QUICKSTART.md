# Quick Start Guide

Get up and running with the Agent Trust Network Web UI in 5 minutes.

## Prerequisites

- Node.js 18+ installed
- npm, yarn, or pnpm

## Installation

```bash
# Clone or navigate to the project directory
cd agent-trust-web

# Install dependencies
npm install

# Start development server
npm run dev
```

Open your browser to `http://localhost:5173`

## First Steps

### 1. Explore the Default Network

You'll see 5 agents already loaded:
- **Alice** 🟢 - Cooperative
- **Bob** 🟢 - Cooperative
- **Charlie** 🟡 - Neutral
- **David** 🔴 - Malicious
- **Eve** 🟡 - Neutral

### 2. Run a Simulation

Click the **"×10"** button to run 10 simulation steps.

Watch as:
- Node sizes change (trust scores update)
- Connection lines thicken/thin (trust relationships change)
- Statistics update in the left panel

### 3. Add a New Agent

1. Enter "Frank" in the name field
2. Select "🟢 Cooperative"
3. Click **"Add Agent"**

Frank appears as a green node in the network.

### 4. Explore Agent Details

Click on any node (e.g., Alice) to see:
- Trust score and behavior
- Interaction count and success rate
- Trend (rising/falling/stable)
- Reliability rating

### 5. Hover for Quick Info

Hover over nodes to see a tooltip with:
- Agent name and behavior
- Current trust score
- Interactions and success rate

## Common Tasks

### Run a Long Simulation

Click **"×50"** multiple times to run hundreds of steps.

### Reset the Network

Click the **"Reset"** button to start fresh.

### Save Your Network

Click **"Export"** to download the current state as JSON.

### Load a Saved Network

Click **"Import"** and select a previously saved JSON file.

### Navigate the Graph

- **Scroll** to zoom in/out
- **Drag** background to pan
- **Drag** nodes to reposition

## Understanding the Display

### Node Colors

- 🟢 **Green** = Cooperative (always helpful)
- 🟡 **Yellow** = Neutral (helps based on trust)
- 🔴 **Red** = Malicious (rarely cooperates)
- ⚫ **Purple** = Adversarial (actively harmful)

### Node Size

- **Larger** = Higher trust score
- **Smaller** = Lower trust score

### Connection Lines

- **Thicker** = Stronger trust relationship
- **Thinner** = Weaker trust relationship

## Next Steps

- Read [DEMO.md](./DEMO.md) for detailed walkthroughs
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment options
- Review [README.md](./README.md) for full documentation

## Troubleshooting

**Build fails?**
```bash
rm -rf node_modules dist
npm install
npm run build
```

**Port already in use?**
```bash
# Use a different port
npm run dev -- --port 3000
```

**Blank page?**
- Open browser console (F12) for errors
- Ensure all dependencies are installed
- Try clearing browser cache

## Key Concepts

### Trust Score

Calculated using PageRank algorithm:
- Considers who trusts you
- Considers how much they trust you
- Updates after each interaction
- Range: 0-100%

### Network Health

Overall network quality:
- Average trust level
- Trust distribution (high vs low)
- Confidence in trust scores
- Range: 0-100%

### Agent Behavior

How an agent interacts:
- **Cooperative**: 90% success rate
- **Neutral**: 70% success rate, varies by trust
- **Malicious**: 40% success rate
- **Adversarial**: 20% success rate

### Simulation Steps

Each step:
1. Random agents interact
2. Success/failure recorded
3. Trust relationships updated
4. Trust scores recalculated
5. Metrics updated

## Tips

1. **Start simple**: Use the default network to learn
2. **Watch patterns**: Cooperative agents cluster together
3. **Experiment**: Try different agent combinations
4. **Save often**: Export interesting network states
5. **Observe trends**: Watch how trust evolves over time

## Keyboard Shortcuts

- **Enter**: Add agent (when name field focused)
- **Escape**: Deselect selected agent
- **Scroll**: Zoom in/out

## Support

- Issues? Check the main [README.md](./README.md)
- Questions? Review [DEMO.md](./DEMO.md)
- Bugs? Open an issue on GitHub

Happy exploring! 🧪
