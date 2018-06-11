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

export const getEditions = () => {
  if (!token) return Promise.reject();
  return agent
    .get(API_URI + '/editions')
    .then(res => res.body)
}

export const getAuthors = () => {
  if (!token) return Promise.reject();
  return agent
    .get(API_URI + '/authors')
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

export const getAuthorDetail = (authorId, topic) => {
  if (!token) return Promise.reject()
  let req = agent.get(API_URI + '/author/' + authorId)
  // TODO review api design here, it should be rather in url but now it clashes with author/posts endpoint
  if (topic) { req = req.query({ topic }) }
  return req.then(res => res.body)
}

export const getAuthorPosts = (authorId, topic, cursor) => {
  if (!token) return Promise.reject()
  let req = agent.get(API_URI + '/author/' + authorId + '/posts')
  if (topic) { req = req.query({ topic }) }
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
    .post(API_URI + '/subscribe/' + editionId)
    .then(res => res.body)
}

export const unsubscribeEdition = editionId => {
  if (!token) return Promise.reject();
  return agent
    .post(API_URI + '/unsubscribe/' + editionId)
    .then(res => res.body)
}

export const subscribeAuthor = (author, period, time, dow) => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.VUE_APP_BASE_URI + author.followUrl)
    .send({period, time, dow})
    .then(res => res.body)
}

export const unsubscribeAuthor = author => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.VUE_APP_BASE_URI + author.unfollowUrl)
    .then(res => res.body)
}
