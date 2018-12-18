import Vue from 'vue'
import VueI18n from 'vue-i18n'

import moment from 'moment'

Vue.use(VueI18n)

export default ({ req, app, store }) => {
  // vue-i18n expecting app.i18n instance to be exist
  app.i18n = new VueI18n({
    locale: store.state.locale,
    fallbackLocale: 'en',
    messages: {
      'en': require('~/po/en.json'),
      'cs': require('~/po/cs.json')
    }
  })

  app.setLocale = function(locale) {
    store.commit('setLang', locale)
    app.i18n.locale = locale
    moment.locale(locale)
  }

  Vue.prototype.setLocale = app.setLocale

  // set local according to state current state value
  // this is especially important for client side where store
  // contains actual local
  moment.locale(store.state.locale)

  // const $t = Vue.prototype.$t
  // Vue.prototype.$t = function(key, ...args) {
  //   key = key.replace(/[{}]/g, '/')
  //   console.log(key)
  //   return $t.call(this, key, ...args)
  // }
}
