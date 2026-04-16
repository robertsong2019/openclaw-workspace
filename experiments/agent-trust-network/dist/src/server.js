"use strict";
/**
 * Express HTTP Server for Agent Trust Network Web UI
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const path_1 = __importDefault(require("path"));
const trust_network_1 = require("./trust-network");
const agent_1 = require("./agent");
const advanced_agent_1 = require("./advanced-agent");
const trust_metrics_1 = require("./trust-metrics");
const app = (0, express_1.default)();
const PORT = process.env.PORT || 3000;
app.use(express_1.default.json());
app.use(express_1.default.static(path_1.default.join(__dirname, '..', 'web')));
// Global network + metrics state
let network = createDefaultNetwork();
let metrics = new trust_metrics_1.TrustMetrics();
let stepCount = 0;
function createDefaultNetwork() {
    const net = new trust_network_1.TrustNetwork({ dampingFactor: 0.85, trustDecayRate: 0.001 });
    const behaviors = ['cooperative', 'neutral', 'malicious', 'adversarial'];
    const names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu'];
    // Create 10 diverse agents
    for (let i = 0; i < 10; i++) {
        const behavior = behaviors[i % behaviors.length];
        const agent = new agent_1.Agent({
            id: `agent-${i}`,
            name: names[i] || `Agent-${i}`,
            behavior,
            initialTrust: 0.3 + Math.random() * 0.4,
            reliability: 0.5 + Math.random() * 0.5,
        });
        net.addAgent(agent);
    }
    // Create random trust relations
    const agentIds = Array.from({ length: 10 }, (_, i) => `agent-${i}`);
    for (let i = 0; i < agentIds.length; i++) {
        const numRelations = 2 + Math.floor(Math.random() * 3);
        for (let j = 0; j < numRelations; j++) {
            const targetIdx = Math.floor(Math.random() * agentIds.length);
            if (targetIdx !== i) {
                net.setTrustRelation(agentIds[i], agentIds[targetIdx], 0.1 + Math.random() * 0.8);
            }
        }
    }
    net.calculateTrustScores();
    return net;
}
// ─── API Routes ──────────────────────────────────────────
// GET /api/network - full network state
app.get('/api/network', (_req, res) => {
    const state = network.export();
    const stats = network.getStats();
    const malicious = network.identifyMaliciousAgents(0.3);
    const trusted = network.getTrustedAgents(0.7);
    // Add computed trust scores to agents
    state.agents = state.agents.map((a) => {
        const agent = network.agents.get(a.id);
        if (agent)
            return { ...a, trustScore: agent.trustScore, interactions: agent.interactions, successRate: agent.successRate };
        return a;
    });
    res.json({
        ...state,
        stats,
        malicious,
        trustedCount: trusted.length,
        stepCount,
    });
});
// POST /api/simulate - run N simulation steps
app.post('/api/simulate', (req, res) => {
    const steps = req.body.steps || 1;
    const agentIds = [];
    network.agents.forEach((_, id) => agentIds.push(id));
    // Record snapshots before
    network.agents.forEach((agent) => metrics.recordSnapshot(agent));
    for (let s = 0; s < steps; s++) {
        // Random pairwise interactions
        for (let i = 0; i < agentIds.length; i++) {
            const j = Math.floor(Math.random() * agentIds.length);
            if (i !== j) {
                try {
                    network.simulateInteraction(agentIds[i], agentIds[j], 0.3 + Math.random() * 0.4);
                }
                catch (_) { }
            }
        }
        // Apply decay
        network.applyTrustDecay(1);
        network.calculateTrustScores();
        stepCount++;
    }
    // Record snapshots after
    network.agents.forEach((agent) => metrics.recordSnapshot(agent));
    res.json({ ok: true, stepsCompleted: steps, stepCount });
});
// POST /api/reset
app.post('/api/reset', (_req, res) => {
    network = createDefaultNetwork();
    metrics = new trust_metrics_1.TrustMetrics();
    stepCount = 0;
    res.json({ ok: true });
});
// POST /api/agent - add a new agent
app.post('/api/agent', (req, res) => {
    const { name, behavior, strategy } = req.body;
    if (!name || !behavior) {
        res.status(400).json({ error: 'name and behavior required' });
        return;
    }
    const id = `agent-${Date.now()}`;
    const validBehaviors = ['cooperative', 'neutral', 'malicious', 'adversarial'];
    if (!validBehaviors.includes(behavior)) {
        res.status(400).json({ error: `behavior must be one of: ${validBehaviors.join(', ')}` });
        return;
    }
    if (strategy) {
        const validStrategies = ['tit-for-tat', 'grim-trigger', 'pavlov', 'random', 'adaptive'];
        if (!validStrategies.includes(strategy)) {
            res.status(400).json({ error: `strategy must be one of: ${validStrategies.join(', ')}` });
            return;
        }
        const agent = new advanced_agent_1.AdvancedAgent({
            id, name, behavior, strategy,
            initialTrust: 0.5,
            reliability: 0.5 + Math.random() * 0.5,
        });
        network.addAgent(agent);
    }
    else {
        const agent = new agent_1.Agent({
            id, name, behavior,
            initialTrust: 0.5,
            reliability: 0.5 + Math.random() * 0.5,
        });
        network.addAgent(agent);
    }
    // Add some random relations to/from new agent
    const agentIds = [];
    network.agents.forEach((_, aid) => { if (aid !== id)
        agentIds.push(aid); });
    const numLinks = Math.min(3, agentIds.length);
    for (let i = 0; i < numLinks; i++) {
        const target = agentIds[Math.floor(Math.random() * agentIds.length)];
        network.setTrustRelation(id, target, 0.2 + Math.random() * 0.6);
        if (Math.random() > 0.5) {
            network.setTrustRelation(target, id, 0.2 + Math.random() * 0.6);
        }
    }
    network.calculateTrustScores();
    res.json({ ok: true, id });
});
// GET /api/metrics
app.get('/api/metrics', (_req, res) => {
    const agents = [];
    network.agents.forEach((a) => agents.push(a));
    const agentMetrics = agents.map(a => metrics.calculateAgentMetrics(a));
    const netMetrics = metrics.calculateNetworkMetrics(agents);
    res.json({ agents: agentMetrics, network: netMetrics });
});
// SPA fallback
app.use((_req, res) => {
    res.sendFile(path_1.default.join(__dirname, '..', 'web', 'index.html'));
});
app.listen(PORT, () => {
    console.log(`🧪 Agent Trust Network UI → http://localhost:${PORT}`);
});
//# sourceMappingURL=server.js.map