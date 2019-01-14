<script>
export default {
  fetch ({ store, params, redirect }) {
    redirect(301, '/user/transactions/upcoming')
  }
}
</script>
