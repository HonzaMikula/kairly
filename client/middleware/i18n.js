
export default function ({ isHMR, app, store, req, route, params, error, redirect }) {
  // If middleware is called from hot module replacement, ignore it
  if (isHMR) {
    return
  }

  if (store.state.locale) {
    // local already set, this is just page transition
    return
  }

  const locales = Object.keys(app.i18n.messages)
  let locale = null

  const queryLang = route.query.lang

  if (!locale && locales.includes(queryLang)) {
    locale = queryLang
    app.$auth.$storage.setUniversal('locale', locale)
  }

  if (!locale) {
    locale = app.$auth.$storage.getUniversal('locale')
  }

  if (!locale && req) {
    try {
      locale = req.headers['accept-language']
        .split(',')
        .map(lang => lang.trim().toLocaleLowerCase().substring(0, 2))
        .find(lang => locales.includes(lang))
    } catch {
      // no header is present or header is invalid
      locale = 'en'
    }
  }

  if (locale && locale !== store.state.locale) {
    app.setLocale(locale)
  }
}
