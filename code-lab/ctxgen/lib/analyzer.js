const fs = require('fs');
const path = require('path');

const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', '.next', '.nuxt', 'target',
  '__pycache__', '.venv', 'venv', '.tox', 'vendor', '.cache', '.turbo',
  'coverage', '.parcel-cache', '.sx', '.openclaw',
]);

const LANG_MAP = {
  '.js': 'JavaScript', '.ts': 'TypeScript', '.tsx': 'TypeScript (React)',
  '.jsx': 'JavaScript (React)', '.py': 'Python', '.go': 'Go', '.rs': 'Rust',
  '.rb': 'Ruby', '.java': 'Java', '.kt': 'Kotlin', '.swift': 'Swift',
  '.c': 'C', '.cpp': 'C++', '.h': 'C/C++ Header', '.cs': 'C#',
  '.php': 'PHP', '.scala': 'Scala', '.lua': 'Lua', '.sh': 'Shell',
  '.bash': 'Shell', '.zsh': 'Shell',
};

const FRAMEWORK_HINTS = {
  'next.config': 'Next.js', 'nuxt.config': 'Nuxt', 'angular.json': 'Angular',
  'vue.config': 'Vue', 'svelte.config': 'Svelte', 'tailwind.config': 'Tailwind CSS',
  'postcss.config': 'PostCSS', 'vite.config': 'Vite', 'webpack.config': 'Webpack',
  'rollup.config': 'Rollup', 'esbuild': 'esbuild', 'Dockerfile': 'Docker',
  'docker-compose': 'Docker Compose', 'Makefile': 'Make', 'Cargo.toml': 'Cargo/Rust',
  'go.mod': 'Go Modules', 'requirements.txt': 'pip', 'Pipfile': 'Pipenv',
  'pyproject.toml': 'Python (pyproject)', 'Gemfile': 'Bundler/Ruby',
  'pom.xml': 'Maven/Java', 'build.gradle': 'Gradle', 'Package.swift': 'Swift PM',
};

function loadGitignore(repoPath) {
  const giPath = path.join(repoPath, '.gitignore');
  if (!fs.existsSync(giPath)) return [];
  return fs.readFileSync(giPath, 'utf8').split('\n')
    .map(l => l.trim())
    .filter(l => l && !l.startsWith('#'));
}

function shouldIgnore(dirName) {
  return IGNORE_DIRS.has(dirName) || dirName.startsWith('.');
}

function walkDir(dir, gitignore, depth = 0) {
  if (depth > 5) return { files: [], dirs: [] };
  const files = [];
  const dirs = [];
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      if (shouldIgnore(e.name)) continue;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        dirs.push(e.name);
        const sub = walkDir(full, gitignore, depth + 1);
        files.push(...sub.files);
        dirs.push(...sub.dirs);
      } else {
        files.push(full);
      }
    }
  } catch {}
  return { files, dirs };
}

function detectFrameworksAndTools(repoPath) {
  const frameworks = [];
  const tools = [];
  const entries = fs.readdirSync(repoPath);

  // Check package.json
  const pkgPath = path.join(repoPath, 'package.json');
  if (fs.existsSync(pkgPath)) {
    tools.push('Node.js');
    try {
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };
      if (deps.react) frameworks.push('React');
      if (deps.vue) frameworks.push('Vue');
      if (deps.next) frameworks.push('Next.js');
      if (deps.nuxt) frameworks.push('Nuxt');
      if (deps.express) frameworks.push('Express');
      if (deps.fastify) frameworks.push('Fastify');
      if (deps.hono) frameworks.push('Hono');
      if (deps.tailwindcss) tools.push('Tailwind CSS');
      if (deps.typescript) tools.push('TypeScript');
      if (deps.jest || deps.vitest) tools.push('Testing');
      if (deps.eslint) tools.push('ESLint');
      if (deps.prettier) tools.push('Prettier');
      if (deps.prisma) tools.push('Prisma');
      if (deps.drizzleOrm || deps['drizzle-orm']) tools.push('Drizzle ORM');
    } catch {}
  }

  // Check config files
  for (const entry of entries) {
    const base = entry.replace(/\.(js|ts|mjs|cjs|json|yaml|yml|toml)$/, '');
    if (FRAMEWORK_HINTS[base] || FRAMEWORK_HINTS[entry]) {
      const hint = FRAMEWORK_HINTS[base] || FRAMEWORK_HINTS[entry];
      if (!frameworks.includes(hint) && !tools.includes(hint)) {
        if (['Docker', 'Docker Compose', 'Make', 'Vite', 'Webpack', 'Rollup', 'esbuild'].includes(hint)) {
          tools.push(hint);
        } else {
          frameworks.push(hint);
        }
      }
    }
  }

  return { frameworks, tools };
}

