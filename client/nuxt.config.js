const fs = require('fs')
const path = require('path')

module.exports = {
  /*
  ** Headers of the page
  */
  head: function() {
    const h = {
      title: 'Kairly – Read only what you care about',
      meta: [
        { charset: 'utf-8' },
        { 'http-equiv': 'X-UA-Compatible', content: 'IE=edge' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' },
        { hid: 'description', name: 'description', content: 'Subscribe to a digital newspapers informing you on topics you are interested in.' }
      ],
      link: [
        { rel: 'icon', sizes: '192x192', href: '/favicon.png' },
        { rel: 'apple-touch-icon', sizes: '192x192', href: '/favicon.png' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Merriweather:300,300i,400,400i,700,700i,900,900i|Roboto:400,400i,700,700i&amp;subset=latin-ext' },
      ],
      htmlAttrs: {
        lang: 'en',
      }
    }
    // this.$route is not present in spa mode
    if (this.$route) {
      h.link.push({ rel: 'canonical', href: 'https://kairly.com'+ this.$route.path })
    }
    return h
  },
  /*
  ** Customize the progress bar color
  */
  // loadingIndicator: { name: 'circle', color: '#57ad68', background: 'white'}
  // loading: { color: '#57ad68' },
  /* TODO add https://github.com/nuxt-community/analytics-module */
  plugins: [
    '~/plugins/ignored-elements',
    '~/plugins/portal-vue',
    { src: '~/plugins/vue-infinite-scroll', ssr: false},
    { src: '~/plugins/rich-editor', ssr: false },
    '~/plugins/vue-moment',
    '~/plugins/vue-uid',
    '~/plugins/axios',
    '~/plugins/i18n.js',
  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    ['@nuxtjs/google-analytics', {
      id: 'UA-114180015-2',
      debug: {
        enabled: true,
        sendHitTask: true
      }
    }],
    ['@nuxtjs/style-resources'],
    ['bootstrap-vue/nuxt'],
  //  '@nuxtjs/redirect-module',
  ],

  bootstrapVue: {
    bootstrapCSS: false,
    bootstrapVueCSS: false,
    directivePlugins: ['VBTooltipPlugin'],
    config: {
      'BTooltip': {
        'delay': { 'show': 500, 'hide': 0 }
      }
    }
  },

  styleResources: {
    sass: '@/styles/base.sass'
  },

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
    }
  },

  auth: {
    redirect: {
      login: '/',
      logout: '/',
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

      routes.push({
        name: 'author-newspaper-issue',
        path: '/:author/:newspaper/:issue',
        component: resolve(__dirname, 'pages/_author/_newspaper/index.vue'),
        chunkName: 'pages/_author/_newspaper/index'
      })
    }
  },

  // redirect: [
  //   { from: '^/platform$', to: '/platform/readers', statusCode: 302 },
  //   { from: '^/platform/$', to: '/platform/readers', statusCode: 302 },
  //   { from: '^/readers$', to: '/platform/readers', statusCode: 302 },
  //   { from: '^/journalists$', to: '/platform/journalists', statusCode: 302 },
  //   { from: '^/publishers$', to: '/platform/publishers', statusCode: 302 },
  //   { from: '^/think-tanks$', to: '/platform/think-tanks', statusCode: 302 },
  //   { from: '^/features$', to: '/features/rss-reader', statusCode: 302 },
  //   { from: '^/features/$', to: '/features/rss-reader', statusCode: 302 },
  //   { from: '^/rss-reader$', to: '/features/rss-reader', statusCode: 302 },
  // ]
}
