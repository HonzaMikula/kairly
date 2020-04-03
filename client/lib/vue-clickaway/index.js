// patched lib from https://github.com/joshiste/vue-clickaway
// branch bugfix/context-of-undefined
// existing pull request https://github.com/simplesmiler/vue-clickaway/pull/29
// version from repository can by used after contains this PR merged
import Vue from 'vue'

export const version = '2.2.2'

const compatible = (/^2\./).test(Vue.version)
if (!compatible) {
  Vue.util.warn('VueClickaway ' + version + ' only supports Vue 2.x, and does not support Vue ' + Vue.version)
}

// @SECTION: implementation

const HANDLER = '_vue_clickaway_handler'

function bind (el, binding, vnode) {
  unbind(el)

  const vm = vnode.context

  const callback = binding.value
  if (typeof callback !== 'function') {
    if (process.env.NODE_ENV !== 'production') {
      Vue.util.warn(
        'v-' + binding.name + '="' +
        binding.expression + '" expects a function value, ' +
        'got ' + callback
      )
    }
    return
  }

  // @NOTE: Vue binds directives in microtasks, while UI events are dispatched
  //        in macrotasks. This causes the listener to be set up before
  //        the "origin" click event (the event that lead to the binding of
  //        the directive) arrives at the document root. To work around that,
  //        we ignore events until the end of the "initial" macrotask.
  // @REFERENCE: https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/
  // @REFERENCE: https://github.com/simplesmiler/vue-clickaway/issues/8
  let initialMacrotaskEnded = false
  setTimeout(function () {
    initialMacrotaskEnded = true
  }, 0)

  el[HANDLER] = function (ev) {
    // @NOTE: this test used to be just `el.contains`, but working with path is better,
    //        because it tests whether the element was there at the time of
    //        the click, not whether it is there now, that the event has arrived
    //        to the top.
    // @NOTE: `.path` is non-standard, the standard way is `.composedPath()`
    const path = ev.path || (ev.composedPath ? ev.composedPath() : undefined)
    if (initialMacrotaskEnded && (path ? !path.includes(el) : !el.contains(ev.target))) {
      return callback.call(vm, ev)
    }
  }

  document.documentElement.addEventListener('click', el[HANDLER], false)
}

function unbind (el) {
  document.documentElement.removeEventListener('click', el[HANDLER], false)
  delete el[HANDLER]
}

export const directive = {
  bind,
  update (el, binding, vnode) {
    if (binding.value === binding.oldValue) { return }
    bind(el, binding, vnode)
  },
  unbind,
}

export const mixin = {
  directives: { onClickaway: directive },
}
