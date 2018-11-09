import axiosRetry from 'axios-retry';

export default function({ $axios, redirect }) {
  axiosRetry($axios, {
    retryDelay: axiosRetry.exponentialDelay
  })

  $axios.onError(err => {
    const code = parseInt(err.response && err.response.status)
    if (code === 401) {
      redirect('/')
    }
  })
}
