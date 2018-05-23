import request from 'superagent'

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
    .post(process.env.BACKEND_BASE + '/api/token')
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
    .get(process.env.BACKEND_BASE + '/api/profile')
    .then(res => res.body.user)
}

export const getTimeline = (cursor) => {
  if (!token) return Promise.reject();
  let url = process.env.BACKEND_BASE + '/api/timeline'
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
    .get(process.env.BACKEND_BASE + '/api/editions')
    .then(res => res.body)
}

export const getEditionDetail = (editionId) => {
  if (!token) return Promise.reject();
  return agent
    .get(process.env.BACKEND_BASE + '/api/editions/' + editionId)
    .then(res => res.body)
}

export const getAuthorDetail = (authorId) => {
  if (!token) return Promise.reject();
  return agent
    .get(process.env.BACKEND_BASE + '/api/author/' + authorId)
    .then(res => res.body)
}

export const getAuthorPosts = (authorId, cursor) => {
  if (!token) return Promise.reject();
  let url = process.env.BACKEND_BASE + '/api/author/' + authorId + '/posts'
  if (cursor) {
    url += '?cursor=' + cursor
  }
  return agent
    .get(url)
    .then(res => res.body)
}

export const getPost = (postId) => {
  if (!token) return Promise.reject();
  return agent
    .get(process.env.BACKEND_BASE + '/api/post/'  + postId)
    .then(res => res.body.post)
}

export const subscribeEdition = editionId => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.BACKEND_BASE + '/api/subscribe/' + editionId)
    .then(res => res.body)
}

export const unsubscribeEdition = editionId => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.BACKEND_BASE + '/api/unsubscribe/' + editionId)
    .then(res => res.body)
}

export const subscribeAuthor = (author, period) => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.BACKEND_BASE + author.followUrl)
    .send({period})
    .then(res => res.body)
}

export const unsubscribeAuthor = author => {
  if (!token) return Promise.reject();
  return agent
    .post(process.env.BACKEND_BASE + author.unfollowUrl)
    .then(res => res.body)
}
