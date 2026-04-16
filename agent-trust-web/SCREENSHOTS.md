# Screenshots - Agent Trust Network Web UI

This document describes the key screenshots that would be included in documentation.

## Screenshot 1: Initial View

**File**: `screenshots/01-initial-view.png`

**Description**: The application immediately after loading, showing the default 5-agent network.

**Visible Elements**:
- Header with title "🧪 Agent Trust Network" and PageRank badge
- Left panel with simulation controls (Step, ×10, ×50, Reset buttons)
- Center canvas showing network graph with 5 colored nodes
- Right panel with agent leaderboard sorted by trust score
- Step counter showing "Step 0"

**Network State**:
- Alice (green) - large node, high trust
- Bob (green) - large node, high trust
- Charlie (yellow) - medium node, medium trust
- David (red) - small node, low trust
- Eve (yellow) - medium node, medium trust

**Stats Displayed**:
- Agents: 5
- Relations: 6
- Avg Trust: 50%
- Health: 45%

---

## Screenshot 2: After Simulation

**File**: `screenshots/02-after-simulation.png`

**Description**: Network state after running 50 simulation steps.

**Visible Changes**:
- Step counter showing "Step 50"
- Node sizes have changed based on new trust scores
- Connection lines have different thicknesses
- Trust distribution chart updated

**Network State**:
- Cooperative agents (Alice, Bob) have grown larger (trust increased)
- Malicious agent (David) has shrunk (trust decreased)
- Neutral agents show mixed results
- Some connections are thicker (stronger trust)
- Some connections are thinner (weaker trust)

**Stats Displayed**:
- Agents: 5
- Relations: 8 (new relationships formed)
- Avg Trust: 58% (increased)
- Health: 52% (improved)

**Trust Distribution**:
- High: 40% (2 agents)
- Medium: 40% (2 agents)
- Low: 20% (1 agent)

---

## Screenshot 3: Hover Tooltip

**File**: `screenshots/03-hover-tooltip.png`

**Description**: Mouse hovering over the "Alice" node showing detailed information.

**Visible Elements**:
- Tooltip box appearing near the node
- Tooltip content:
  - Name: "Alice" (green color)
  - Behavior: Cooperative
  - Trust Score: 87.3%
  - Interactions: 23
  - Success Rate: 91.2%
- Connected links highlighted in green
- Non-connected links dimmed
- Selected node appears slightly larger

---

## Screenshot 4: Selected Agent Details

**File**: `screenshots/04-selected-agent.png`

**Description**: After clicking on "Bob" node, right panel shows detailed metrics.

**Visible Elements**:
- Right panel header: "Selected Agent" with "Close" button
- Agent details card showing:
  - Green dot indicator
  - Name: "Bob"
  - Behavior: Cooperative
  - Trust Score: 82.1%
  - Interactions: 19
  - Success Rate: 89.4%
  - Trend: rising (green text)
  - Reliability: high (green text)
- Red "Delete Agent" button
- Agent leaderboard below (Bob highlighted)

**Metrics Explanation**:
- **Trend**: Rising because trust score has been increasing
- **Reliability**: High because of consistent performance and stability

---

## Screenshot 5: Adding New Agent

**File**: `screenshots/05-adding-agent.png`

**Description**: User about to add a new "Frank" agent with cooperative behavior.

**Visible Elements**:
- Left panel "Add Agent" section highlighted
- Name field: "Frank"
- Behavior dropdown: "🟢 Cooperative" selected
- "Add Agent" button visible (not yet clicked)

**Context**:
- Current network has 5 agents
- User is testing network growth
- New agent will start with 50% trust
- Will form relationships over time

---

## Screenshot 6: Network with Many Agents

**File**: `screenshots/06-many-agents.png`

**Description**: Complex network with 15+ agents after extensive simulation.

**Visible Elements**:
- Dense network graph with many nodes and connections
- Variety of node colors (green, yellow, red, purple)
- Complex web of trust relationships
- Some clusters of highly-connected agents
- Some isolated or poorly-connected agents

**Stats Displayed**:
- Agents: 17
- Relations: 34
- Avg Trust: 62%
- Health: 68%

**Notable Patterns**:
- Cooperative agents (green) tend to cluster together
- Malicious agents (red) often on network periphery
- Trust flows through cooperative hubs
- Some neutral agents successfully integrated

---

## Screenshot 7: Trust Distribution Charts

**File**: `screenshots/07-distribution-charts.png`

**Description**: Close-up of the trust and behavior distribution charts in the left panel.

**Trust Distribution Chart**:
- Bar chart with 3 colored bars
- Red bar (Low trust): 20% height
- Yellow bar (Medium trust): 40% height
- Green bar (High trust): 60% height
- Legend showing color meanings

**Behavior Distribution**:
- Cooperative: 6 agents with green progress bar
- Neutral: 5 agents with yellow progress bar
- Malicious: 3 agents with red progress bar
- Adversarial: 3 agents with purple progress bar
- Each shows count and percentage bar

