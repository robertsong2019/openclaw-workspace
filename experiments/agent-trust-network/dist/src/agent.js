"use strict";
/**
 * Agent - 网络中的代理节点
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.Agent = void 0;
class Agent {
    constructor(config) {
        this._interactions = 0;
        this._successfulInteractions = 0;
        this.id = config.id;
        this.name = config.name;
        this.behavior = config.behavior;
        this.expertise = config.expertise || [];
        this.reliability = config.reliability ?? 0.8;
        this._trustScore = config.initialTrust ?? 0.5;
        this._lastActiveTime = new Date();
    }
    get trustScore() {
        return this._trustScore;
    }
    set trustScore(value) {
        this._trustScore = Math.max(0, Math.min(1, value));
    }
    get interactions() {
        return this._interactions;
    }
    get successRate() {
        return this._interactions > 0
            ? this._successfulInteractions / this._interactions
            : 0;
    }
    get lastActiveTime() {
        return this._lastActiveTime;
    }
    /**
     * 记录一次交互
     */
    recordInteraction(success) {
        this._interactions++;
        if (success) {
            this._successfulInteractions++;
        }
        this._lastActiveTime = new Date();
    }
    /**
     * 决定是否与另一个 Agent 合作
     */
    shouldCooperate(otherAgent) {
        switch (this.behavior) {
            case 'cooperative':
                return true;
            case 'neutral':
                return otherAgent.trustScore > 0.3;
            case 'malicious':
                return Math.random() > 0.7; // 30% 概率不合作
            case 'adversarial':
                return false;
        }
    }
    /**
     * 执行任务（根据行为类型返回结果）
     */
    performTask(taskComplexity = 0.5) {
        const baseSuccessRate = this.getBaseSuccessRate();
        const adjustedRate = baseSuccessRate * (1 - taskComplexity * 0.3);
        // 可靠性因素
        const finalRate = adjustedRate * this.reliability;
        return Math.random() < finalRate;
    }
    getBaseSuccessRate() {
        switch (this.behavior) {
            case 'cooperative':
                return 0.85;
            case 'neutral':
                return 0.65;
            case 'malicious':
                return 0.4;
            case 'adversarial':
                return 0.1;
        }
    }
    /**
     * 导出状态
     */
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            behavior: this.behavior,
            trustScore: this._trustScore,
            interactions: this._interactions,
            successfulInteractions: this._successfulInteractions,
            successRate: this.successRate,
            expertise: this.expertise,
            reliability: this.reliability,
            lastActiveTime: this._lastActiveTime.toISOString()
        };
    }
}
exports.Agent = Agent;
//# sourceMappingURL=agent.js.map