var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  BACKEND_BASE: '"http://kairly.com"'
  //BACKEND_BASE: '"http://localhost:8000"'
})
