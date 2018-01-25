import Vue from 'vue'
import Router from 'vue-router'
import Timeline from '@/components/Timeline'
import Post from '@/components/Post'
import Editions from '@/components/Editions'
import Editor from '@/components/Editor'
import ReadLater from '@/components/ReadLater'
import Homepage from '@/components/Homepage'
import MyEditions from '@/components/MyEditions'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Timeline',
      component: Timeline
    }, {
      path: '/post/:postId',
      name: 'Post',
      component: Post
    }, {
      path: '/editions',
      name: 'Editions',
      component: Editions
    }, {
      path: '/editor',
      name: 'Editor',
      component: Editor
    }, {
      path: '/read-later',
      name: 'ReadLater',
      component: ReadLater
    }, {
      path: '/homepage',
      name: 'Homepage',
      component: Homepage
    }, {
      path: '/my-editions',
      name: 'MyEditions',
      component: MyEditions
    }
  ],
  linkActiveClass: '',
  linkExactActiveClass: 'is-active'
})
