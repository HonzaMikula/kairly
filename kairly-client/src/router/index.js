import Vue from 'vue'
import Router from 'vue-router'
import Timeline from '@/components/Timeline'
import PostDetail from '@/components/PostDetail'
import EditionDetail from '@/components/EditionDetail'
import AuthorDetail from '@/components/AuthorDetail'
import Homepage from '@/components/Homepage'
import MySubscription from '@/components/MySubscription'
import MyAuthors from '@/components/MyAuthors'
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
      path: '/editions/:editionId+',
      name: 'Edition Detail',
      component: EditionDetail
    }, {
      path: '/author/:authorId',
      name: 'Author Detail',
      component: AuthorDetail
    }, {
      path: '/homepage',
      name: 'Homepage',
      component: Homepage
    }, {
      path: '/subscription',
      component: MySubscription,
      children: [
        {
          path: 'editions',
          name: 'MyEditions',
          component: MyEditions
        },
        {
          path: 'authors',
          name: 'MyAuthors',
          component: MyAuthors
        }
      ]

    }
  ],
  linkActiveClass: '',
  linkExactActiveClass: 'is-active'
})
