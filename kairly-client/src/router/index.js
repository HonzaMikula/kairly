import Vue from 'vue'
import Router from 'vue-router'
import Timeline from '@/components/Timeline'
import PostDetail from '@/components/PostDetail'
import EditionDetail from '@/components/EditionDetail'
import IssueDetail from '@/components/IssueDetail'
import AuthorDetail from '@/components/AuthorDetail'
import Homepage from '@/components/Homepage'
import MySubscription from '@/components/my-subscription/MySubscription'
import MyAuthors from '@/components/my-subscription/Authors'
import MyEditions from '@/components/my-subscription/Editions'
import Explore from '@/components/my-subscription/Explore'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {path: '/', name: 'timeline', component: Timeline},
    {path: '/post/:postId', name: 'post', component: PostDetail},
    {path: '/editions/:editionId([^\/]+/[^\/]+)', name: 'edition', component: EditionDetail},
    {path: '/editions/:editionId([^\/]+/[^\/]+)/:issueId', name: 'issue', component: IssueDetail},
    {path: '/author/:authorId', name: 'author', component: AuthorDetail},
    {path: '/author/:authorId/:topic', name: 'topic', component: AuthorDetail},
    {path: '/homepage', name: 'homepage', component: Homepage},
    {path: '/subscription', component: MySubscription, children: [
      {path: '', name: 'subscription', redirect: { name: 'subscription.editions'}},
      {path: 'editions', name: 'subscription.editions', component: MyEditions},
      {path: 'authors', name: 'subscription.authors', component: MyAuthors},
      {path: 'explore', name: 'subscription.explore', component: Explore}
    ]}
  ],
  linkActiveClass: 'is-active',
  linkExactActiveClass: 'is-active'
})
