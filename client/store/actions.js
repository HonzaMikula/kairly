

// function onError(err, commit) {
//   commit('showError', (err + '') || 'Request failed')
//   // eslint-disable-next-line no-console
//   console.log(err)
// }


export async function getUserBacklog({ commit, state }) {
  if (state.backlog) {
    return state.backlog
  }
  const { backlog } = await this.$axios.$get('/backlog')
  commit('backlog', backlog)
  return backlog
}

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

export async function loadTimeline({ commit, state }, { date, cachedOnly=false}) {
  let cacheKey = date
  // TODO check not only valid to but also change of hour or too old timeline
  // but this is not important now
  if (!cacheKey && state.today && state.today.validTo > (Date.now() / 1000)) {
    // if today is requested (no date arg) then lookup to helper structure which
    // keeps current value of "today" (mind that "today" may not match real today)
    cacheKey = state.today.date
  }

  if (state.timeline[cacheKey]) {
    return cacheKey
  }

  if (cachedOnly) {
    return null
  }

  const { status, data } = await this.$axios.get('/timeline', {params: {date}})

  if (status === 204) {
    commit('timelineHasNoActiveSubscriptions')
    return null
  }

  // group recommendations
  data.issues.forEach(issue => {
    const posts = []
    const recommendedPosts = []
    const recommendedIssues = []
    issue.posts.forEach(post => {
      if (post.type == 'recommendation-post') {
        recommendedPosts.push(post)
      } else if (post.type == 'recommendation-issue') {
        recommendedIssues.push(post)
      } else {
        posts.push(post)
      }
    })
    if (recommendedPosts.length || recommendedIssues.length) {
      const sample = recommendedPosts.length ? recommendedPosts[0] : recommendedIssues[0]
      posts.push({
        author: sample.author,
        id: `wrapper-${sample.id}`,
        type: 'recommendations',
        posts: recommendedPosts,
        issues: recommendedIssues,
      })
      issue.posts = posts
    }
  })

  if (data.recommended) {
    data.recommended.forEach(id => commit('recommendedIssue', {id, value: true}))
  }

  if (!date) {
    commit('today', {date: data.date, validTo: data.validTo})
  }
  commit('timelineReceived', data)
  return data.date
}

