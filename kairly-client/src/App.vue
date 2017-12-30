<template>
  <app-view>
    <AppHeaderComponent />
    
    <app-main>
      <router-view></router-view>
    </app-main> 
  </app-view>
</template>

<script>
import AppHeaderComponent from '@/components/AppHeaderComponent'

export default {
  name: 'app',
  components: {
    AppHeaderComponent
  }
}
</script>

<style lang="sass">
  @import 'styles/style'
</style>
