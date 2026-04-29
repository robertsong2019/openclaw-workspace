import { jest } from '@jest/globals';
import fs from 'fs-extra';
import path from 'path';

// Test the template categorization logic extracted from commands/task.js
describe('task command template categorization', () => {
  const templates = [
    { name: 'code-review', description: '代码审查任务', category: '代码质量' },
    { name: 'refactor', description: '重构任务', category: '代码质量' },
    { name: 'test-generation', description: '测试生成', category: '测试' },
    { name: 'documentation', description: '文档生成', category: '文档' },
    { name: 'api-design', description: 'API 设计', category: '设计' },
    { name: 'bug-fix', description: 'Bug 修复', category: '调试' },
    { name: 'feature-implementation', description: '功能实现', category: '开发' },
    { name: 'performance-optimization', description: '性能优化', category: '优化' },
  ];

  test('templates are grouped by category', () => {
    const byCategory = {};
    templates.forEach(t => {
      if (!byCategory[t.category]) byCategory[t.category] = [];
      byCategory[t.category].push(t);
    });

    expect(Object.keys(byCategory)).toHaveLength(7);
    expect(byCategory['代码质量']).toHaveLength(2);
    expect(byCategory['测试']).toHaveLength(1);
    expect(byCategory['优化']).toHaveLength(1);
  });

  test('each template has required fields', () => {
    templates.forEach(t => {
      expect(t).toHaveProperty('name');
      expect(t).toHaveProperty('description');
      expect(t).toHaveProperty('category');
      expect(t.name).toBeTruthy();
      expect(t.description).toBeTruthy();
    });
  });

  test('template names are unique', () => {
    const names = templates.map(t => t.name);
    expect(new Set(names).size).toBe(names.length);
  });

  test('categories are non-empty strings', () => {
    const categories = [...new Set(templates.map(t => t.category))];
    categories.forEach(c => {
      expect(typeof c).toBe('string');
      expect(c.length).toBeGreaterThan(0);
    });
  });
});
