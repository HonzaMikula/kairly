

export default function ({ isHMR, app, store, req, route, params, error, redirect }) {
  // If middleware is called from hot module replacement, ignore it
  if (isHMR) {
    return
  }

  if (store.state.locale) {
    // store already hydrated on server side
    return
  }

  const locales = Object.keys(app.i18n.messages)
  let locale = null

  const queryLang = route.query.lang

  if (!locale && locales.indexOf(queryLang) !== -1) {
    locale = queryLang
    app.$auth.$storage.setUniversal('locale', locale)
  }

  if (!locale) {
    locale = app.$auth.$storage.getUniversal('locale')
  }

  if (!locale && req) {
    locale = req.headers['accept-language']
      .split(',')
      .map(lang => lang.trim().toLocaleLowerCase().substring(0, 2))
      .find(lang => locales.indexOf(lang) !== -1)
  }

  if (locale && locale !== store.state.locale) {
    app.setLocale(locale)
  }
}
