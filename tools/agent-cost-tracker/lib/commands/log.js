/**
 * Log Command - 记录 AI 使用
 */

import chalk from 'chalk';
import ora from 'ora';
import { addLog, getModel, calculateCost } from '../storage.js';

export default async function logCommand(options) {
  const spinner = ora('记录成本...').start();

  try {
    // 验证必需参数
    if (!options.model) {
      spinner.fail(chalk.red('错误: 必须指定模型名称'));
      console.log(chalk.gray('\n使用 --help 查看帮助'));
      process.exit(1);
    }

    // 检查模型是否存在
    const model = getModel(options.model);
    if (!model) {
      spinner.warn(chalk.yellow(`警告: 模型 ${options.model} 不在配置中，将尝试直接使用指定成本`));
    }

    // 验证 token 数量
    const promptTokens = parseInt(options.promptTokens) || 0;
    const completionTokens = parseInt(options.completionTokens) || 0;
    const directCost = parseFloat(options.cost) || 0;

    if (promptTokens === 0 && completionTokens === 0 && directCost === 0) {
      spinner.fail(chalk.red('错误: 必须提供 token 数量或直接成本'));
      console.log(chalk.gray('\n示例:'));
      console.log(chalk.gray('  act log -m gpt-4 -p 1000 -c 500'));
      console.log(chalk.gray('  act log -m gpt-4 --cost 0.05'));
      process.exit(1);
    }

    // 构建日志数据
    const logData = {
      model: options.model,
      promptTokens,
      completionTokens,
      cost: directCost,
      session: options.session || 'default',
      note: options.note || ''
    };

    // 添加日志
    const log = addLog(logData);
    const cost = calculateCost(log);

    spinner.succeed(chalk.green('✅ 记录成功'));

    // 显示结果
    console.log('\n' + chalk.bold('📊 本次使用:'));
    console.log(`  模型: ${chalk.cyan(log.model)}`);
    console.log(`  输入 tokens: ${chalk.yellow(log.promptTokens?.toLocaleString() || 'N/A')}`);
    console.log(`  输出 tokens: ${chalk.yellow(log.completionTokens?.toLocaleString() || 'N/A')}`);
    console.log(`  成本: ${chalk.green('$' + cost.toFixed(4))}`);
    if (log.session) {
      console.log(`  会话: ${chalk.gray(log.session)}`);
    }
    if (log.note) {
      console.log(`  备注: ${chalk.gray(log.note)}`);
    }

  } catch (error) {
    spinner.fail(chalk.red('❌ 记录失败'));
    console.error(error.message);
    process.exit(1);
  }
}
