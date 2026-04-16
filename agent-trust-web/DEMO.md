# Demo Guide - Agent Trust Network Web UI

This guide provides a walkthrough of the Agent Trust Network visualization tool.

## Getting Started

### 1. Launch the Application

```bash
# Development mode
npm run dev

# Production build
npm run build
npm run preview
```

The application will open in your browser at `http://localhost:5173` (dev) or `http://localhost:4173` (preview).

### 2. Initial State

When you first open the application, you'll see:

**Network Graph (Center)**
- 5 default agents displayed as colored nodes
- Alice (green) - Cooperative
- Bob (green) - Cooperative
- Charlie (yellow) - Neutral
- David (red) - Malicious
- Eve (yellow) - Neutral

**Control Panel (Left)**
- Simulation controls (Step, ×10, ×50, Reset)
- Add Agent form
- Network statistics
- Trust distribution chart
- Behavior distribution chart

**Agent Details Panel (Right)**
- Agent leaderboard sorted by trust score
- Selected agent details (when a node is clicked)

## Core Features

### 1. Running Simulations

#### Step-by-Step Simulation

1. Click the **"Step ▶"** button to run one simulation step
2. Watch as agents interact and trust scores update
3. Observe node sizes change based on trust scores
4. Notice connection colors and thicknesses updating

#### Batch Simulation

1. Click **"×10 ⏩"** to run 10 steps at once
2. Click **"×50"** for 50 steps
3. Watch the step counter increment
4. Observe how trust patterns emerge over time

#### Reset Network

1. Click the **"Reset"** button
2. Network returns to initial state
3. All agents restored to default trust levels

### 2. Adding New Agents

#### Add a Cooperative Agent

1. Enter name: "Frank"
2. Select behavior: "🟢 Cooperative"
3. Click **"Add Agent"**
4. Frank appears in the network as a green node
5. Initial trust score starts at 50%

#### Add a Malicious Agent

1. Enter name: "Grace"
2. Select behavior: "🔴 Malicious"
3. Click **"Add Agent"**
4. Grace appears as a red node
5. Will likely lose trust quickly during simulations

#### Add an Adversarial Agent

1. Enter name: "Henry"
2. Select behavior: "⚫ Adversarial"
3. Click **"Add Agent"**
4. Henry appears as a purple node
5. Actively harms network trust

### 3. Exploring the Network

#### Hover for Quick Info

1. Hover your mouse over any node
2. Tooltip appears showing:
   - Agent name
   - Behavior type
   - Current trust score
   - Total interactions
   - Success rate

#### Click for Detailed View

1. Click on any agent node
2. Right panel updates with:
   - Agent details card
   - Trust score and behavior
   - Interaction count and success rate
   - Trend indicator (rising/falling/stable)
   - Reliability rating (high/medium/low)
3. Click "Close" to deselect

#### Navigate the Graph

1. **Scroll** to zoom in/out
2. **Click and drag** background to pan
3. **Click and drag** nodes to reposition
4. Double-click to reset zoom

### 4. Understanding Metrics

#### Network Stats (Left Panel)

- **Agents**: Total number of agents in network
- **Relations**: Number of trust relationships
- **Avg Trust**: Mean trust score across all agents
- **Health**: Overall network quality (0-100%)

#### Trust Distribution Chart

Three bars showing:
- **Red**: Low trust agents (<30%)
- **Yellow**: Medium trust agents (30-70%)
- **Green**: High trust agents (>70%)

#### Behavior Distribution

Shows count of each behavior type:
- 🟢 Cooperative
- 🟡 Neutral
- 🔴 Malicious
- ⚫ Adversarial

#### Network Metrics

- **Avg Reputation**: Weighted reputation score
- **Confidence Index**: How reliable trust scores are
- **Volatility Index**: How much trust is changing

### 5. Import/Export

#### Export Current Network

1. Click **"Export"** button in header
2. JSON file downloads automatically
3. File named `trust-network-[timestamp].json`
4. Contains:
   - All agents and their states
   - All trust relations
   - Current step count

#### Import Saved Network

1. Click **"Import"** button in header
2. Select previously saved JSON file
3. Network loads with saved state
4. All trust scores and relations restored

## Usage Scenarios

### Scenario 1: Building a Trusting Community

**Goal**: Create a network with high trust

**Steps**:
1. Reset the network
2. Add 5-7 cooperative agents
3. Run 50-100 simulation steps
4. Obtrust trust scores rise
5. Network health should reach 80%+

