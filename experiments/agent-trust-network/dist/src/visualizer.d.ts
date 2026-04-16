/**
 * Visualizer - 信任网络可视化工具
 *
 * 生成 ASCII 艺术和简单的可视化输出
 */
import { TrustNetwork } from './trust-network';
export declare class Visualizer {
    /**
     * 生成网络拓扑图（ASCII 艺术）
     */
    static renderNetworkGraph(network: TrustNetwork): string;
    /**
     * 生成交互历史图
     */
    static renderInteractionHistory(history: Array<{
        requester: string;
        provider: string;
        success: boolean;
    }>): string;
    /**
     * 生成信任传播动画（ASCII）
     */
    static renderTrustPropagation(network: TrustNetwork, iterations: number): string;
    /**
     * 辅助方法：获取排序后的 Agent
     */
    private static getSortedAgents;
    /**
     * 辅助方法：获取行为表情
     */
    private static getBehaviorEmoji;
    /**
     * 辅助方法：获取信任度进度条
     */
    private static getTrustBar;
    /**
     * 辅助方法：获取进度条
     */
    private static getProgressBar;
}
//# sourceMappingURL=visualizer.d.ts.map