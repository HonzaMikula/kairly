// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Tooltip from 'vue-directive-tooltip'
import VueMce from 'vue-mce'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/.*/]

Vue.use(Tooltip)
Vue.use(VueMce)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
