module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/essential',
    '@vue/airbnb',
    '@vue/typescript/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',

    // My own rules
    indent: ['error', 2],
    semi: ['error', 'never'],
    quotes: ['error', 'single', { avoidEscape: true, allowTemplateLiterals: true }],
    'brace-style': ['error', 'stroustrup', { allowSingleLine: true }],
    'class-methods-use-this': ['off'],
    'lines-between-class-members': ['off'],
    'max-len': ['error', 120],
    '@typescript-eslint/no-non-null-assertion': ['off'],
  },
  overrides: [
    {
      files: ['*.vue'],
      rules: {
        'max-len': 'off', // disables line length check
      },
    },
    {
      files: ['store.ts'],
      rules: {
        'no-explicit-any': 'off',
      },
    },
    {
      files: ['**/dataclasses/*.ts', '**/interfaces/*.ts'],
      // Disable some annoying rules that prevent me from running JSON.stringify to send the data
      rules: {
        camelcase: 'off',
      },
    },
    {
      files: ['src/mixins/savage_aim_mixin.ts'],
      rules: {
        '@typescript-eslint/ban-ts-comment': 'off',
      },
    },
  ],
}
