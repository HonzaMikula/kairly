<script>
export default {
  fetch ({ store, params, redirect }) {
    if (!store.state.auth.loggedIn) {
      redirect('/homepage')
      return
    }

    redirect(301, '/subscription/newspapers')
  }
}
</script>
