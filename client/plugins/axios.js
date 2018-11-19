import axiosRetry from 'axios-retry';

export default function({ app, $axios, redirect }) {
  axiosRetry($axios, {
    retryDelay: axiosRetry.exponentialDelay
  })

  $axios.onError(async (err) => {
    const code = parseInt(err.response && err.response.status)
    if (code === 401) {
      // delete all local tokens
      await app.$auth.logout()
      redirect('/')
    }
  })
}
