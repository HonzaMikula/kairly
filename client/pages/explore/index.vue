<script>
export default {
  auth: false,

  async fetch({ redirect }) {
    redirect('/explore/news')
  }
}
</script>
