/**
 * Stats Command - 查看成本统计
 */

import chalk from 'chalk';
import Table from 'cli-table3';
import { getLogs, getStats, getBudget } from '../storage.js';
import { format } from 'date-fns';

export default async function statsCommand(options) {
  try {
    const logs = getLogs({
      period: options.period,
      model: options.model,
      session: options.session
    });

    if (logs.length === 0) {
      console.log(chalk.yellow('⚠️  没有找到符合条件的数据'));
      return;
    }

    const stats = getStats(logs, options.groupBy);
    const budget = getBudget();

    // 显示总体统计
    if (options.groupBy === null || options.groupBy === 'model') {
      console.log(chalk.bold(`\n📊 成本统计 (${options.period})\n`));

      if (options.format === 'json') {
        console.log(JSON.stringify(stats, null, 2));
        return;
      }

      // 表格显示
      const table = new Table({
        head: [
          chalk.cyan('模型'),
          chalk.cyan('请求次数'),
          chalk.cyan('总 Tokens'),
          chalk.cyan('总成本 (USD)')
        ],
        style: {
          head: [],
          border: ['gray']
        }
      });

      if (options.groupBy) {
        // 分组显示
        for (const [key, data] of Object.entries(stats)) {
          table.push([
            key,
            data.requests,
            data.tokens.toLocaleString(),
            chalk.green('$' + data.cost.toFixed(4))
          ]);
        }
      } else {
        // 总计显示
        table.push([
          chalk.bold('总计'),
          stats.totalRequests,
          stats.totalTokens.toLocaleString(),
          chalk.green.bold('$' + stats.totalCost.toFixed(4))
        ]);
      }

      console.log(table.toString());

      // 预算对比
      if (budget.enabled) {
        const budgetStart = getBudgetStart(budget.period);
        const budgetLogs = logs.filter(log => new Date(log.timestamp) >= budgetStart);
        const budgetCost = budgetLogs.reduce((sum, log) => {
          return sum + ((log.promptTokens || 0) / 1000000 * 0.01 + (log.completionTokens || 0) / 1000000 * 0.03);
        }, 0);

        const percentage = (budgetCost / budget.amount) * 100;

        console.log('\n' + chalk.bold('💰 预算状态:'));
        console.log(`  周期: ${chalk.cyan(budget.period)}`);
        console.log(`  预算: ${chalk.yellow('$' + budget.amount.toFixed(2))}`);
        console.log(`  已用: ${chalk.cyan('$' + budgetCost.toFixed(2))} (${percentage.toFixed(1)}%)`);

        if (percentage >= 100) {
          console.log(`  ${chalk.red.bold('⚠️  已超出预算！')}`);
        } else if (percentage >= budget.warningThreshold) {
          console.log(`  ${chalk.yellow('⚠️  接近预算警告阈值')}`);
        } else {
          console.log(`  ${chalk.green('✅ 预算正常')}`);
        }
      }

      // 时间范围
      const oldest = new Date(logs[logs.length - 1].timestamp);
      const newest = new Date(logs[0].timestamp);
      console.log(`\n${chalk.gray('时间范围:')} ${format(oldest, 'yyyy-MM-dd HH:mm')} - ${format(newest, 'yyyy-MM-dd HH:mm')}`);

    } else {
      // 其他分组方式
      console.log(chalk.bold(`\n📊 按 ${options.groupBy} 分组统计 (${options.period})\n`));

      const table = new Table({
        head: [
          chalk.cyan(options.groupBy),
          chalk.cyan('请求次数'),
          chalk.cyan('总 Tokens'),
          chalk.cyan('总成本')
        ],
        style: {
          head: [],
          border: ['gray']
        }
      });

      for (const [key, data] of Object.entries(stats)) {
        table.push([
          key,
          data.requests,
          data.tokens.toLocaleString(),
          chalk.green('$' + data.cost.toFixed(4))
        ]);
      }

      console.log(table.toString());
    }

  } catch (error) {
    console.error(chalk.red('❌ 统计失败:'), error.message);
    process.exit(1);
  }
}

function getBudgetStart(period) {
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
