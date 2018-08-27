
export default function ({ app }) {
  if (process.client) {
    app.$axios.defaults.headers.common['X-Timezone'] = Intl.DateTimeFormat().resolvedOptions().timeZone
  }
}
