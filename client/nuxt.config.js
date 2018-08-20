module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'kairly',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'New way how we consume and produce news' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress bar color
  */
  loading: { color: '#3B8070' },
  /* TODO add https://github.com/nuxt-community/analytics-module */
  plugins: [
    '~/plugins/portal-vue',
    '~/plugins/tooltip',
    '~/plugins/vue-infinite-scroll',
    '~/plugins/vue-keep-scroll',
    '~/plugins/vue-moment',
  ],
  modules: [
    '@nuxtjs/axios',
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
    }
  }
}
