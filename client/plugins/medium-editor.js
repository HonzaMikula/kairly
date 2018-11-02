import Vue from 'vue'
import MediumEditor from '@/components/editor/MediumEditor'

// register component from plugin to bypass SSR
Vue.component('medium-editor', MediumEditor)
