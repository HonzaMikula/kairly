import Vue from 'vue'
import Router from 'vue-router'
import Timeline from '@/components/Timeline'
import PostDetail from '@/components/PostDetail'
import EditionDetail from '@/components/EditionDetail'
import AuthorDetail from '@/components/AuthorDetail'
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
      component: PostDetail
    }, {
      path: '/editions',
      name: 'Editions',
      component: Editions
    }, {
      path: '/editions/:editionId+',
      name: 'Edition Detail',
      component: EditionDetail
    }, {
      path: '/author/:authorId',
      name: 'Author Detail',
      component: AuthorDetail
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