**Insights**:
- More high-trust agents than low-trust
- Cooperative agents are majority
- Malicious/adversarial agents are minority
- Network is relatively healthy

---

## Screenshot 8: Export Dialog

**File**: `screenshots/08-export-dialog.png`

**Description**: Browser download dialog after clicking "Export" button.

**Visible Elements**:
- Browser's save file dialog
- Filename: "trust-network-1712987456.json"
- File type: JSON Document
- Save button highlighted
- Download destination folder visible

**What's Being Saved**:
- All 17 agents with current states
- All 34 trust relations
- Current step count (247)
- Trust history for metrics calculation
- Network configuration

---

## Screenshot 9: Import Dialog

**File**: `screenshots/09-import-dialog.png`

**Description**: File selection dialog after clicking "Import" button.

**Visible Elements**:
- Browser's file selection dialog
- Filter: "JSON Documents (*.json)"
- List of saved network files:
  - trust-network-1712987456.json
  - trust-network-1712991234.json
  - trust-network-1713005678.json
- "Open" button ready to click
- Cancel button available

**Context**:
- User wants to restore a previous network state
- Multiple saved configurations available
- Will load complete network state including trust history

---

## Screenshot 10: Network Metrics Panel

**File**: `screenshots/10-metrics-panel.png`

**Description**: Detailed network metrics displayed in the left panel.

**Visible Elements**:
- Section header: "Network Metrics"
- Metric 1: "Avg Reputation" - 67.3%
- Metric 2: "Confidence Index" - 72.1%
- Metric 3: "Volatility Index" - 23.4%

**What These Mean**:

**Average Reputation (67.3%)**:
- Weighted score considering trust, success rate, stability, and experience
- Above 50% indicates overall good reputation
- Influenced by behavior distribution and interaction success

**Confidence Index (72.1%)**:
- How reliable the trust scores are
- Based on interaction count and stability
- Higher is better - means scores are trustworthy

**Volatility Index (23.4%)**:
- How much trust scores are changing
- Lower is more stable
- 23% is moderate - some fluctuation but not chaotic

**Overall Assessment**:
- Network is stable and healthy
- Trust scores are reliable
- Not too much volatility

---

## Screenshot 11: Zoomed In View

**File**: `screenshots/11-zoomed-in.png`

**Description**: Network graph zoomed in to show details of a cluster.

**Visible Elements**:
- Close-up view of 4-5 interconnected agents
- Node labels clearly visible
- Connection arrows easy to see
- Individual link weights apparent
- Hover tooltip on one node

**Cluster Details**:
- Central hub agent (Alice) with many connections
- Satellite agents connected to hub
- Trust relationships visible
- Some bidirectional trust visible

---

## Screenshot 12: Malicious Agent Isolation

**File**: `screenshots/12-malicious-isolation.png`

**Description**: Network showing how malicious agents become isolated.

**Visible Elements**:
- Red/purple nodes on periphery
- Few connections to malicious agents
- Thinner lines (weak trust) to malicious agents
- Green nodes clustered together
- Trust flows around malicious agents

**What Happened**:
- Malicious agents failed interactions
- Other agents reduced trust in them
- Network naturally isolates untrustworthy agents
- Trust relationships wither away

**Network Self-Correction**:
- Demonstrates trust network resilience
- Untrustworthy agents don't gain influence
- Cooperative agents maintain strong relationships
- Network health maintained despite bad actors

---

## Capturing Screenshots

To capture these screenshots yourself:

1. **Install a screenshot tool**:
   - macOS: Cmd+Shift+4 (built-in)
   - Windows: Win+Shift+S (Snipping Tool)
   - Linux: gnome-screenshot, shutter, or flameshot

2. **Set up the scenario**:
   - Follow the steps in DEMO.md
   - Use the simulation controls
   - Add/remove agents as needed

3. **Capture the screenshot**:
   - Ensure browser is fullscreen or sized appropriately
   - Hide browser bookmarks/toolbar if needed
   - Capture the entire viewport or relevant section

4. **Save and organize**:
   - Use descriptive filenames
   - Create a `screenshots/` directory
   - Include in documentation with this reference

---

## Video Demo (Optional)

Consider creating a short video demo (1-2 minutes) showing:

1. Initial load and network view
2. Running a batch simulation
3. Adding a new agent
4. Clicking and exploring agent details
5. Hovering over nodes
6. Exporting and importing

**Recording Tools**:
- macOS: Cmd+Shift+5 (screen recording)
- Windows: Xbox Game Bar (Win+G)
- Linux: OBS Studio, SimpleScreenRecorder

**Video Structure**:
- 0:00-0:15: Introduction and initial view
- 0:15-0:30: Running simulations
- 0:30-0:45: Adding agents and exploring
- 0:45-1:00: Import/export demonstration
- 1:00-1:15: Key features summary
