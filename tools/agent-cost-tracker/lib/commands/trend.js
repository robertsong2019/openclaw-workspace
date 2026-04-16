/**
 * Trend Command - 查看成本趋势
 */

import chalk from 'chalk';
import { getLogs } from '../storage.js';
import { format, subDays, startOfDay } from 'date-fns';

export default async function trendCommand(options) {
  try {
    const days = parseInt(options.days) || 30;
    const logs = getLogs({ period: 'all' });

    // 按日期分组
    const dailyData = {};
    const startDate = subDays(new Date(), days - 1);

    // 初始化所有日期
    for (let i = days - 1; i >= 0; i--) {
      const date = startOfDay(subDays(new Date(), i));
      const key = format(date, 'yyyy-MM-dd');
      dailyData[key] = {
        date: key,
        cost: 0,
        tokens: 0,
        requests: 0
      };
    }

    // 填充数据
    logs.forEach(log => {
      const date = startOfDay(new Date(log.timestamp));
      const key = format(date, 'yyyy-MM-dd');

      if (dailyData[key]) {
        dailyData[key].cost += (log.promptTokens || 0) / 1000000 * 0.01 + (log.completionTokens || 0) / 1000000 * 0.03;
        dailyData[key].tokens += (log.promptTokens || 0) + (log.completionTokens || 0);
        dailyData[key].requests++;
      }
    });

    // 转换为数组
    const data = Object.values(dailyData);

    console.log(chalk.bold(`\n📈 成本趋势 (${days} 天)\n`));

    if (options.chart) {
      // ASCII 图表
      const maxCost = Math.max(...data.map(d => d.cost), 0.01);
      const barWidth = 40;

      console.log(chalk.gray('日期        成本        趋势'));
      console.log(chalk.gray('─'.repeat(60)));

      data.forEach(d => {
        const barLength = Math.round((d.cost / maxCost) * barWidth);
        const bar = '█'.repeat(barLength) + '·'.repeat(barWidth - barLength);
        const costStr = '$' + d.cost.toFixed(4);

        console.log(
          `${chalk.gray(format(new Date(d.date), 'MM-dd'))}  ` +
          `${chalk.cyan(costStr.padStart(10))}  ` +
          `${chalk.green(bar)}`
        );
      });

    } else {
      // 表格显示
      const Table = (await import('cli-table3')).default;
      const table = new Table({
        head: [
          chalk.cyan('日期'),
          chalk.cyan('请求数'),
          chalk.cyan('Tokens'),
          chalk.cyan('成本')
        ],
        style: {
          head: [],
          border: ['gray']
        }
      });

      data.forEach(d => {
        table.push([
          format(new Date(d.date), 'yyyy-MM-dd'),
          d.requests,
          d.tokens.toLocaleString(),
          chalk.green('$' + d.cost.toFixed(4))
        ]);
      });

      console.log(table.toString());
    }

    // 汇总统计
    const totalCost = data.reduce((sum, d) => sum + d.cost, 0);
    const totalTokens = data.reduce((sum, d) => sum + d.tokens, 0);
    const totalRequests = data.reduce((sum, d) => sum + d.requests, 0);
    const avgCost = totalCost / days;
    const activeDays = data.filter(d => d.requests > 0).length;

    console.log(chalk.bold('\n📊 汇总:'));
    console.log(`  总成本: ${chalk.green('$' + totalCost.toFixed(4))}`);
    console.log(`  平均每天: ${chalk.yellow('$' + avgCost.toFixed(4))}`);
    console.log(`  最高单日: ${chalk.red('$' + Math.max(...data.map(d => d.cost)).toFixed(4))}`);
    console.log(`  最低单日: ${chalk.cyan('$' + Math.min(...data.map(d => d.cost)).toFixed(4))}`);
    console.log(`  总请求: ${chalk.cyan(totalRequests.toLocaleString())}`);
    console.log(`  总 Tokens: ${chalk.cyan(totalTokens.toLocaleString())}`);
    console.log(`  活跃天数: ${chalk.cyan(activeDays + ' / ' + days)}`);

  } catch (error) {
    console.error(chalk.red('❌ 趋势分析失败:'), error.message);
    process.exit(1);
  }
}
