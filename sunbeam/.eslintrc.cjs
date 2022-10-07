module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended', 'prettier'],
  plugins: ['svelte3', '@typescript-eslint'],
  ignorePatterns: ['*.cjs', 'src/lib/base/Alert.svelte'], // ignore .cjs files and Alert.svelte (as eslint doesn't support class attributes somehow)
  overrides: [{ files: ['*.svelte'], processor: 'svelte3/svelte3' }],
  settings: {
    'svelte3/typescript': () => require('typescript')
  },
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 'latest'
  },
  env: {
    browser: true,
    es2017: true,
    es2022: true,
    node: true
  }
};
