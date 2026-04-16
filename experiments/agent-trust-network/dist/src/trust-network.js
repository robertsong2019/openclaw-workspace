"use strict";
/**
 * TrustNetwork - 多 Agent 信任网络
 *
 * 使用 PageRank 式算法计算信任分数
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.TrustNetwork = void 0;
const agent_1 = require("./agent");
class TrustNetwork {
    constructor(config) {
        this.agents = new Map();
        this.relations = [];
        this.trustMatrix = new Map();
        this.dampingFactor = 0.85;
        this.convergenceThreshold = 0.0001;
        this.maxIterations = 100;
        this.trustDecayRate = 0.001; // 每小时衰减率
        if (config?.dampingFactor) {
            this.dampingFactor = config.dampingFactor;
        }
        if (config?.trustDecayRate) {
            this.trustDecayRate = config.trustDecayRate;
        }
    }
    /**
     * 添加 Agent 到网络
     */
    addAgent(agent) {
        this.agents.set(agent.id, agent);
        this.trustMatrix.set(agent.id, new Map());
    }
    /**
     * 移除 Agent
     */
    removeAgent(agentId) {
        this.agents.delete(agentId);
        this.trustMatrix.delete(agentId);
        // 移除所有相关的关系
        this.relations = this.relations.filter(r => r.from !== agentId && r.to !== agentId);
        // 清理信任矩阵
        this.trustMatrix.forEach(row => {
            row.delete(agentId);
        });
    }
    /**
     * 建立/更新信任关系
     */
    setTrustRelation(fromId, toId, weight) {
        if (!this.agents.has(fromId) || !this.agents.has(toId)) {
            throw new Error('Agent not found in network');
        }
        weight = Math.max(0, Math.min(1, weight));
        // 更新或创建关系
        const existingIndex = this.relations.findIndex(r => r.from === fromId && r.to === toId);
        if (existingIndex >= 0) {
            this.relations[existingIndex].weight = weight;
            this.relations[existingIndex].timestamp = new Date();
        }
        else {
            this.relations.push({
                from: fromId,
                to: toId,
                weight,
                timestamp: new Date()
            });
        }
        // 更新信任矩阵
        this.trustMatrix.get(fromId).set(toId, weight);
    }
    /**
     * 获取两个 Agent 之间的信任权重
     */
    getTrustWeight(fromId, toId) {
        return this.trustMatrix.get(fromId)?.get(toId) ?? 0;
    }
    /**
     * 计算信任分数（PageRank 算法）
     */
    calculateTrustScores() {
        const n = this.agents.size;
        if (n === 0)
            return new Map();
        // 初始化分数
        const scores = new Map();
        const newScores = new Map();
        this.agents.forEach((_, id) => {
            scores.set(id, 1 / n);
        });
        // 迭代计算
        let iterations = 0;
        let converged = false;
        while (!converged && iterations < this.maxIterations) {
            this.agents.forEach((agent, id) => {
                // 计算入链贡献
                let incomingTrust = 0;
                this.relations
                    .filter(r => r.to === id)
                    .forEach(r => {
                    const sourceScore = scores.get(r.from) || 0;
                    const outgoingWeight = this.getOutgoingWeight(r.from);
                    if (outgoingWeight > 0) {
                        incomingTrust += (sourceScore * r.weight) / outgoingWeight;
                    }
                });
                // PageRank 公式
                const newScore = (1 - this.dampingFactor) / n +
                    this.dampingFactor * incomingTrust;
                newScores.set(id, newScore);
            });
            // 检查收敛
            converged = this.checkConvergence(scores, newScores);
            // 更新分数
            newScores.forEach((value, key) => {
                scores.set(key, value);
            });
            iterations++;
        }
        // 归一化到 0-1 范围
        const maxScore = Math.max(...Array.from(scores.values()));
        const minScore = Math.min(...Array.from(scores.values()));
        const range = maxScore - minScore;
        if (range > 0) {
            scores.forEach((value, key) => {
                scores.set(key, (value - minScore) / range);
            });
        }
        // 更新 Agent 的信任分数
        scores.forEach((score, id) => {
            const agent = this.agents.get(id);
            if (agent) {
                agent.trustScore = score;
            }
        });
        return scores;
    }
    /**
     * 获取节点的出链总权重
     */
    getOutgoingWeight(agentId) {
        let total = 0;
        this.trustMatrix.get(agentId)?.forEach(weight => {
            total += weight;
        });
        return total;
    }
    /**
     * 检查是否收敛
     */
    checkConvergence(oldScores, newScores) {
        for (const [id, oldScore] of oldScores) {
            const newScore = newScores.get(id);
            if (newScore === undefined)
                return false;
            if (Math.abs(oldScore - newScore) > this.convergenceThreshold) {
                return false;
            }
        }
        return true;
    }
    /**
     * 应用信任衰减
     */
    applyTrustDecay(hoursElapsed) {
        const decayFactor = Math.pow(1 - this.trustDecayRate, hoursElapsed);
        this.agents.forEach(agent => {
            agent.trustScore *= decayFactor;
        });
        this.relations.forEach(relation => {
            relation.weight *= decayFactor;
        });
    }
    /**
     * 模拟交互
     */
    simulateInteraction(requesterId, providerId, taskComplexity = 0.5) {
        const requester = this.agents.get(requesterId);
        const provider = this.agents.get(providerId);
        if (!requester || !provider) {
            throw new Error('Agent not found');
        }
        // 决定是否合作
        const willCooperate = provider.shouldCooperate(requester);
        if (!willCooperate) {
            return { success: false, trustChange: -0.1 };
        }
        // 执行任务
        const success = provider.performTask(taskComplexity);
        // 记录交互
        provider.recordInteraction(success);
        requester.recordInteraction(success);
        // 计算信任变化
        const trustChange = success ? 0.05 : -0.1;
        // 更新信任关系
        const currentWeight = this.getTrustWeight(requesterId, providerId);
        const newWeight = Math.max(0, Math.min(1, currentWeight + trustChange));
        this.setTrustRelation(requesterId, providerId, newWeight);
        return { success, trustChange };
    }
    /**
     * 识别恶意 Agent
     */
    identifyMaliciousAgents(threshold = 0.3) {
        const malicious = [];
        this.agents.forEach((agent, id) => {
            if (agent.trustScore < threshold) {
                malicious.push(id);
            }
        });
        return malicious;
    }
    /**
     * 获取可信 Agent
     */
    getTrustedAgents(threshold = 0.7) {
        const trusted = [];
        this.agents.forEach(agent => {
            if (agent.trustScore >= threshold) {
                trusted.push(agent);
            }
        });
        return trusted.sort((a, b) => b.trustScore - a.trustScore);
    }
    /**
     * 获取网络统计
     */
    getStats() {
        const behaviorCounts = {
            cooperative: 0,
            neutral: 0,
            malicious: 0,
            adversarial: 0
        };
        let totalTrust = 0;
        this.agents.forEach(agent => {
            behaviorCounts[agent.behavior]++;
            totalTrust += agent.trustScore;
        });
        return {
            totalAgents: this.agents.size,
            totalRelations: this.relations.length,
            averageTrust: this.agents.size > 0 ? totalTrust / this.agents.size : 0,
            trustDistribution: behaviorCounts,
            clusterCount: this.estimateClusterCount()
        };
    }
    /**
     * 估算网络中的集群数量（简化算法）
     */
    estimateClusterCount() {
        const visited = new Set();
        let clusterCount = 0;
        const dfs = (agentId) => {
            if (visited.has(agentId))
                return;
            visited.add(agentId);
            // 遍历邻居
            this.trustMatrix.get(agentId)?.forEach((_, neighborId) => {
                if (!visited.has(neighborId)) {
                    dfs(neighborId);
                }
            });
            this.trustMatrix.forEach((row, fromId) => {
                if (row.get(agentId) && !visited.has(fromId)) {
                    dfs(fromId);
                }
            });
        };
        this.agents.forEach((_, id) => {
            if (!visited.has(id)) {
                dfs(id);
                clusterCount++;
            }
        });
        return clusterCount;
    }
    /**
     * 导出网络状态
     */
    export() {
        return {
            agents: Array.from(this.agents.values()).map(a => a.toJSON()),
            relations: this.relations.map(r => ({
                ...r,
                timestamp: r.timestamp.toISOString()
            })),
            config: {
                dampingFactor: this.dampingFactor,
                trustDecayRate: this.trustDecayRate
            }
        };
    }
    /**
     * 导入网络状态
     */
    static import(data) {
        const network = new TrustNetwork(data.config);
        // 导入 Agent
        data.agents.forEach((agentData) => {
            const agent = new agent_1.Agent({
                id: agentData.id,
                name: agentData.name,
                behavior: agentData.behavior,
                initialTrust: agentData.trustScore,
                expertise: agentData.expertise,
                reliability: agentData.reliability
            });
            network.addAgent(agent);
        });
        // 导入关系
        data.relations.forEach((r) => {
            network.setTrustRelation(r.from, r.to, r.weight);
        });
        return network;
    }
}
exports.TrustNetwork = TrustNetwork;
//# sourceMappingURL=trust-network.js.map