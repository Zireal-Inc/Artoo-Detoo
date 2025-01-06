const baseConfig = require('./base');
const reactConfig = require('./rules/react');
const reactNativeConfig = require('./rules/react-native');
const typescriptConfig = require('./rules/typescript');

module.exports = {
  ...baseConfig,
  overrides: [
    {
      files: ['*.jsx', '*.js'],
      ...reactConfig,
    },
    {
      files: ['*.tsx', '*.ts'],
      ...typescriptConfig,
    },
    {
      files: ['*.js'],
      ...reactNativeConfig,
    },
  ],
};
