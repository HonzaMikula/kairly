import request from 'superagent'

const API_URI = process.env.VUE_APP_BASE_URI + '/api'

let token = localStorage.getItem("token")
let agent = createAgent(token)


function createAgent(token) {
  let agent = request.agent()
    .set('X-Timezone', Intl.DateTimeFormat().resolvedOptions().timeZone)
  if (token) {
    agent = agent.set('Authorization', 'Bearer ' + token)
  }
  return agent
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

export const getNewspaperDetail = (newspaperId, issueId=null) => {
  if (!token) return Promise.reject();
  let url = `${API_URI}/newspapers/${newspaperId}`
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
  let req = agent.get(`${API_URI}/authors/${authorId}`)
  return req.then(res => res.body)
}

export const getAuthorPosts = (authorId, cursor) => {
  if (!token) return Promise.reject()
  let req = agent.get(`${API_URI}/authors/${authorId}/posts`)
  if (cursor) { req = req.query({ cursor }) }
  return req.then(res => res.body)
}

export const getPost = (postId) => {
  if (!token) return Promise.reject();
  return agent
    .get(`${API_URI}/post/${postId}`)
    .then(res => res.body.post)
}

export const subscribeNewspaper = newspaperId => {
  if (!token) return Promise.reject()
  return agent
    .post(`${API_URI}/newspapers/${newspaperId}/subscribe`)
    .then(res => res.body)
}

export const unsubscribeNewspaper = newspaperId => {
  if (!token) return Promise.reject();
  return agent
    .post(`${API_URI}/newspapers/${newspaperId}/unsubscribe`)
    .then(res => res.body)
}

export const subscribeAuthor = (authorId, periodicity) => {
  if (!token) return Promise.reject();
  return agent
    .post(`${API_URI}/authors/${authorId}/subscribe`)
    .send(periodicity)
    .then(res => res.body)
}

export const unsubscribeAuthor = authorId => {
  if (!token) return Promise.reject();
  return agent
    .post(`${API_URI}/authors/${authorId}/unsubscribe`)
    .then(res => res.body)
}

export const createNewspaper = (authorId, newspaper) => {
  //const { title, description, image, period, time, dow } = newspaper
  if (!token) return Promise.reject();
  return agent
    .post(`${API_URI}/authors/${authorId}/start-newspaper`)
    .send(newspaper)
    .then(res => res.body)
}

export const updateNewspaper = (fullName, fields) => {
  if (!token) return Promise.reject();
  return agent
    .patch(`${API_URI}/newspapers/${fullName}`)
    .send(fields)
    .then(res => res.body)
}

export const deleteNewspaper = newspaperId => {
  if (!token) return Promise.reject();
  return agent
    .delete(`${API_URI}/newspapers/${newspaperId}`)
}

export const getNewspaperBacklog = newspaperId => {
  if (!token) return Promise.reject();
  return agent
    .get(`${API_URI}/newspapers/${newspaperId}/backlog`)
    .then(res => res.body)
}

export const addToBacklog = (newspaperId, postId) => {
  if (!token) return Promise.reject();
  return agent
    .put(`${API_URI}/newspapers/${newspaperId}/backlog`)
    .send({post: postId})
}

export const deleteFromBacklog = (newspaperId, postId) => {
  if (!token) return Promise.reject();
  return agent
    .delete(`${API_URI}/newspapers/${newspaperId}/backlog`)
    .send({post: postId})
}

export const publishBacklog = (newspaperId, postIds) => {
  if (!token) return Promise.reject();
  return agent
    .post(`${API_URI}/newspapers/${newspaperId}/backlog/publish`)
    .send(postIds)
}

export const signUp = user => {
  return agent
    .post(API_URI + '/signup')
    .send(user)
}

export const updateProfile = profile => {
  if (!token) return Promise.reject();
  return agent
    .patch(API_URI + '/profile')
    .send(profile)
}

export const changePassword = ({oldPassword, newPassword}) => {
  if (!token) return Promise.reject();
  return agent
    .post(API_URI + '/change-password')
    .send({oldPassword, newPassword})
}

export const getExploreTab = tab => {
  if (!token) return Promise.reject();
  return agent
    .get(`${API_URI}/explore/${tab}`)
    .then(res => res.body)
}
