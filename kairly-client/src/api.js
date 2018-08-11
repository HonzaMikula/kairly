import axios from 'axios'

const API_URI = process.env.VUE_APP_BASE_URI + '/api'

let token = localStorage.getItem("token")
let ax = createAxiosInstance(token)


function createAxiosInstance(token) {
  const headers = {
    'X-Timezone': Intl.DateTimeFormat().resolvedOptions().timeZone
  }

  if (token) {
    headers.Authorization = 'Bearer ' + token
  }
  return axios.create({
    baseURL: API_URI,
    headers
  })
}

export const clearToken = () => {
  localStorage.removeItem("token")
  token = null;
  ax = null;
}

export const createToken = (username, password) => {
  return axios
    .post(API_URI + '/token')
    .send({username, password})
    .then(res => {
       token = res.data.token
       localStorage.setItem('token', token)
       ax = createAxiosInstance(token)
       return token;
    })
}

export const getProfile = () => {
  if (!token) return Promise.reject();
  return ax
    .get(API_URI + '/profile')
    .then(res => res.data)
}

export const getTimeline = (cursor) => {
  if (!token) return Promise.reject();
  let url = API_URI + '/timeline'
  if (cursor) {
    url += '?cursor=' + cursor
  }
  return ax
    .get(url)
    .then(res => res.data)
}

export const getNewspaperDetail = (newspaperId, issueId=null) => {
  if (!token) return Promise.reject();
  let url = `${API_URI}/newspapers/${newspaperId}`
  if (issueId) {
    url += '?issue=' + issueId
  }
  return ax
    .get(url)
    .then(res => res.data)
}

export const getRecentIssues = () => {
  if (!token) return Promise.reject();
  let url = API_URI + '/recent/issues'
  return ax
    .get(url)
    .then(res => res.data)
}

export const getRecentPosts = () => {
  if (!token) return Promise.reject();
  let url = API_URI + '/recent/posts'
  return ax
    .get(url)
    .then(res => res.data)
}

export const getAuthorDetail = (authorId) => {
  if (!token) return Promise.reject()
  let req = ax.get(`${API_URI}/authors/${authorId}`)
  return req.then(res => res.data)
}

export const getAuthorPosts = (authorId, cursor) => {
  if (!token) return Promise.reject()
  let req = ax.get(`${API_URI}/authors/${authorId}/posts`)
  if (cursor) { req = req.query({ cursor }) }
  return req.then(res => res.data)
}

export const getPost = (postId) => {
  if (!token) return Promise.reject();
  return ax
    .get(`${API_URI}/post/${postId}`)
    .then(res => res.data.post)
}

export const subscribeNewspaper = newspaperId => {
  if (!token) return Promise.reject()
  return ax
    .post(`${API_URI}/newspapers/${newspaperId}/subscribe`)
    .then(res => res.data)
}

export const unsubscribeNewspaper = newspaperId => {
  if (!token) return Promise.reject();
  return ax
    .post(`${API_URI}/newspapers/${newspaperId}/unsubscribe`)
    .then(res => res.data)
}

export const subscribeAuthor = (authorId, periodicity) => {
  if (!token) return Promise.reject();
  return ax
    .post(`${API_URI}/authors/${authorId}/subscribe`)
    .send(periodicity)
    .then(res => res.data)
}

export const unsubscribeAuthor = authorId => {
  if (!token) return Promise.reject();
  return ax
    .post(`${API_URI}/authors/${authorId}/unsubscribe`)
    .then(res => res.data)
}

export const createNewspaper = (authorId, newspaper) => {
  //const { title, description, image, period, time, dow } = newspaper
  if (!token) return Promise.reject();
  return ax
    .post(`${API_URI}/authors/${authorId}/start-newspaper`)
    .send(newspaper)
    .then(res => res.data)
}

export const updateNewspaper = (fullName, fields) => {
  if (!token) return Promise.reject();
  return ax
    .patch(`${API_URI}/newspapers/${fullName}`)
    .send(fields)
    .then(res => res.data)
}

export const deleteNewspaper = newspaperId => {
  if (!token) return Promise.reject();
  return ax
    .delete(`${API_URI}/newspapers/${newspaperId}`)
}

export const getNewspaperBacklog = newspaperId => {
  if (!token) return Promise.reject();
  return ax
    .get(`${API_URI}/newspapers/${newspaperId}/backlog`)
    .then(res => res.data)
}

export const addToBacklog = (newspaperId, postId) => {
  if (!token) return Promise.reject();
  return ax
    .put(`${API_URI}/newspapers/${newspaperId}/backlog`)
    .send({post: postId})
}

export const deleteFromBacklog = (newspaperId, postId) => {
  if (!token) return Promise.reject();
  return ax
    .delete(`${API_URI}/newspapers/${newspaperId}/backlog`)
    .send({post: postId})
}

export const publishBacklog = (newspaperId, postIds) => {
  if (!token) return Promise.reject();
  return ax
    .post(`${API_URI}/newspapers/${newspaperId}/backlog/publish`)
    .send(postIds)
}

export const signUp = user => {
  return ax
    .post(API_URI + '/signup')
    .send(user)
}

export const updateProfile = profile => {
  if (!token) return Promise.reject();
  return ax
    .patch(API_URI + '/profile')
    .send(profile)
    .then(res => res.data)
}

export const changePassword = ({oldPassword, newPassword}) => {
  if (!token) return Promise.reject();
  return ax
    .post(API_URI + '/change-password')
    .send({oldPassword, newPassword})
}

export const getExploreTab = tab => {
  if (!token) return Promise.reject();
  return ax
    .get(`${API_URI}/explore/${tab}`)
    .then(res => res.data)
}
