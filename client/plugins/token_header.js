import axios from 'axios'

export default function ({ app }) {
  if (app.$auth.loggedIn) {
    // delete plugn when api module converted to actions
    const token = app.$auth.getToken('local')
    axios.defaults.headers.common['Authorization'] = token
  }
}
