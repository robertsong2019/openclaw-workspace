#!/usr/bin/env node

import { program } from 'commander';
import chalk from 'chalk';
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const packageJson = JSON.parse(
  fs.readFileSync(path.join(__dirname, '../package.json'), 'utf-8')
);

program
  .name('aid')
  .description('AI开发效率工具集 - 提升你的 AI 开发工作流')
  .version(packageJson.version);

// Prompt Management Commands
program
  .command('prompt')
  .description('提示词管理工具')
  .argument('[action]', '操作: save, list, search, use, export', 'list')
  .option('-n, --name <name>', '提示词名称')
  .option('-t, --tags <tags>', '标签（逗号分隔）')
  .option('-c, --category <category>', '分类')
  .option('-f, --file <file>', '从文件加载提示词')
  .option('-q, --query <query>', '搜索查询')
  .option('-o, --output <file>', '导出文件路径')
  .action(async (action, options) => {
    const { default: promptCommand } = await import('../commands/prompt.js');
    await promptCommand(action, options);
  });

// Task Generator
program
  .command('task')
  .description('任务生成器')
  .argument('[template]', '任务模板名称')
  .option('-l, --list', '列出所有模板')
  .option('-v, --variables <vars>', '模板变量 (JSON格式)')
  .option('-o, --output <file>', '输出文件')
  .option('-e, --execute', '生成后立即执行')
  .action(async (template, options) => {
    const { default: taskCommand } = await import('../commands/task.js');
    await taskCommand(template, options);
  });

// Code Analyzer
program
  .command('analyze')
  .description('代码质量分析（针对 AI 生成代码）')
  .argument('<file>', '要分析的文件或目录')
  .option('-t, --type <type>', '代码类型: js, ts, py, all', 'all')
  .option('-f, --format <format>', '输出格式: text, json, markdown', 'text')
  .option('-o, --output <file>', '输出报告文件')
  .option('--check-ai', '检测 AI 生成特征')
  .option('--quality', '质量评分')
  .option('--security', '安全检查')
  .action(async (file, options) => {
    const { default: analyzeCommand } = await import('../commands/analyze.js');
    await analyzeCommand(file, options);
  });

// Session Logger
program
  .command('session')
  .description('AI 会话管理')
  .argument('[action]', '操作: start, stop, log, stats, export', 'stats')
  .option('-n, --name <name>', '会话名称')
  .option('-t, --task <task>', '任务描述')
  .option('-m, --model <model>', '使用的模型')
  .option('--tokens <count>', 'token 数量')
  .option('--duration <seconds>', '持续时间（秒）')
  .option('-f, --file <file>', '导入/导出文件')
  .action(async (action, options) => {
    const { default: sessionCommand } = await import('../commands/session.js');
    await sessionCommand(action, options);
  });

// Quick Actions
program
  .command('quick')
  .description('快速操作')
  .argument('<action>', '操作: scaffold, template, snippet, review')
  .option('-n, --name <name>', '名称')
  .option('-t, --type <type>', '类型')
  .option('-d, --description <desc>', '描述')
  .action(async (action, options) => {
    const { default: quickCommand } = await import('../commands/quick.js');
    await quickCommand(action, options);
  });

// Configuration
program
  .command('config')
  .description('配置管理')
  .argument('[key]', '配置键')
  .argument('[value]', '配置值')
  .option('-l, --list', '列出所有配置')
  .option('-r, --reset', '重置配置')
  .option('--set-path <path>', '设置数据存储路径')
  .action(async (key, value, options) => {
    const { default: configCommand } = await import('../commands/config.js');
    await configCommand(key, value, options);
  });

// Info
program
  .command('info')
  .description('显示工具信息')
  .action(() => {
    console.log(chalk.bold('\n🛠️  AI Dev Tools - AI 开发效率工具集\n'));
    console.log('版本:', chalk.cyan(packageJson.version));
    console.log('数据路径:', chalk.gray(getDataPath()));
    console.log('\n可用命令:');
    console.log('  ' + chalk.cyan('aid prompt') + '    - 提示词管理');
    console.log('  ' + chalk.cyan('aid task') + '      - 任务生成');
    console.log('  ' + chalk.cyan('aid analyze') + '   - 代码分析');
    console.log('  ' + chalk.cyan('aid session') + '   - 会话管理');
    console.log('  ' + chalk.cyan('aid quick') + '     - 快速操作');
    console.log('  ' + chalk.cyan('aid config') + '    - 配置管理');
    console.log('\n使用 ' + chalk.cyan('aid [command] --help') + ' 查看详细帮助\n');
  });

function getDataPath() {
  return process.env.AID_DATA_PATH || path.join(process.env.HOME || '~', '.ai-dev-tools');
}

program.parse();
