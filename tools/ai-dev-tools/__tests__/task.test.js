import { loadTemplate, generateTaskContent } from '../commands/task.js';
import { spawn } from 'child_process';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Real-module tests (replaced previous suite that tested self-defined fixtures)
describe('task command — real template engine', () => {
  const ALL_TEMPLATES = [
    'code-review', 'refactor', 'test-generation', 'documentation',
    'api-design', 'bug-fix', 'feature-implementation', 'performance-optimization'
  ];

  describe('loadTemplate', () => {
    test('loads every template advertised by --list', async () => {
      for (const name of ALL_TEMPLATES) {
        const t = await loadTemplate(name);
        expect(t).toBeDefined();
        expect(t.name).toBe(name);
        expect(t.template).toBeTruthy();
        expect(Array.isArray(t.variables)).toBe(true);
        expect(t.variables.length).toBeGreaterThan(0);
      }
    });

    test('every {placeholder} in template body is declared in variables', async () => {
      for (const name of ALL_TEMPLATES) {
        const t = await loadTemplate(name);
        const placeholders = [...t.template.matchAll(/\{(\w+)\}/g)].map(m => m[1]);
        const declared = new Set(t.variables);
        placeholders.forEach(p => {
          expect(declared.has(p)).toBe(true);
        });
      }
    });

    test('unknown template returns undefined (not a throw)', async () => {
      expect(await loadTemplate('no-such-template')).toBeUndefined();
    });
  });

  describe('generateTaskContent', () => {
    test('substitutes all declared variables', async () => {
      const t = await loadTemplate('code-review');
      const out = generateTaskContent(t, { file_path: 'src/app.js', review_type: 'security' });
      expect(out).toContain('src/app.js');
      expect(out).toContain('security');
      expect(out).not.toContain('{file_path}');
      expect(out).not.toContain('{review_type}');
    });

    test('replaces every occurrence, not just the first', async () => {
      const t = { name: 'dup', variables: ['x'], template: '{x} and {x} again' };
      expect(generateTaskContent(t, { x: 'A' })).toBe('A and A again');
    });

    test('dollar-sign replacement patterns in values are NOT interpreted ($& bugfix)', () => {
      const t = { name: 'shell', variables: ['cmd'], template: 'run: {cmd}' };
      // Before fix: value '$&' would be replaced by the matched text ('{cmd}')
      expect(generateTaskContent(t, { cmd: '$&' })).toBe('run: $&');
      expect(generateTaskContent(t, { cmd: "$`" })).toBe('run: $`');
      expect(generateTaskContent(t, { cmd: "$'" })).toBe("run: $'");
      expect(generateTaskContent(t, { cmd: 'cost: $5 & $10' })).toBe('cost: $5 & $10' && 'run: cost: $5 & $10');
    });

    test('non-string values are stringified, not corrupted', () => {
      const t = { name: 'num', variables: ['n'], template: 'count: {n}' };
      expect(generateTaskContent(t, { n: 42 })).toBe('count: 42');
    });

    test('undeclared placeholders are left untouched', () => {
      const t = { name: 'partial', variables: ['a'], template: '{a} {b}' };
      expect(generateTaskContent(t, { a: 'X' })).toBe('X {b}');
    });

    // 2026-09-24: regex-metachar keys used to crash with raw SyntaxError from
    // new RegExp('{a(b}') — "Unterminated group". Placeholder lookup is literal.
    describe('metacharacter keys are literal (no RegExp injection)', () => {
      const t = { name: 'inj', variables: ['x'], template: 'run: {x}' };

      test.each([
        ['paren group opener', 'a(b'],
        ['bracket class', 'x[1]'],
        ['quantifier brace', 'a{2}'],
        ['dot-all', 'a.b'],
        ['dollar anchor', 'end$'],
        ['star quantifier', 'a*b'],
      ])('%s key: no-throw, no substitution side-effects', (_label, badKey) => {
        expect(() => generateTaskContent(t, { [badKey]: 'VAL' })).not.toThrow();
        // key is not a declared placeholder → template body unchanged
        expect(generateTaskContent(t, { [badKey]: 'VAL' })).toBe('run: {x}');
      });

      test('mixed: metachar garbage key + real placeholder still substitutes', () => {
        const out = generateTaskContent(t, { 'a(b': 'V', 'x]': 'W', x: 'OK' });
        expect(out).toBe('run: OK');
      });

      test('brace in key does not break literal pattern', () => {
        const t2 = { name: 'brace', variables: ['q'], template: 'Q: {q}' };
        expect(generateTaskContent(t2, { 'q{': 'V', 'q': 'REAL' })).toBe('Q: REAL');
      });
    });

    // 2026-09-24: Object.entries(null) TypeError — null/undefined = no substitution
    describe('null/undefined variables are a no-op, not a TypeError', () => {
      const t = { name: 'nul', variables: ['x'], template: 'run: {x}' };

      test('null', () => {
        expect(generateTaskContent(t, null)).toBe('run: {x}');
      });

      test('undefined', () => {
        expect(generateTaskContent(t, undefined)).toBe('run: {x}');
      });
    });
  });

  describe('CLI gate: --variables non-object JSON exits 1 (spawn e2e)', () => {
    const bin = path.resolve(__dirname, '../bin/aid.js');
    const cliDataDir = path.join(os.tmpdir(), `aidt-cli-e2e-${process.pid}`);

    function runAid(args) {
      return new Promise((resolve) => {
        const child = spawn(process.execPath, [bin, ...args], {
          env: { ...process.env, AID_DATA_PATH: cliDataDir, XDG_CONFIG_HOME: path.join(cliDataDir, 'cfg') },
        });
        let stdout = '';
        child.stdout.on('data', d => { stdout += d; });
        child.on('close', code => resolve({ code, stdout }));
      });
    }

    test('valid object variables → exit 0, placeholders filled, no prompt',
      async () => {
        const { code, stdout } = await runAid([
          'task', 'code-review',
          '-v', JSON.stringify({ file_path: 'src/app.js', review_type: 'security' }),
        ]);
        expect(code).toBe(0);
        expect(stdout).toContain('src/app.js');
        expect(stdout).not.toContain('{file_path}');
      }, 30000);

    test('null JSON → exit 1 with object-required error (was silent raw template)',
      async () => {
        const { code, stdout } = await runAid(['task', 'code-review', '-v', 'null']);
        expect(code).toBe(1);
        expect(stdout).toContain('必须是对象');
      }, 30000);

    test('array JSON → exit 1 (same gate)',
      async () => {
        const { code, stdout } = await runAid(['task', 'code-review', '-v', '[1,2]']);
        expect(code).toBe(1);
        expect(stdout).toContain('必须是对象');
      }, 30000);

    test('unparseable JSON → exit 1 with parse error (exitCode was silently 0)',
      async () => {
        const { code, stdout } = await runAid(['task', 'code-review', '-v', '{bad']);
        expect(code).toBe(1);
        expect(stdout).toContain('格式错误');
      }, 30000);
  });
});
