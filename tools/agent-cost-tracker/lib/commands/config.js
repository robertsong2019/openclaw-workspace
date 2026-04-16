/**
 * Config Command - 管理模型价格配置
 */

import chalk from 'chalk';
import Table from 'cli-table3';
import { getModels, addModel, updateModel, removeModel } from '../storage.js';

export default async function configCommand(action, options) {
  try {
    switch (action) {
      case 'list':
        await listModels();
        break;

      case 'add':
        await addModelConfig(options);
        break;

      case 'update':
        await updateModelConfig(options);
        break;

      case 'remove':
        await removeModelConfig(options);
        break;

      default:
        console.log(chalk.red(`未知操作: ${action}`));
        console.log(chalk.gray('可用操作: list, add, update, remove'));
        process.exit(1);
    }
  } catch (error) {
    console.error(chalk.red('❌ 配置操作失败:'), error.message);
    process.exit(1);
  }
}

async function listModels() {
  const models = getModels();

  if (Object.keys(models).length === 0) {
    console.log(chalk.yellow('⚠️  没有配置的模型'));
    return;
  }

  console.log(chalk.bold('\n📋 模型价格配置\n'));

  const table = new Table({
    head: [
      chalk.cyan('模型名称'),
      chalk.cyan('输入价格'),
      chalk.cyan('输出价格'),
      chalk.cyan('货币')
    ],
    style: {
      head: [],
      border: ['gray']
    }
  });

  for (const [name, config] of Object.entries(models)) {
    table.push([
      name,
      `$${config.inputPrice}/M`,
      `$${config.outputPrice}/M`,
      config.currency
    ]);
  }

  console.log(table.toString());
  console.log(chalk.gray('\n价格单位: 每 1M tokens\n'));
}

async function addModelConfig(options) {
  if (!options.model || !options.inputPrice || !options.outputPrice) {
    console.log(chalk.red('错误: 添加模型需要 --model, --input-price, --output-price'));
    console.log(chalk.gray('\n示例:'));
    console.log(chalk.gray('  act config add -m my-model -i 5 -o 15 -c USD'));
    process.exit(1);
  }

  const model = addModel(options.model, {
    inputPrice: parseFloat(options.inputPrice),
    outputPrice: parseFloat(options.outputPrice),
    currency: options.currency || 'USD'
  });

  console.log(chalk.green(`✅ 模型 ${options.model} 添加成功`));
  console.log(`  输入价格: $${model.inputPrice}/M`);
  console.log(`  输出价格: $${model.outputPrice}/M`);
  console.log(`  货币: ${model.currency}`);
}

async function updateModelConfig(options) {
  if (!options.model) {
    console.log(chalk.red('错误: 必须指定 --model'));
    process.exit(1);
  }

  const updates = {};
  if (options.inputPrice) updates.inputPrice = parseFloat(options.inputPrice);
  if (options.outputPrice) updates.outputPrice = parseFloat(options.outputPrice);
  if (options.currency) updates.currency = options.currency;

  if (Object.keys(updates).length === 0) {
    console.log(chalk.red('错误: 至少需要更新一个字段'));
    process.exit(1);
  }

  const model = updateModel(options.model, updates);

  console.log(chalk.green(`✅ 模型 ${options.model} 更新成功`));
  console.log(`  输入价格: $${model.inputPrice}/M`);
  console.log(`  输出价格: $${model.outputPrice}/M`);
  console.log(`  货币: ${model.currency}`);
}

async function removeModelConfig(options) {
  if (!options.model) {
    console.log(chalk.red('错误: 必须指定 --model'));
    process.exit(1);
  }

  removeModel(options.model);

  console.log(chalk.green(`✅ 模型 ${options.model} 已删除`));
}