**Expected Outcome**:
- Most agents have >70% trust
- Network health high
- Confidence index stable
- Volatility low

### Scenario 2: Detecting Malicious Agents

**Goal**: Identify untrustworthy agents

**Steps**:
1. Reset the network
2. Add a mix of agent types
3. Run 100+ simulation steps
4. Click on low-trust nodes
5. Check their metrics

**Expected Outcome**:
- Malicious/adversarial agents have low trust (<30%)
- High volatility for malicious agents
- Low reliability ratings
- Falling trust trends

### Scenario 3: Trust Propagation

**Goal**: Observe how trust spreads

**Steps**:
1. Reset the network
2. Add one highly trusted agent (e.g., "Oracle" with cooperative behavior)
3. Add several new neutral agents
4. Run simulations
5. Watch trust flow from Oracle to others

**Expected Outcome**:
- Oracle maintains high trust
- Neutral agents gradually increase trust
- Trust relationships form around Oracle
- Network becomes more cohesive

### Scenario 4: Network Resilience

**Goal**: Test network stability under stress

**Steps**:
1. Build a stable network (Scenario 1)
2. Add 2-3 malicious agents
3. Run 100+ simulations
4. Observe how network adapts

**Expected Outcome**:
- Network health decreases
- Trusted agents isolate malicious ones
- Trust scores redistribute
- Some relationships break (low weight)

## Visual Indicators

### Node Colors

- 🟢 **Green**: Cooperative - Always tries to help
- 🟡 **Yellow**: Neutral - Helps based on trust
- 🔴 **Red**: Malicious - Rarely cooperates
- ⚫ **Purple**: Adversarial - Actively harms

### Node Size

- **Larger nodes**: Higher trust score
- **Smaller nodes**: Lower trust score
- Size updates dynamically during simulation

### Connection Lines

- **Thicker lines**: Stronger trust relationship
- **Thinner lines**: Weaker trust relationship
- **Darker lines**: Higher trust weight
- **Lighter lines**: Lower trust weight

### Arrows

- Point from trustor to trustee
- Show direction of trust flow
- Highlight when node is hovered

## Tips and Tricks

### Performance

- Use batch simulation (×10, ×50) instead of single steps for large networks
- Limit network to <50 agents for smooth performance
- Close browser tabs you don't need

### Analysis

- Compare trust scores before and after adding agents
- Watch for agents with rapidly changing trust (high volatility)
- Look for agents with consistently high trust and low volatility (most reliable)

### Experimentation

1. **Vary behavior ratios**: Try different mixes of cooperative/neutral/malicious agents
2. **Stress test**: Add 10+ malicious agents and see if network survives
3. **Recovery test**: After adding malicious agents, add more cooperative agents
4. **Isolation**: Remove all connections and watch trust decay

## Common Questions

**Q: Why do trust scores change?**
A: Trust scores update after each interaction based on success/failure. Successful interactions increase trust, failures decrease it.

**Q: What affects the speed of trust change?**
A: Behavior type (malicious agents fail more often), task complexity, and random chance in the simulation.

**Q: Can I manually set trust values?**
A: Not directly in this UI, but you can export, edit the JSON, and import to set specific values.

**Q: How is trust calculated?**
A: Using PageRank algorithm that considers:
- Direct trust from other agents
- Trust of those who trust you
- Network topology
- Damping factor to prevent infinite loops

**Q: What's the difference between neutral and malicious?**
A: Neutral agents help based on trust levels (can be won over), while malicious agents rarely cooperate regardless of trust.

## Keyboard Shortcuts

- **Enter**: Submit "Add Agent" form (when name field is focused)
- **Escape**: Deselect selected agent
- **Scroll**: Zoom in/out
- **Drag**: Pan around the graph

## Troubleshooting

**Graph not rendering?**
- Refresh the page
- Check browser console for errors
- Ensure all dependencies are installed

**Agents not appearing?**
- Verify agent name is not empty
- Check if agent ID already exists
- Try a different name

**Simulation stuck?**
- Click Reset to start over
- Refresh the page
- Check browser console for errors

## Next Steps

1. **Explore**: Try different agent combinations
2. **Experiment**: Run long simulations (500+ steps)
3. **Analyze**: Export data and analyze in external tools
4. **Customize**: Modify the source code for your needs
5. **Deploy**: Share with others using deployment options in DEPLOYMENT.md

## Support

For issues or questions:
- Check the main README.md for setup instructions
- Review DEPLOYMENT.md for deployment help
- Examine the code comments for implementation details
- Open an issue on GitHub for bugs or feature requests
