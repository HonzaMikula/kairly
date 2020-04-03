module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    '@nuxtjs',
    'plugin:nuxt/recommended'
  ],
  // add your custom rules here
  rules: {
    'comma-dangle': 'off',
    'arrow-parens': 'off',
    'no-console': ['warn', { 'allow': ["warn", "error"] }],
    'standard/no-callback-literal': 'off',
    'nuxt/no-cjs-in-config': 'off',
    'vue/no-v-html': 'off',
    'vue/singleline-html-element-content-newline': 'off',
    'vue/multiline-html-element-content-newline': 'off',
    'vue/no-template-shadow': 'off',
    'vue/require-default-prop': 'off' // TODO enable it
  }
}
