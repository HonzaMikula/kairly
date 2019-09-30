const fs = require('fs')
const path = require('path')

const CKEditorWebpackPlugin = require('@ckeditor/ckeditor5-dev-webpack-plugin');
const { styles } = require('@ckeditor/ckeditor5-dev-utils');

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

  vue: {
    config: {
      // The source of CKEditor is encapsulated in ES6 modules. By default, the code
      // from the node_modules directory is not transpiled, so you must explicitly tell
      // the CLI tools to transpile JavaScript files in all ckeditor5-* modules.
      transpileDependencies: [
        /ckeditor5-[^/\\]+[/\\]src[/\\].+\.js$/,
      ],

      configureWebpack: {
        plugins: [
          // CKEditor needs its own plugin to be built using webpack.
          new CKEditorWebpackPlugin({
            // See https://ckeditor.com/docs/ckeditor5/latest/features/ui-language.html
            language: 'en'
          })
        ]
      },

      // Vue CLI would normally use its own loader to load .svg and .css files, however:
      //	1. The icons used by CKEditor must be loaded using raw-loader,
      //	2. The CSS used by CKEditor must be transpiled using PostCSS to load properly.
      chainWebpack: config => {
        // (1.) To handle editor icons, get the default rule for *.svg files first:
        const svgRule = config.module.rule( 'svg' )

        // Then you can either:
        //
        // * clear all loaders for existing 'svg' rule:
        //
        //		svgRule.uses.clear();
        //
        // * or exclude ckeditor directory from node_modules:
        svgRule.exclude.add( path.join( __dirname, 'node_modules', '@ckeditor' ) )

        // Add an entry for *.svg files belonging to CKEditor. You can either:
        //
        // * modify the existing 'svg' rule:
        //
        //		svgRule.use( 'raw-loader' ).loader( 'raw-loader' );
        //
        // * or add a new one:
        config.module
          .rule( 'cke-svg' )
          .test( /ckeditor5-[^/\\]+[/\\]theme[/\\]icons[/\\][^/\\]+\.svg$/ )
          .use( 'raw-loader' )
          .loader( 'raw-loader' )

        // (2.) Transpile the .css files imported by the editor using PostCSS.
        // Make sure only the CSS belonging to ckeditor5-* packages is processed this way.
        config.module
          .rule( 'cke-css' )
          .test( /ckeditor5-[^/\\]+[/\\].+\.css$/ )
          .use( 'postcss-loader' )
          .loader( 'postcss-loader' )
          .tap(() => {
            return styles.getPostCssConfig({
              themeImporter: {
                themePath: require.resolve('@ckeditor/ckeditor5-theme-lark'),
              },
              minify: true
            })
          })
      }
    }
  }
}
