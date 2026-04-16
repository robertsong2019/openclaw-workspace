/**
 * Budget Command - 设置和检查预算
 */

import chalk from 'chalk';
import { getLogs, getBudget, setBudget, resetBudget } from '../storage.js';
import { format, subDays, startOfDay } from 'date-fns';

export default async function budgetCommand(action, options) {
  try {
    switch (action) {
      case 'set':
        await setBudgetConfig(options);
        break;

      case 'check':
        await checkBudgetStatus();
        break;

      case 'reset':
        resetBudget();
        console.log(chalk.green('✅ 预算已重置'));
        break;

      default:
        console.log(chalk.red(`未知操作: ${action}`));
        console.log(chalk.gray('可用操作: set, check, reset'));
        process.exit(1);
    }
  } catch (error) {
    console.error(chalk.red('❌ 预算操作失败:'), error.message);
    process.exit(1);
  }
}

async function setBudgetConfig(options) {
  if (!options.amount) {
    console.log(chalk.red('错误: 必须指定 --amount'));
    console.log(chalk.gray('\n示例:'));
    console.log(chalk.gray('  act budget set -a 100 -p month'));
    process.exit(1);
  }

  setBudget(
    options.amount,
    options.period || 'month',
    options.warning || 80
  );

  console.log(chalk.green(`✅ 预算设置成功`));
  console.log(`  金额: ${chalk.yellow('$' + parseFloat(options.amount).toFixed(2))}`);
  console.log(`  周期: ${chalk.cyan(options.period || 'month')}`);
  console.log(`  警告阈值: ${chalk.cyan(options.warning + '%')}`);
}

async function checkBudgetStatus() {
  const budget = getBudget();

  if (!budget.enabled) {
    console.log(chalk.yellow('⚠️  预算功能未启用'));
    console.log(chalk.gray('\n使用以下命令设置预算:'));
    console.log(chalk.gray('  act budget set -a <amount> -p <period>'));
    return;
  }

  console.log(chalk.bold(`\n💰 预算状态 (${budget.period})\n`));

  // 获取当前周期的数据
  const periodStart = getPeriodStart(budget.period);
  const logs = getLogs({ period: 'all' });
  const periodLogs = logs.filter(log => new Date(log.timestamp) >= periodStart);

  // 计算当前成本
  const currentCost = periodLogs.reduce((sum, log) => {
    return sum + ((log.promptTokens || 0) / 1000000 * 0.01 + (log.completionTokens || 0) / 1000000 * 0.03);
  }, 0);

  const percentage = (currentCost / budget.amount) * 100;
  const remaining = budget.amount - currentCost;

  // 显示状态
  console.log(`  预算金额: ${chalk.yellow('$' + budget.amount.toFixed(2))}`);
  console.log(`  已用金额: ${chalk.cyan('$' + currentCost.toFixed(4))}`);
  console.log(`  剩余金额: ${chalk.green('$' + remaining.toFixed(4))}`);
  console.log(`  使用率: ${percentage.toFixed(1)}%`);

  // 警告阈值
  console.log(`\n  警告阈值: ${budget.warningThreshold}%`);

  // 状态判断
  console.log(`\n  状态: `);

  if (percentage >= 100) {
    console.log(chalk.red.bold('⚠️  已超出预算！'));
  } else if (percentage >= budget.warningThreshold) {
    console.log(chalk.yellow('⚠️  接近预算警告阈值'));
  } else {
    console.log(chalk.green('✅ 预算正常'));
  }

  // 按模型细分
  if (periodLogs.length > 0) {
    console.log(`\n${chalk.bold('按模型细分:')}`);

    const modelStats = {};
    periodLogs.forEach(log => {
      if (!modelStats[log.model]) {
        modelStats[log.model] = { cost: 0, requests: 0 };
      }
      modelStats[log.model].cost += ((log.promptTokens || 0) / 1000000 * 0.01 + (log.completionTokens || 0) / 1000000 * 0.03);
      modelStats[log.model].requests++;
    });

    for (const [model, stats] of Object.entries(modelStats)) {
      const modelPercent = (stats.cost / currentCost) * 100;
      console.log(`    ${model}: $${stats.cost.toFixed(4)} (${modelPercent.toFixed(1)}%) - ${stats.requests} 次请求`);
    }
  }

  // 时间信息
  const now = new Date();
  const periodEnd = getPeriodEnd(budget.period);
  const daysLeft = Math.ceil((periodEnd - now) / (1000 * 60 * 60 * 24));

  console.log(`\n${chalk.gray('时间信息:')}`);
  console.log(`  周期开始: ${format(periodStart, 'yyyy-MM-dd')}`);
  console.log(`  周期结束: ${format(periodEnd, 'yyyy-MM-dd')}`);
  console.log(`  剩余天数: ${daysLeft} 天`);

  // 建议
  if (daysLeft > 0) {
    const avgDaily = currentCost / ((now - periodStart) / (1000 * 60 * 60 * 24));
    const projectedTotal = currentCost + (avgDaily * daysLeft);

    console.log(`\n${chalk.bold('预测:')}`);
    console.log(`  平均日支出: $${avgDaily.toFixed(4)}`);
    console.log(`  预计总支出: $${projectedTotal.toFixed(4)}`);

    if (projectedTotal > budget.amount) {
      console.log(`  ${chalk.red('⚠️  按当前速度预计将超出预算 $' + (projectedTotal - budget.amount).toFixed(2))}`);
    }
  }
}

function getPeriodStart(period) {
  const now = new Date();

  switch (period) {
    case 'day':
      now.setHours(0, 0, 0, 0);
      break;
    case 'week':
      const dayOfWeek = now.getDay();
      const diff = now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
      now.setDate(diff);
      now.setHours(0, 0, 0, 0);
      break;
    case 'month':
      now.setDate(1);
      now.setHours(0, 0, 0, 0);
      break;
  }

  return now;
}

function getPeriodEnd(period) {
  const now = new Date();

  switch (period) {
    case 'day':
      now.setHours(23, 59, 59, 999);
      break;
    case 'week':
      const dayOfWeek = now.getDay();
      const diff = now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
      now.setDate(diff + 6);
      now.setHours(23, 59, 59, 999);
      break;
    case 'month':
      now.setMonth(now.getMonth() + 1, 0);
      now.setHours(23, 59, 59, 999);
      break;
  }

  return now;
}
