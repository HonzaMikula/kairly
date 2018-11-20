const fs = require('fs')
const path = require('path')

module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'Kairly – We aim for exceptional journalism',
    meta: [
      { charset: 'utf-8' },
      { 'http-equiv': 'X-UA-Compatible', content: 'IE=edge' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' },
      { hid: 'description', name: 'description', content: 'New way how we consume and produce news' }
    ],
    link: [
      { rel: 'icon', sizes: '192x192', href: '/favicon.png' },
      { rel: 'apple-touch-icon', sizes: '192x192', href: '/favicon.png' },
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css?family=Merriweather:300,300i,400,400i,700,700i,900,900i|Roboto:400,400i,700,700i&amp;subset=latin-ext" }
    ]
  },
  css: [
    'medium-editor/dist/css/medium-editor.min.css',
    'medium-editor/dist/css/themes/default.min.css',
  ],
  /*
  ** Customize the progress bar color
  */
  // loadingIndicator: { name: 'circle', color: '#57ad68', background: 'white'}
  // loading: { color: '#57ad68' },
  /* TODO add https://github.com/nuxt-community/analytics-module */
  plugins: [
    '~/plugins/ignored-elements',
    '~/plugins/portal-vue',
    {src: '~/plugins/tooltip', ssr: false},
    {src: '~/plugins/vue-infinite-scroll', ssr: false},
    {src: '~/plugins/medium-editor', ssr: false },
    //{src: '~/plugins/vue-keep-scroll', ssr: false},
    '~/plugins/vue-moment',
    '~/plugins/axios',
    '~/plugins/i18n.js',
  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    ['@nuxtjs/google-analytics', {
      id: process.env.GA_ID
    }],
    ['nuxt-sass-resources-loader', {
      resources: '@/styles/base.sass'
    }],
  ],
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLint on save
    */
    extend (config, { isDev }) {
      // fix stuck on 91% additional chunk assets processing when buildin again stable Nuxt
      //config.plugins = config.plugins.filter((plugin) => plugin.constructor.name !== 'UglifyJsPlugin')
      if (isDev && process.client) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    },

    extractCSS: {
      allChunks: true
    }
  },

  auth: {
    redirect: {
      login: '/homepage',
      logout: '/homepage',
      home: '/'
    },
    localStorage: false,
    cookie: {
      options: {
        expires: 60
      }
    },
    strategies: {
      local: {
        endpoints: {
          login: { url: '/token', method: 'post', propertyName: 'token' },
          logout: false,
          user: { url: '/profile', method: 'get', propertyName: 'user' }
        }
        // tokenRequired: true,
        // tokenType: 'bearer',
      }
    }
  },

  router: {
    middleware: ['i18n'],
    extendRoutes (routes, resolve) {
      // make sure that author/post is before author/newspaper
      const postRouteIdx = routes.findIndex(r => r.name === 'author-post')
      const postRoute = routes.splice(postRouteIdx, 1)[0]
      postRoute.path = '/:author/:post([-\\w]*\\-\\-[0-9a-f]{9})'
      routes.unshift(postRoute)

      routes.unshift({
        name: 'timeline-date',
        path: '/:date(\\d{4}-\\d{2}-\\d{2})',
        component: resolve(__dirname, 'pages/index.vue'),
        chunkName: 'pages/index'
      })
    }
  }
}