function detectConventions(files, repoPath) {
  const conventions = [];

  // Check for common patterns
  const hasIndexFiles = files.some(f => path.basename(f).startsWith('index.'));
  const hasBarrelExports = files.some(f => path.basename(f) === 'index.ts' || path.basename(f) === 'index.js');
  const srcDir = files.some(f => f.includes('/src/'));
  const libDir = files.some(f => f.includes('/lib/'));

  if (hasBarrelExports) conventions.push('Barrel exports (index.ts/js files)');
  if (srcDir) conventions.push('Source in src/ directory');

  // Naming conventions
  const tsFiles = files.filter(f => f.endsWith('.ts') || f.endsWith('.tsx'));
  const kebabCase = tsFiles.filter(f => /^[a-z-]+\.(ts|tsx)$/.test(path.basename(f)));
  const camelCase = tsFiles.filter(f => /^[a-z][a-zA-Z]+\.(ts|tsx)$/.test(path.basename(f)));

  if (kebabCase.length > camelCase.length && kebabCase.length > 3) {
    conventions.push('File naming: kebab-case');
  } else if (camelCase.length > 3) {
    conventions.push('File naming: camelCase');
  }

  // Check for test patterns
  const testFiles = files.filter(f =>
    f.includes('.test.') || f.includes('.spec.') || f.includes('__tests__')
  );
  if (testFiles.length > 0) {
    const isCoLocated = testFiles.some(f => !f.includes('__tests__'));
    conventions.push(isCoLocated ? 'Tests co-located with source' : 'Tests in __tests__ directory');
  }

  return conventions;
}

function extractKeyStructures(files, repoPath) {
  // Find important directories
  const dirCounts = {};
  for (const f of files) {
    const rel = path.relative(repoPath, f);
    const parts = rel.split(path.sep);
    if (parts.length > 1) {
      const topDir = parts[0];
      dirCounts[topDir] = (dirCounts[topDir] || 0) + 1;
    }
  }

  const keyDirs = Object.entries(dirCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([d]) => d);

  return keyDirs;
}

async function analyzeRepo(repoPath) {
  const gitignore = loadGitignore(repoPath);
  const { files, dirs } = walkDir(repoPath, gitignore);

  // Detect languages
  const langCounts = {};
  for (const f of files) {
    const ext = path.extname(f);
    if (LANG_MAP[ext]) {
      const lang = LANG_MAP[ext];
      langCounts[lang] = (langCounts[lang] || 0) + 1;
    }
  }
  const languages = Object.entries(langCounts)
    .sort((a, b) => b[1] - a[1])
    .map(([l]) => l);

  const { frameworks, tools } = detectFrameworksAndTools(repoPath);
  const conventions = detectConventions(files, repoPath);
  const keyDirs = extractKeyStructures(files, repoPath);

  // Get repo name
  const repoName = path.basename(repoPath);

  // Read existing context files if any
  const existingContext = {};
  for (const name of ['AGENTS.md', '.cursorrules', 'CLAUDE.md', 'context.md']) {
    const p = path.join(repoPath, name);
    if (fs.existsSync(p)) {
      existingContext[name] = fs.readFileSync(p, 'utf8').slice(0, 2000);
    }
  }

  // Read README if exists
  let readme = '';
  for (const name of ['README.md', 'readme.md']) {
    const p = path.join(repoPath, name);
    if (fs.existsSync(p)) {
      readme = fs.readFileSync(p, 'utf8').slice(0, 3000);
      break;
    }
  }

  return {
    repoName,
    repoPath,
    languages,
    frameworks,
    tools,
    conventions,
    keyDirs,
    fileCount: files.length,
    existingContext,
    readme,
    topFiles: files.slice(0, 100).map(f => path.relative(repoPath, f)),
  };
}

module.exports = { analyzeRepo };
