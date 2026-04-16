#!/usr/bin/env node

const { analyzeRepo } = require('./lib/analyzer');
const { generateContext } = require('./lib/generator');
const { writeOutput } = require('./lib/writer');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);

if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
  console.log(`
ctxgen - Auto-generate AI context files for your codebase

Usage:
  ctxgen <path>           Generate all context files
  ctxgen <path> --dry-run Preview without writing
  ctxgen <path> --target <name>  Generate specific target(s)
  ctxgen --help           Show this help

Targets: agents.md, cursorrules, claude.md, context.md
`);
  process.exit(0);
}

const repoPath = path.resolve(args[0] || '.');
const dryRun = args.includes('--dry-run');
const targets = [];
args.forEach((a, i) => {
  if (a === '--target' && args[i + 1]) targets.push(args[i + 1]);
});

const outputIdx = args.indexOf('--output');
const customOutput = outputIdx !== -1 ? args[outputIdx + 1] : null;

if (!fs.existsSync(repoPath)) {
  console.error(`Error: path not found: ${repoPath}`);
  process.exit(1);
}

(async () => {
  console.log(`🔍 Analyzing ${repoPath}...`);
  const analysis = await analyzeRepo(repoPath);

  console.log(`\n📊 Detected:`);
  console.log(`   Languages: ${analysis.languages.join(', ') || 'none'}`);
  console.log(`   Frameworks: ${analysis.frameworks.join(', ') || 'none'}`);
  console.log(`   Tools: ${analysis.tools.join(', ') || 'none'}`);
  console.log(`   Files analyzed: ${analysis.fileCount}`);
  console.log(`   Key dirs: ${analysis.keyDirs.join(', ')}`);

  const defaultTargets = ['agents.md', 'cursorrules', 'claude.md', 'context.md'];
  const genTargets = targets.length > 0 ? targets : defaultTargets;

  console.log(`\n✏️  Generating: ${genTargets.join(', ')}...`);
  const results = {};

  for (const t of genTargets) {
    results[t] = generateContext(t, analysis);
    if (dryRun) {
      console.log(`\n--- [${t}] (dry run) ---`);
      console.log(results[t].slice(0, 500));
      if (results[t].length > 500) console.log(`... (${results[t].length} chars total)`);
    }
  }

  if (!dryRun) {
    for (const t of genTargets) {
      const outPath = customOutput && genTargets.length === 1
        ? path.resolve(customOutput)
        : path.join(repoPath, t === 'agents.md' ? 'AGENTS.md' : t === 'cursorrules' ? '.cursorrules' : t === 'claude.md' ? 'CLAUDE.md' : 'context.md');
      await writeOutput(outPath, results[t], t);
      console.log(`   ✅ Written: ${outPath}`);
    }
  }

  console.log('\n✨ Done!');
})();
