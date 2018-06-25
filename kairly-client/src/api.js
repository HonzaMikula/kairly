import request from 'superagent'

const API_URI = process.env.VUE_APP_BASE_URI + '/api'

let token = localStorage.getItem("token")
let agent = createAgent(token)


function createAgent(token) {
  if (!token) {
    return null
  }
  return request.agent()
    .set('Authorization', 'Bearer ' + token)
    .set('X-Timezone', new Date().getTimezoneOffset())
}

export const clearToken = () => {
  localStorage.removeItem("token")
  token = null;
  agent = null;
}

export const createToken = (username, password) => {
  return request
    .post(API_URI + '/token')
    .send({username, password})
    .then(res => {
       token = res.body.token
       localStorage.setItem('token', token)
       agent = createAgent(token)
       return token;
    })
}

export const getProfile = () => {
  if (!token) return Promise.reject();
  return agent
    .get(API_URI + '/profile')
    .then(res => res.body)
}

export const getTimeline = (cursor) => {
  if (!token) return Promise.reject();
  let url = API_URI + '/timeline'
  if (cursor) {
    url += '?cursor=' + cursor
  }
  return agent
    .get(url)
    .then(res => res.body)
}

export const getUserEditions = () => {
  if (!token) return Promise.reject();
  return agent
    .get(API_URI + '/user/editions')
    .then(res => res.body)
}

export const getUserAuthors = () => {
  if (!token) return Promise.reject();
  return agent
    .get(API_URI + '/user/authors')
    .then(res => res.body)
}

export const getEditionDetail = (editionId, issueId=null) => {
  if (!token) return Promise.reject();
  let url = API_URI + '/editions/' + editionId
  if (issueId) {
    url += '?issue=' + issueId
  }
  return agent
    .get(url)
    .then(res => res.body)
}

export const getRecentIssues = () => {
  if (!token) return Promise.reject();
  let url = API_URI + '/recent/issues'
  return agent
    .get(url)
    .then(res => res.body)
}

export const getRecentPosts = () => {
  if (!token) return Promise.reject();
  let url = API_URI + '/recent/posts'
  return agent
    .get(url)
    .then(res => res.body)
}

export const getAuthorDetail = (authorId) => {
  if (!token) return Promise.reject()
  let req = agent.get(API_URI + '/authors/' + authorId)
  return req.then(res => res.body)
}

export const getAuthorPosts = (authorId, cursor) => {
  if (!token) return Promise.reject()
  let req = agent.get(API_URI + '/authors/' + authorId + '/posts')
  if (cursor) { req = req.query({ cursor }) }
  return req.then(res => res.body)
}

export const getPost = (postId) => {
  if (!token) return Promise.reject();
  return agent
    .get(API_URI + '/post/'  + postId)
    .then(res => res.body.post)
}

export const subscribeEdition = editionId => {
  if (!token) return Promise.reject()
  return agent
    .post(API_URI + '/editions/' + editionId + '/subscribe')
    .then(res => res.body)
}

export const unsubscribeEdition = editionId => {
  if (!token) return Promise.reject();
  return agent
    .post(API_URI + '/editions/' + editionId + '/unsubscribe')
    .then(res => res.body)
}

export const subscribeAuthor = (author, periodicity) => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.VUE_APP_BASE_URI + author.followUrl)
    .send(periodicity)
    .then(res => res.body)
}

export const unsubscribeAuthor = author => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.VUE_APP_BASE_URI + author.unfollowUrl)
    .then(res => res.body)
}

export const createEdition = (authorId, edition) => {
  //const { title, description, image, period, time, dow } = edition
  if (!token) return Promise.reject();
  return agent
    .post(API_URI + '/authors/' + authorId + '/new-edition')
    .send(edition)
    .then(res => res.body)
}

export const deleteEdition = editionId => {
  if (!token) return Promise.reject();
  return agent
    .delete(API_URI + '/editions/' + editionId)
}

export const getEditionBacklog = editionId => {
  if (!token) return Promise.reject();
  return agent
    .get(API_URI + '/editions/' + editionId + '/backlog')
    .then(res => res.body)
}

export const addToBacklog = (editionId, postId, publish=false) => {
  if (!token) return Promise.reject();
  return agent
    .put(API_URI + '/editions/' + editionId + '/backlog')
    .send({post: postId, publish})
}

export const deleteFromBacklog = (editionId, postId) => {
  if (!token) return Promise.reject();
  return agent
    .delete(API_URI + '/editions/' + editionId + '/backlog')
    .send({post: postId})
}
