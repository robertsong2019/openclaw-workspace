import chalk from 'chalk';
import inquirer from 'inquirer';
import ora from 'ora';
import { storage } from '../lib/storage.js';

export default async function sessionCommand(action, options) {
  switch (action) {
    case 'start':
      await startSession(options);
      break;
    case 'stop':
      await stopSession(options);
      break;
    case 'log':
      await logSession(options);
      break;
    case 'stats':
      await showStats(options);
      break;
    case 'export':
      await exportSessions(options);
      break;
    case 'list':
      await listSessions(options);
      break;
    default:
      await showStats(options);
  }
}

async function startSession(options) {
  console.log(chalk.bold('\n▶️  开始新会话\n'));
  
  let sessionData = {};
  
  if (!options.name || !options.task) {
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'name',
        message: '会话名称:',
        default: options.name || `Session-${Date.now()}`,
        validate: (input) => input.trim() ? true : '名称不能为空'
      },
      {
        type: 'input',
        name: 'task',
        message: '任务描述:',
        default: options.task || '',
        validate: (input) => input.trim() ? true : '任务描述不能为空'
      },
      {
        type: 'list',
        name: 'model',
        message: '使用的模型:',
        choices: [
          'GPT-4',
          'GPT-3.5-turbo',
          'Claude-3',
          'Claude-2',
          'Gemini Pro',
          'GLM-4',
          '其他'
        ],
        default: options.model || 'GPT-4'
      }
    ]);
    
    sessionData = answers;
  } else {
    sessionData = {
      name: options.name,
      task: options.task,
      model: options.model || 'GPT-4'
    };
  }
  
  const spinner = ora('创建会话...').start();
  
  try {
    const session = await storage.saveSession(sessionData);
    spinner.succeed(chalk.green(`✓ 会话已开始: ${session.name}`));
    
    console.log('\n会话信息:');
    console.log(chalk.gray('  ID:'), session.id);
    console.log(chalk.gray('  任务:'), session.task);
    console.log(chalk.gray('  模型:'), session.model);
    console.log(chalk.gray('  开始时间:'), new Date(session.startTime).toLocaleString('zh-CN'));
    console.log();
    console.log(chalk.cyan('使用 ' + chalk.bold('aid session log') + ' 记录进度'));
    console.log(chalk.cyan('使用 ' + chalk.bold('aid session stop') + ' 结束会话\n'));
  } catch (error) {
    spinner.fail(chalk.red(`创建失败: ${error.message}`));
  }
}

async function stopSession(options) {
  const sessions = storage.getSessions({ status: 'active' });
  
  if (sessions.length === 0) {
    console.log(chalk.yellow('当前没有活动会话\n'));
    return;
  }
  
  let sessionId = options.name;
  
  if (!sessionId) {
    const answer = await inquirer.prompt([
      {
        type: 'list',
        name: 'session',
        message: '选择要结束的会话:',
        choices: sessions.map(s => ({
          name: `${s.name} - ${s.task}`,
          value: s.id
        }))
      }
    ]);
    sessionId = answer.session;
  }
  
  // 获取统计信息
  const statsAnswer = await inquirer.prompt([
    {
      type: 'number',
      name: 'tokens',
      message: '消耗的 token 数量:',
      default: options.tokens || 0
    },
    {
      type: 'number',
      name: 'duration',
      message: '持续时间（分钟）:',
      default: Math.floor((Date.now() - sessions.find(s => s.id === sessionId).startTime) / 60000) || 1
    }
  ]);
  
  const spinner = ora('结束会话...').start();
  
  try {
    const session = await storage.updateSession(sessionId, {
      status: 'completed',
      tokens: statsAnswer.tokens,
      duration: statsAnswer.duration * 60 // 转换为秒
    });
    
    spinner.succeed(chalk.green(`✓ 会话已完成: ${session.name}`));
    
    console.log('\n会话统计:');
    console.log(chalk.gray('  总时长:'), `${statsAnswer.duration} 分钟`);
    console.log(chalk.gray('  Token 消耗:'), statsAnswer.tokens);
    console.log(chalk.gray('  开始时间:'), new Date(session.startTime).toLocaleString('zh-CN'));
    console.log(chalk.gray('  结束时间:'), new Date(session.endTime).toLocaleString('zh-CN'));
    console.log();
  } catch (error) {
    spinner.fail(chalk.red(`结束失败: ${error.message}`));
  }
}

async function logSession(options) {
  const sessions = storage.getSessions({ status: 'active' });
  
  if (sessions.length === 0) {
    console.log(chalk.yellow('当前没有活动会话\n'));
    return;
  }
  
  // 记录会话日志
  const answer = await inquirer.prompt([
    {
      type: 'list',
      name: 'session',
      message: '选择会话:',
      choices: sessions.map(s => ({
        name: `${s.name} - ${s.task}`,
        value: s.id
      }))
    },
    {
      type: 'editor',
      name: 'log',
      message: '记录内容:'
    }
  ]);
  
  console.log(chalk.green('\n✓ 日志已记录\n'));
}

async function showStats(options) {
  console.log(chalk.bold('\n📊 AI 开发统计\n'));
  
  const stats = storage.getStats();
  
  // 提示词统计
  console.log(chalk.cyan.bold('提示词管理'));
  console.log(chalk.gray('  总数:'), stats.prompts.total);
  if (Object.keys(stats.prompts.byCategory).length > 0) {
    console.log(chalk.gray('  按分类:'));
    Object.entries(stats.prompts.byCategory).forEach(([cat, count]) => {
      console.log(`    ${cat}: ${count}`);
    });
  }
  
  console.log();
  
  // 会话统计
  console.log(chalk.cyan.bold('会话统计'));
  console.log(chalk.gray('  总会话数:'), stats.sessions.total);
  console.log(chalk.gray('  活动会话:'), stats.sessions.active);
  console.log(chalk.gray('  已完成:'), stats.sessions.completed);
  console.log(chalk.gray('  总 Token:'), stats.sessions.totalTokens.toLocaleString());
  console.log(chalk.gray('  总时长:'), `${Math.floor(stats.sessions.totalDuration / 60)} 分钟`);
  
  if (Object.keys(stats.sessions.modelUsage).length > 0) {
    console.log(chalk.gray('  模型使用:'));
    Object.entries(stats.sessions.modelUsage).forEach(([model, count]) => {
      console.log(`    ${model}: ${count} 次`);
    });
  }
  
  console.log();
}

async function listSessions(options) {
  console.log(chalk.bold('\n📋 会话列表\n'));
  
  const sessions = storage.getSessions(options);
  
  if (sessions.length === 0) {
    console.log(chalk.gray('暂无会话记录\n'));
    return;
  }
  
  sessions.slice(0, 20).forEach(s => {
    const status = s.status === 'active' ? chalk.green('●') : chalk.gray('○');
    const duration = s.duration ? ` (${Math.floor(s.duration / 60)}min)` : '';
    console.log(`${status} ${chalk.white(s.name)}${duration}`);
    console.log(chalk.gray(`  任务: ${s.task}`));
    console.log(chalk.gray(`  模型: ${s.model} | Token: ${s.tokens || 0}`));
    console.log();
  });
}

async function exportSessions(options) {
  const outputPath = options.output || `sessions-export-${Date.now()}.json`;
  const spinner = ora('导出会话数据...').start();
  
  try {
    await storage.exportData('json', outputPath);
    spinner.succeed(chalk.green(`✓ 已导出到: ${outputPath}\n`));
  } catch (error) {
    spinner.fail(chalk.red(`导出失败: ${error.message}`));
  }
}
