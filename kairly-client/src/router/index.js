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
import Explore from '@/components/explore/Explore'
import Editions from '@/components/editor/Editions'
import SignUp from '@/components/profile/SignUp'
import Settings from '@/components/profile/Settings'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {path: '/', name: 'timeline', component: Timeline},
    {path: '/homepage', name: 'homepage', component: Homepage},

    {path: '/subscription', component: MySubscription, children: [
      {path: '', name: 'subscription', redirect: { name: 'subscription.editions'}},
      {path: 'editions', name: 'subscription.editions', component: MyEditions},
      {path: 'authors', name: 'subscription.authors', component: MyAuthors}
    ]},
    {path: '/explore', name: 'explore', component: Explore},
    {path: '/explore/:tab', component: Explore},
    {path: '/user/settings', component: Settings, name: 'settings'},
    {path: '/join-and-read-with-kairly', component: SignUp, meta: { public: true }},

    {path: '/editions', name: 'author-editions', component: Editions},
    {path: '/post/:postId', name: 'post', component: PostDetail},  // TODO remap to /:author/post--:id

    {path: '/:author', name: 'author', component: AuthorDetail},
    {path: '/:author/:edition', name: 'edition', component: EditionDetail},
    {path: '/:author/:edition/:issue', name: 'issue', component: IssueDetail},



  ],
  linkActiveClass: 'is-active',
  linkExactActiveClass: 'is-active'
})
