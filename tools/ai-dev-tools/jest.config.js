export default {
  testEnvironment: 'node',
  transform: {},
  moduleFileExtensions: ['js', 'mjs'],
  testMatch: ['<rootDir>/__tests__/**/*.test.js'],
  globals: {
    'jest': {
      'isolatedModules': true
    }
  }
};