export const invalidateTimeline = ({ commit }) => {
  commit('invalidateTimeline')
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

export async function loadNewspaperBacklog({ commit, state, dispatch }, fullName) {
  const { backlog, publish, currentMonth } = await this.$axios.$get(`/newspapers/${fullName}/backlog`)
  commit('newspaperBacklog', {
    fullName,
    postsBacklog: backlog.reverse(),
    postsPublished: publish,
    currentMonthStats: currentMonth
  })
}

export async function backlogPublish({ commit, state}, {newspaper, log}) {
  const { fullName } = newspaper
  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[fullName]
  const modifiedBacklog = [...postsBacklog]
  const modifiedPublished = [...postsPublished]
  modifiedBacklog.splice(modifiedBacklog.indexOf(log), 1)
  modifiedPublished.push(log)
  commit('newspaperBacklog', {
    fullName,
    postsBacklog: modifiedBacklog,
    postsPublished: modifiedPublished,
    currentMonthStats
  })
  const postIds = modifiedPublished.map(item => item.post.id)
  await this.$axios.$post(`/newspapers/${fullName}/backlog/publish`, postIds)
  commit('backlogSetPostState', {newspaper: fullName, postId: log.post.id, val: 'P'})
}

export async function backlogUndoPublish({ commit, state}, {newspaper, log}) {
  const { fullName } = newspaper
  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[fullName]
  const modifiedBacklog = [...postsBacklog]
  const modifiedPublished = [...postsPublished]
  modifiedBacklog.push(log)
  modifiedPublished.splice(modifiedPublished.indexOf(log), 1)
  commit('newspaperBacklog', {
    fullName,
    postsBacklog: modifiedBacklog,
    postsPublished: modifiedPublished,
    currentMonthStats
  })
  const postIds = modifiedPublished.map(item => item.post.id)
  await this.$axios.$post(`/newspapers/${fullName}/backlog/publish`, postIds)
  commit('backlogSetPostState', {newspaper: fullName, postId: log.post.id, val: 'C'})
}

export async function backlogMoveUp({ commit, state}, {newspaper, index}) {
  const { fullName } = newspaper
  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[fullName]
  const log = postsPublished[index]
  const modified = [...postsPublished]
  modified[index] = postsPublished[index - 1]
  modified[index - 1] = log
  commit('newspaperBacklog', {
    fullName,
    postsBacklog,
    postsPublished: modified,
    currentMonthStats
  })
  const postIds = modified.map(item => item.post.id)
  await this.$axios.$post(`/newspapers/${fullName}/backlog/publish`, postIds)
}

export async function backlogMoveDown({ commit, state}, {newspaper, index}) {
  const { fullName } = newspaper
  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[fullName]
  const log = postsPublished[index]
  const modified = [...postsPublished]
  modified[index] = postsPublished[index + 1]
  modified[index + 1] = log
  commit('newspaperBacklog', {
    fullName,
    postsBacklog,
    postsPublished: modified,
    currentMonthStats
  })
  const postIds = modified.map(item => item.post.id)
  await this.$axios.$post(`/newspapers/${fullName}/backlog/publish`, postIds)
}

export async function removeFromNewspaperBacklog({ commit, state }, { newspaper, log }) {
  const { fullName } = newspaper
  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[fullName]
  const modifiedBacklog = [...postsBacklog]
  modifiedBacklog.splice(modifiedBacklog.indexOf(log), 1)
  commit('newspaperBacklog', {
    fullName,
    postsBacklog: modifiedBacklog,
    postsPublished,
    currentMonthStats
  })

  // TODO to have better user experience, post can be removed immediately
  // and reverted when api call fails
  await this.$axios.delete(`/newspapers/${newspaper.fullName}/backlog`, { data: {post: log.post.id}})
  commit('backlogRemove', {
    newspaperId: newspaper.fullName,
    postId: log.post.id,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Stop considering for newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
}

export async function addLinkToBacklog({ commit, state }, { newspaper, url }) {
  const { fullName } = newspaper
  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[fullName]
  const resp = await this.$axios.$post(`/newspapers/${newspaper.fullName}/backlog/links`, {url})
  if (resp.post) {
    const modifiedBacklog = [...postsBacklog]
    modifiedBacklog.unshift({ post: resp.post, editorial: null })
    commit('newspaperBacklog', {
      fullName,
      postsBacklog: modifiedBacklog,
      postsPublished,
      currentMonthStats
    })

    commit('backlogAdd', {
      newspaperId: newspaper.fullName,
      postId: resp.post.id,
      meta: {
        analytics: [
          ['event', {
            eventCategory: 'Consider for newspaper',
            eventAction: newspaper.fullName
          }]
        ]
      }
    })
  }
}

export async function saveEditorial({ commit, state }, { newspaperId, postId, title, content, position}) {
  const editorial = await this.$axios.$post(`/newspapers/${newspaperId}/editorials/${postId}`, {
    title,
    content,
    position,
  })

  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[newspaperId]
  const idx = postsPublished.findIndex(({post}) => post.id === postId)
  const log = postsPublished[idx]
  const modified = [...postsPublished]
  modified[idx] = {...log, editorial}

  commit('newspaperBacklog', {
    fullName: newspaperId,
    postsBacklog,
    postsPublished: modified,
    currentMonthStats
  })
}

export async function removeEditorial({ commit, state }, { newspaperId, postId}) {
  await this.$axios.$delete(`/newspapers/${newspaperId}/editorials/${postId}`)
  const { postsBacklog, postsPublished, currentMonthStats } = state.newspaperBacklog[newspaperId]
  const idx = postsPublished.findIndex(({post}) => post.id === postId)
  const log = postsPublished[idx]
  const modified = [...postsPublished]
  modified[idx] = {...log, editorial: null}

  commit('newspaperBacklog', {
    fullName: newspaperId,
    postsBacklog,
    postsPublished: modified,
    currentMonthStats
  })
}


export async function subscribeNewspaper({ commit }, { fullName, donation, allowSuspended=false }) {
  commit('invalidateTimeline')

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
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Subscribe newspaper',
          eventAction: fullName
        }]
      ]
    }
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
  commit('invalidateTimeline')

  const { subscription } = await this.$axios.$delete(`/newspapers/${fullName}/subscription`)
  commit('newspaperSubscription', {
    fullName,
    subscription,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Unsubscribe newspaper',
          eventAction: fullName
        }]
      ]
    }
  })
  return subscription
}

