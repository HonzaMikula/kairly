export async function getSubscriptions({ commit, state }) {
  if (state.subscriptions) {
    return state.subscriptions
  }
  const { newspapers, subscriptions } = await this.$axios.$get('/subscriptions')
  newspapers.forEach(newspaper => commit('newspaper', { newspaper }))
  commit('subscriptions', subscriptions)
  return subscriptions
}

export async function getTransactions({ commit, state }) {
  const { credits, transactions, newspapers } = await this.$axios.$get(`/transactions`)

  transactions.forEach(t => {
    if (t.source.newspaper) t.source.newspaper = newspapers[t.source.newspaper]
    if (t.target.newspaper) t.target.newspaper = newspapers[t.target.newspaper]
  })

  commit('updateCredits', credits)
  Object.keys(newspapers).forEach(newspaper => commit('newspaper', { newspaper }))

  return transactions
}



export async function getNewspaperDetail({ commit }, { newspaperId, issue }) {
  const data = await this.$axios.$get(`/newspapers/${newspaperId}`, { params: {issue} })
  commit('newspaper', { newspaper: data.newspaper })
  if (data.recommended) {
    data.recommended.forEach(id => commit('recommendedIssue', {id, value: true}))
  }
  return data
}

export async function getNewspapers(store, newspaperIds) {
  const missing = newspaperIds.filter(id => !(id in store.state.newspapers))
  if (missing.length) {
    const promises = missing.map(id => getNewspaperDetail.call(this, store, { newspaperId: id }))
    await Promise.all(promises)
  }
  return newspaperIds.map(id => store.state.newspapers[id])
}

export async function getAuthor({ commit, state, dispatch }, authorId) {
  const data = await this.$axios.$get(`/authors/${authorId}`)
  data.newspapers.forEach(n => dispatch('newspaperUpdated', n))
  return data
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

  return subscription
}

export async function loadAuthorPosts({ commit }, { authorId, cursor: requestedCursor }) {
  const { posts, cursor } = await this.$axios.$get(
    `/authors/${authorId}/posts`,
    { params: { cursor: requestedCursor } }
  );

  let prevRecommendation = null
  const mappedPosts = []

  posts.forEach(post => {
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

  return subscription
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

  return subscription
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

  return subscription
}

export async function startNewspaper({ commit }, { authorId, newspaper: postData }) {
  const { newspaper } = await this.$axios.$post(`/authors/${authorId}/start-newspaper`, postData)
  commit('newspaper', { newspaper })
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
  commit('newspaper', { newspaper })

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

export const newspaperUpdated = ({ commit }, newspaper) => {
  commit('newspaper', { newspaper })
}


export const afterLogout = ({ commit }) => {
  commit('backlog/resetState')
  commit('timeline/resetState')
  commit('resetState')
}
