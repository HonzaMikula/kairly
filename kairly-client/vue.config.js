const fs = require('fs')
const path = require('path')


const vueConfig = {
  css: {
    loaderOptions: {
      sass: {
        includePaths: [
          path.resolve(__dirname, "./src/styles"),
          path.resolve(__dirname, "./node_modules")  // needed for font-awesome
        ],
        data: (
          fs.readFileSync('src/styles/base.sass', 'utf-8')
        )
      }
    }
  }
}

if (process.env.NODE_ENV === 'production') {
  // productio django needs to have static assets served by nginx from /static
  // after build, index.html must be moved from dist/static to dist
  // this is made in package.json by build command
  vueConfig.outputDir = 'dist/static'
  vueConfig.configureWebpack = {
      output: {
        publicPath: "/static/"
      },
      performance: {
        hints: false
      }
  }
}

module.exports = vueConfig
