import keyBy from 'lodash/keyBy'

export async function getSubscriptions({ commit, state }) {
  if (state.subscriptions) {
    return state.subscriptions
  }
  const { subscriptions } = await this.$axios.$get('/subscriptions')
  const mappedByKey = {
    'authors': keyBy(subscriptions.authors, 'author'),
    'newspapers': keyBy(subscriptions.newspapers, 'newspaper')
  }
  commit('subscriptions', mappedByKey)
  return mappedByKey
}

export async function getTransactions({ commit, getters }) {
  const { credits, transactions } = await this.$axios.$get(`/transactions`)
  commit('updateCredits', credits)
  return {
    credits,
    transactions: getters['entities/denormalize'](transactions, 'Transaction')
  }
}

export async function getPlatformTransactions({ getters }) {
  const { credits, transactions } = await this.$axios.$get(`/platform-transactions`)
  return {
    credits,
    transactions: getters['entities/denormalize'](transactions, 'Transaction')
  }
}

export async function getNewspaperDetail({ commit, getters }, { newspaperId, issue }) {
  const data = await this.$axios.$get(`/newspapers/${newspaperId}`, { params: {issue} })
  if (data.recommended) {
    data.recommended.forEach(id => commit('recommendedIssue', {id, value: true}))
  }

  data.newspaper = getters['entities/denormalize'](data.newspaper, 'Newspaper')
  data.issue = getters['entities/denormalize'](data.issue, 'Issue')
  return data
}

export async function getNewspapers(store, newspaperIds) {
  const missing = newspaperIds.filter(id => !(id in store.state.entities.newspapers))
  if (missing.length) {
    const promises = missing.map(id => getNewspaperDetail.call(this, store, { newspaperId: id }))
    await Promise.all(promises)
  }
  return newspaperIds.map(id => store.getters['entities/denormalize'](id, 'Newspaper'))
}

export async function getAuthor({ getters }, authorId) {
  const { author, newspapers } = await this.$axios.$get(`/authors/${authorId}`)
  return {
    author: getters['entities/denormalize'](author, 'Author'),
    newspapers: getters['entities/denormalize'](newspapers, 'Newspaper'),
  }
}

export async function getAuthorPosts({ getters }, { authorId, cursor, skipRecommendations }) {
  const params = { cursor, skipRecommendations }
  const resp = await this.$axios.$get(`/authors/${authorId}/posts`, { params })
  return {
    posts: getters['entities/denormalize'](resp.posts, 'Post'),
    cursor: resp.cursor
  }
}

export async function getPost({ getters }, postId) {
  const { post, editorials, recommended } = await this.$axios.$get(`/posts/${postId}`)
  return {
    post: getters['entities/denormalize'](post, 'Post'),
    editorials: getters['entities/denormalize'](editorials, 'EditorialRef'),
    recommended,
  }
}

export async function getDrafts({ getters }) {
  const { posts } = await this.$axios.$get(`/drafts`)
  return getters['entities/denormalize'](posts, 'Post')
}

export async function getPostDraft({ getters }, postId) {
  const { post } = await this.$axios.$get(`/drafts/${postId}`)
  return getters['entities/denormalize'](post, 'Post')
}

export async function getRecentIssues({ getters }, count) {
  const { issues } = await this.$axios.$get(`/recent/issues?count=${count}`)
  return getters['entities/denormalize'](issues, 'Issue')
}

export async function getRecentPosts({ getters }) {
  const { posts } = await this.$axios.$get('/recent/posts')
  return getters['entities/denormalize'](posts, 'Post')
}

export async function getNewAuthors({ getters }, count) {
  const { authors } = await this.$axios.$get(`/explore/new-authors?count=${count}`)
  return getters['entities/denormalize'](authors, 'Author')
}

export async function subscribeNewspaper({ commit }, { fullName, donation, allowSuspended=false }) {
  commit('timeline/invalidate')

  const body = {
    donation
  }
  if (allowSuspended) {
    body.allowSuspended = true
  }
  const { subscription, credits } = await this.$axios.$post(`/newspapers/${fullName}/subscription`, body)
  commit('updateCredits', credits)
  commit('newspaperSubscription', {
    fullName,
    subscription,
  })

  this.$ga.event({
    eventCategory: 'Subscribe newspaper',
    eventAction: fullName,
    eventValue: credits
  })

  return subscription[fullName]
}