export async function subscribeAuthor({ commit }, { author, donation, periodicity, keepStatus=false, allowSuspended=false }) {
  commit('invalidateTimeline')

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
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Subscribe author',
          eventAction: periodicity ? periodicity.frequency : 'renewal',
          eventLabel: author.id
        }]
      ]
    }
  })
  return subscription
}

export async function unsubscribeAuthor({ commit }, { author }) {
  commit('invalidateTimeline')

  const { subscription } = await this.$axios.$delete(`/authors/${author.id}/subscription`)
  commit('authorSubscription', {
    authorId: author.id,
    subscription,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Subscribe author',
          eventAction: author.id
        }]
      ]
    }
  })
  return subscription
}

export async function startNewspaper({ commit }, { authorId, newspaper: postData }) {
  const { newspaper } = await this.$axios.$post(`/authors/${authorId}/start-newspaper`, postData)
  commit('newspaper', { newspaper })
  commit('appendOwnedNewspaper', {
    newspaper,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Start newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
  return newspaper
}

export async function updateNewspaper({ commit }, { fullName, fields }) {
  const { newspaper } = await this.$axios.$patch(`/newspapers/${fullName}`, fields)
  commit('newspaper', {
    newspaper,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Update newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
  return newspaper
}

export async function deleteNewspaper({ commit }, newspaper) {
  await this.$axios.delete(`/newspapers/${newspaper.fullName}`)
  commit('removeNewspaper', {
    newspaper,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Delete newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
}

export async function addToBacklog({ commit }, { newspaper, post }) {
  // TODO to have better user experience, post can be added immediately
  // and reverted when api call fails
  await this.$axios.put(`/newspapers/${newspaper.fullName}/backlog`, {post: post.id})
  commit('backlogAdd', {
    newspaperId: newspaper.fullName,
    postId: post.id,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Consider for newspaper',
          eventAction: newspaper.fullName
        }]
      ]
    }
  })
}

export async function removeFromBacklog({ commit }, { newspaper, post }) {
  try {
    // TODO to have better user experience, post can be removed immediately
    // and reverted when api call fails
    await this.$axios.delete(`/newspapers/${newspaper.fullName}/backlog`, { data: { post: post.id } })
    commit('backlogRemove', {
      newspaperId: newspaper.fullName,
      postId: post.id,
      meta: {
        analytics: [
          ['event', {
            eventCategory: 'Stop considering for newspaper',
            eventAction: newspaper.fullName
          }]
        ]
      }
    })
  } catch (err) {
    onError(err, commit)
  }
}

export const newspaperUpdated = ({ commit }, newspaper) => {
  commit('newspaper', { newspaper })
}

export const expandIssue = ({ commit }, issueId) => {
  commit('expandIssue', {
    issueId,
    meta: {
      analytics: [
        ['event', {
          eventCategory: 'Show more (issue)',
          eventAction: issueId
        }]
      ]
    }
  })
}

export const afterLogout = ({ commit }) => {
  commit('resetState')
}
