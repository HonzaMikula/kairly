import jwtDecode from 'jwt-decode'

export default function ({ app, $axios, store, redirect }) {
  $axios.onResponse(({ data }) => {
    if (data.$authors) {
      Object.values(data.$authors).forEach(author => store.commit('entities/author', { author }))
    }
    if (data.$newspapers) {
      Object.values(data.$newspapers).forEach(newspaper => store.commit('entities/newspaper', { newspaper }))
    }
  })

  $axios.onError(async (err) => {
    const code = parseInt(err.response && err.response.status)
    if (code === 401) {
      // delete all local tokens
      await app.$auth.logout()
      redirect('/')
    } else {
      throw err
    }
  })

  if (process.browser) {
    window.onNuxtReady(async (app) => {
      const token = app.$auth.getToken('local')
      if (token) {
        let data = null
        try {
          data = jwtDecode(token.split(' ')[1])
        } catch (e) {
          await app.$auth.logout()
          return
        }

        if (data && data.exp) {
          const now = Date.now() / 1000
          const remaining = data.exp - now

          if (remaining < 0) {
            await app.$auth.logout()
            return
          }

          if (remaining < 7 * 86400) {
            const resp = await $axios.$get('/refresh-token')
            const newToken = 'Bearer ' + resp.token

            await app.$auth.setStrategy('local')
            app.$auth.setToken('local', newToken)
            app.$auth.strategy._setToken(newToken)
          }
        }
      }
    })
  }
}