export async function loadAuthorPosts({ getters }, { authorId, cursor: requestedCursor }) {
  const { posts, cursor } = await this.$axios.$get(
    `/authors/${authorId}/posts`,
    { params: { cursor: requestedCursor } }
  );

  let prevRecommendation = null
  const mappedPosts = []

  posts.forEach(post => {
    post = getters['entities/denormalize'](post, 'Post')

    if (post.type == 'recommendation-post' || post.type == 'recommendation-issue') {
      if (prevRecommendation === null) {
        prevRecommendation = {
          author: post.author,
          id: `wrapper-${post.id}`,
          type: 'recommendations',
          posts: [],
          issues: [],
        }
         mappedPosts.push(prevRecommendation)
      }
      if (post.type == 'recommendation-post') {
        prevRecommendation.posts.push(post)
      } else {
        prevRecommendation.issues.push(post)
      }
    } else {
      prevRecommendation = null
      mappedPosts.push(post)
    }
  });

  return { posts: mappedPosts, cursor }
}

export async function unsubscribeNewspaper({ commit }, { fullName }) {
  commit('timeline/invalidate')

  const { subscription } = await this.$axios.$delete(`/newspapers/${fullName}/subscription`)
  commit('newspaperSubscription', {
    fullName,
    subscription,
  })

  this.$ga.event({
    eventCategory: 'Unsubscribe newspaper',
    eventAction: fullName
  })

  return subscription ? subscription[fullName] : null
}

export async function subscribeAuthor({ commit }, { author, donation, periodicity, keepStatus=false, allowSuspended=false }) {
  commit('timeline/invalidate')

  const body = { periodicity, donation }
  if (keepStatus) {
    // use when wanted to keep subscption in canceled status but edit just periodicity
    body.keepStatus = true
  }
  if (allowSuspended) {
    body.allowSuspended = true
  }
  const { subscription, credits } = await this.$axios.$post(`/authors/${author.id}/subscription`, body)
  commit('updateCredits', credits)
  commit('authorSubscription', {
    authorId: author.id,
    subscription,
  })

  this.$ga.event({
    eventCategory: 'Subscribe author',
    eventAction: periodicity ? periodicity.frequency : 'renewal',
    eventLabel: author.id
  })

  return subscription[author.id]
}

export async function unsubscribeAuthor({ commit }, { author }) {
  commit('timeline/invalidate')

  const { subscription } = await this.$axios.$delete(`/authors/${author.id}/subscription`)
  commit('authorSubscription', {
    authorId: author.id,
    subscription,
  })

  this.$ga.event({
    eventCategory: 'Subscribe author',
    eventAction: author.id
  })

  return subscription ? subscription[author.id] : null
}

export async function startNewspaper({ commit, getters }, { authorId, newspaper: postData }) {
  const data = await this.$axios.$post(`/authors/${authorId}/start-newspaper`, postData)
  const newspaper = getters['entities/denormalize'](data.newspaper, 'Newspaper')
  commit('appendOwnedNewspaper', {
    newspaper,
  })

  this.$ga.event({
    eventCategory: 'Start newspaper',
    eventAction: newspaper.fullName
  })

  return newspaper
}

export async function updateNewspaper({ commit }, { fullName, fields }) {
  const { newspaper } = await this.$axios.$patch(`/newspapers/${fullName}`, fields)
  commit('entities/newspaper', { newspaper })

  this.$ga.event({
    eventCategory: 'Update newspaper',
    eventAction: newspaper.fullName
  })

  return newspaper
}

export async function deleteNewspaper({ commit }, newspaper) {
  await this.$axios.delete(`/newspapers/${newspaper.fullName}`)
  commit('removeNewspaper', { newspaper })

  this.$ga.event({
    eventCategory: 'Delete newspaper',
    eventAction: newspaper.fullName
  })
}

export const afterLogout = ({ commit }) => {
  commit('backlog/resetState')
  commit('timeline/resetState')
  commit('entities/resetState')
  commit('resetState')
}
