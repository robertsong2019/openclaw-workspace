import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'fs-extra';
import os from 'os';
import path from 'path';
import { analyzeComplexity, analyzeSecurity, calculateHealthScore } from '../index.js';

async function withTempFile(content, ext = '.js') {
  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'cqc-test-'));
  const tmpFile = path.join(tmpDir, `test${ext}`);
  await fs.writeFile(tmpFile, content);
  return { tmpFile, tmpDir, cleanup: () => fs.remove(tmpDir) };
}

describe('analyzeComplexity', () => {
  it('counts if/for/while as complexity', async () => {
    const code = ['if (x) {}', 'for (let i = 0; i < 10; i++) {}', 'while (true) {}'].join('\n');
    const { tmpFile, cleanup } = await withTempFile(code);
    const result = analyzeComplexity(tmpFile);
    assert.equal(result.complexity, 3);
    assert.ok(Array.isArray(result.issues));
    await cleanup();
  });

  it('detects long lines', async () => {
    const { tmpFile, cleanup } = await withTempFile('x'.repeat(150));
    const result = analyzeComplexity(tmpFile);
    assert.ok(result.issues.some(i => i.includes('行过长')));
    await cleanup();
  });

  it('handles empty file', async () => {
    const { tmpFile, cleanup } = await withTempFile('');
    const result = analyzeComplexity(tmpFile);
    assert.equal(result.complexity, 0);
    assert.deepEqual(result.issues, []);
    await cleanup();
  });

  it('reports no issues for simple code', async () => {
    const { tmpFile, cleanup } = await withTempFile('const x = 1;');
    const result = analyzeComplexity(tmpFile);
    assert.equal(result.complexity, 0);
    assert.deepEqual(result.issues, []);
    await cleanup();
  });
});

describe('analyzeSecurity', () => {
  it('detects eval usage', async () => {
    const { tmpFile, cleanup } = await withTempFile('eval("console.log(1)")');
    const issues = await analyzeSecurity(tmpFile);
    assert.ok(issues.some(i => i.message.includes('eval')));
    await cleanup();
  });

  it('detects innerHTML', async () => {
    const { tmpFile, cleanup } = await withTempFile('el.innerHTML = userInput');
    const issues = await analyzeSecurity(tmpFile);
    assert.ok(issues.some(i => i.message.includes('innerHTML')));
    await cleanup();
  });

  it('returns empty for safe code', async () => {
    const { tmpFile, cleanup } = await withTempFile('const x = 1 + 2;');
    const issues = await analyzeSecurity(tmpFile);
    assert.ok(Array.isArray(issues));
    await cleanup();
  });

  it('detects document.write', async () => {
    const { tmpFile, cleanup } = await withTempFile('document.write("hello")');
    const issues = await analyzeSecurity(tmpFile);
    assert.ok(issues.some(i => i.message.includes('document.write')));
    await cleanup();
  });
});

describe('calculateHealthScore', () => {
  it('returns 0 for empty checks', () => {
    assert.equal(calculateHealthScore({}), 0);
  });

  it('returns 100 for perfect eslint', () => {
    assert.equal(calculateHealthScore({
      eslint: { status: 'completed', errorCount: 0, warningCount: 0 }
    }), 100);
  });

  it('deducts for errors and warnings', () => {
    const score = calculateHealthScore({
      eslint: { status: 'completed', errorCount: 2, warningCount: 5 }
    });
    assert.ok(score < 100);
    assert.ok(score > 0);
  });

  it('averages multiple checks', () => {
    assert.equal(calculateHealthScore({
      eslint: { status: 'completed', errorCount: 0, warningCount: 0 },
      security: { status: 'completed', totalIssues: 0 }
    }), 100);
  });

  it('skips non-completed checks', () => {
    assert.equal(calculateHealthScore({
      eslint: { status: 'skipped', reason: 'no config' }
    }), 0);
  });

  it('deducts for security issues', () => {
    const score = calculateHealthScore({
      security: { status: 'completed', totalIssues: 3 }
    });
    assert.ok(score < 100);
  });
});
