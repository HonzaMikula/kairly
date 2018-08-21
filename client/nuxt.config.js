const fs = require('fs')
const path = require('path')

module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'Kairly - exceptional journalism & great reading experience',
    meta: [
      { charset: 'utf-8' },
      { 'http-equiv': 'X-UA-Compatible', content: 'IE=edge' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' }
      //{ hid: 'description', name: 'description', content: 'New way how we consume and produce news' }
    ],
    link: [
      //{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css?family=PT+Serif:400,400i,700,700i|Roboto:300,300i,400,400i,500,500i,700,700i,900,900i" }
    ]
  },
  /*
  ** Customize the progress bar color
  */
  loading: { color: '#3B8070' },
  /* TODO add https://github.com/nuxt-community/analytics-module */
  plugins: [
    '~/plugins/ignored-elements',
    '~/plugins/portal-vue',
    {src: '~/plugins/tooltip', ssr: false},
    {src: '~/plugins/vue-infinite-scroll', ssr: false},
    //{src: '~/plugins/vue-keep-scroll', ssr: false},
    '~/plugins/vue-moment',
  ],
  modules: [
    '@nuxtjs/axios',
    ['@nuxtjs/google-analytics', {
      id: 'UA-114180015-1'
    }]
  ],
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLint on save
    */
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }

      const vueLoader = config.module.rules.find(
        rule => rule.loader === 'vue-loader')
      const { options: {loaders} } = vueLoader || { options: {} }
      if (loaders) {
        for (const loader of Object.values(loaders)) {
          changeLoaderOptions(Array.isArray(loader) ? loader : [loader])
        }
      }
      config.module.rules.forEach(rule => changeLoaderOptions(rule.use))
    }
  }
}


function changeLoaderOptions(loaders) {
  if (loaders) {
    for (const loader of loaders) {
      let options
      switch (loader.loader) {
      case 'sass-loader':
        options = {
          includePaths: [
            path.resolve(__dirname, "./styles"),
            path.resolve(__dirname, "./node_modules")  // needed for font-awesome
          ],
          data: (
            fs.readFileSync('styles/base.sass', 'utf-8')
          )
        }
        break
      // case 'stylus-loader':
      //   options = {
      //     paths: [path.resolve('./styles')],
      //     import: ['_imports']
      //   }
      //   break
      }
      if (options) {
        Object.assign(loader.options, options)
      }
    }
  }
}
