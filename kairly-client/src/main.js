// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './polyfills'

import Vue from 'vue'
import App from './App'
import router from './router'
import Tooltip from 'vue-directive-tooltip'
import VueMoment from 'vue-moment-jalaali'
import InfiniteScroll from 'vue-infinite-scroll'
import VueAnalytics from 'vue-analytics'
import VueKeepScroll from 'vue-keep-scroll'
import PortalVue from 'portal-vue'


import store from '@/store'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/.*/]

Vue.use(Tooltip)
Vue.use(VueMoment)
Vue.use(InfiniteScroll)
Vue.use(VueKeepScroll)
Vue.use(PortalVue)

Vue.use(VueAnalytics, {
  id: 'UA-114180015-1',
  router
})

new Vue({
  render: h => h(App),
  store,
  router,
}).$mount('#app')
