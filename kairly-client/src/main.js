// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import './polyfills'

import InfiniteScroll from 'vue-infinite-scroll'
import PortalVue from 'portal-vue'
import Vue from 'vue'
import VueAnalytics from 'vue-analytics'
import VueKeepScroll from 'vue-keep-scroll'
import VueMeta from 'vue-meta'
import VueMoment from 'vue-moment-jalaali'
import VueTooltip from 'vue-directive-tooltip'

import App from './App'
import router from './router'


import store from '@/store'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/.*/]

Vue.use(InfiniteScroll)
Vue.use(PortalVue)
Vue.use(VueKeepScroll)
Vue.use(VueMoment)
Vue.use(VueMeta)
Vue.use(VueTooltip)

Vue.use(VueAnalytics, {
  id: 'UA-114180015-1',
  router
})

new Vue({
  render: h => h(App),
  store,
  router,
}).$mount('#app')
