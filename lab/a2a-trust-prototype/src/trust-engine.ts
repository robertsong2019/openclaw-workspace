// src/trust-engine.ts — Per-agent and per-skill trust scoring
export type TrustLevel = 'unknown' | 'untrusted' | 'neutral' | 'trusted';

interface AgentRecord {
  score: number;
  interactions: number;
  lastUpdated: number;
}

interface SkillRecord {
  score: number;
  interactions: number;
}

function scoreToLevel(score: number): TrustLevel {
  if (score < 50) return 'untrusted';
  if (score < 80) return 'neutral';
  return 'trusted';
}

export class TrustEngine {
  private agents = new Map<string, AgentRecord>();
  private skillRecords = new Map<string, Map<string, SkillRecord>>(); // agentId → skillId → record

  private getOrCreate(agentId: string): AgentRecord {
    let rec = this.agents.get(agentId);
    if (!rec) {
      rec = { score: 50, interactions: 0, lastUpdated: Date.now() };
      this.agents.set(agentId, rec);
    }
    return rec;
  }

  private getOrCreateSkill(agentId: string, skillId: string): SkillRecord {
    let skillMap = this.skillRecords.get(agentId);
    if (!skillMap) {
      skillMap = new Map();
      this.skillRecords.set(agentId, skillMap);
    }
    let rec = skillMap.get(skillId);
    if (!rec) {
      rec = { score: 50, interactions: 0 };
      skillMap.set(skillId, rec);
    }
    return rec;
  }

  /** Record a general interaction with an agent */
  recordInteraction(agentId: string, success: boolean): void {
    const rec = this.getOrCreate(agentId);
    rec.interactions++;
    rec.lastUpdated = Date.now();
    if (success) {
      const gain = 5 * Math.max(0.1, 1 - (rec.interactions - 1) * 0.01);
      rec.score = Math.min(100, rec.score + gain);
    } else {
      rec.score = Math.max(0, rec.score - 15);
    }
  }

  /** Record a skill-specific interaction */
  recordSkillInteraction(agentId: string, skillId: string, success: boolean): void {
    const rec = this.getOrCreateSkill(agentId, skillId);
    rec.interactions++;
    if (success) {
      const gain = 5 * Math.max(0.1, 1 - (rec.interactions - 1) * 0.01);
      rec.score = Math.min(100, rec.score + gain);
    } else {
      rec.score = Math.max(0, rec.score - 15);
    }
    // Also update overall
    this.recordInteraction(agentId, success);
  }

  /** Get overall trust level for an agent */
  getTrustLevel(agentId: string): TrustLevel {
    const rec = this.agents.get(agentId);
    if (!rec) return 'unknown';
    return scoreToLevel(rec.score);
  }

  /** Get trust score for an agent */
  getScore(agentId: string): number {
    return this.agents.get(agentId)?.score ?? 50;
  }

  /** Get per-skill trust level */
  getSkillTrustLevel(agentId: string, skillId: string): TrustLevel {
    const skillMap = this.skillRecords.get(agentId);
    if (!skillMap) return 'unknown';
    const rec = skillMap.get(skillId);
    if (!rec) return 'unknown';
    return scoreToLevel(rec.score);
  }

  /** Check if delegation is allowed at a given level */
  canDelegate(agentId: string, requiredLevel: TrustLevel): boolean {
    const levels: TrustLevel[] = ['unknown', 'untrusted', 'neutral', 'trusted'];
    const actual = this.getTrustLevel(agentId);
    return levels.indexOf(actual) >= levels.indexOf(requiredLevel);
  }

  /** Time decay: reduce trust based on hours elapsed */
  scoreDecay(agentId: string, hoursElapsed: number): void {
    const rec = this.agents.get(agentId);
    if (!rec) return;
    const decay = hoursElapsed * 0.1;
    rec.score = Math.max(0, rec.score - decay);
    rec.lastUpdated = Date.now();
  }

  /** Get a full trust report for an agent */
  getTrustReport(agentId: string): {
    overall: { score: number; level: TrustLevel; interactions: number };
    skills: Record<string, { score: number; level: TrustLevel }>;
  } {
    const rec = this.agents.get(agentId);
    const skills: Record<string, { score: number; level: TrustLevel }> = {};
    const skillMap = this.skillRecords.get(agentId);
    if (skillMap) {
      for (const [skillId, sRec] of skillMap) {
        skills[skillId] = { score: sRec.score, level: scoreToLevel(sRec.score) };
      }
    }
    return {
      overall: rec
        ? { score: rec.score, level: scoreToLevel(rec.score), interactions: rec.interactions }
        : { score: 50, level: 'unknown' as TrustLevel, interactions: 0 },
      skills,
    };
  }
}
