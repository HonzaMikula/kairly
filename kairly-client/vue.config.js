const fs = require('fs')
const path = require('path')

module.exports = {
  outputDir: 'dist/static',
  configureWebpack: {
    output: {
      publicPath: "/static/"
    }
  },
  css: {
    loaderOptions: {
      sass: {
        includePaths: [
          path.resolve(__dirname, "./src/styles"),
          path.resolve(__dirname, "./node_modules")
        ],
        data: (
          fs.readFileSync('src/styles/base.sass', 'utf-8')
        )
      }
    }
  }
}
