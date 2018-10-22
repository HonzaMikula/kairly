export default function({ $axios, redirect }) {
  $axios.onError(err => {
    const code = parseInt(err.response && err.response.status)
    if (code === 401) {
      redirect('/')
    }
  })
}
