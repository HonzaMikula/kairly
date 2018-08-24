import axios from 'axios'

let token = localStorage.getItem("token")
// TODO validate token validity

// TODO move to action to get access to $axios
// https://axios.nuxtjs.org/usage.html
axios.defaults.baseURL = process.env.API_URL
axios.defaults.headers.common['X-Timezone'] = Intl.DateTimeFormat().resolvedOptions().timeZone

if (token) {
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
}

export const clearToken = () => {
  localStorage.removeItem("token")
  token = null;
  delete axios.defaults.headers.common['Authorization']
}

export const createToken = async (username, password) => {
  const res = await axios.post('/token', {username, password})
  token = res.data.token
  localStorage.setItem('token', token)
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
  return token
}

export const getProfile = async () => {
  if (!token) throw Error("Unauthorized")
  const res = await axios.get('/profile')
  return res.data
}

export const getTimeline = async (cursor) => {
  const res = await axios.get('/timeline', {params: {cursor}})
  return res.data
}

export const getNewspaperDetail = async (newspaperId, issue) => {
  const res = await axios.get(`/newspapers/${newspaperId}`, {params: {issue}})
  return res.data
}

export const getRecentIssues = async () => {
  const res = await axios.get('/recent/issues')
  return res.data
}

export const getRecentPosts = async () => {
  const res = await axios.get('/recent/posts')
  return res.data
}

export const getAuthorDetail = async (authorId) => {
  const res = await axios.get(`/authors/${authorId}`)
  return res.data
}

export const getAuthorPosts = async (authorId, cursor) => {
  const res = await axios.get(`/authors/${authorId}/posts`, {params: {cursor}})
  return res.data
}

export const getPost = async (postId) => {
  const res = await axios.get(`/post/${postId}`)
  return res.data.post
}

export const subscribeNewspaper = async (newspaperId) => {
  const res = await axios.post(`/newspapers/${newspaperId}/subscribe`)
  return res.data
}

export const unsubscribeNewspaper = async (newspaperId) => {
   const res = await axios.post(`/newspapers/${newspaperId}/unsubscribe`)
   return res.data
}

export const subscribeAuthor = async (authorId, periodicity) => {
  const res = await axios.post(`/authors/${authorId}/subscribe`, periodicity)
  return res.data
}

export const unsubscribeAuthor = async (authorId) => {
  const res = await axios.post(`/authors/${authorId}/unsubscribe`)
  return res.data
}

export const createNewspaper = async (authorId, newspaper) => {
  const res = await axios.post(`/authors/${authorId}/start-newspaper`, newspaper)
  return res.data.newspaper
}

export const updateNewspaper = async (fullName, fields) => {
  const res = await axios.patch(`/newspapers/${fullName}`, fields)
  return res.data.newspaper
}

export const deleteNewspaper = async (newspaperId) => {
  const res = await axios.delete(`/newspapers/${newspaperId}`)
  return res.data
}

export const getNewspaperBacklog = async newspaperId => {
  const res = await axios.get(`/newspapers/${newspaperId}/backlog`)
  return res.data
}

export const addToBacklog = async (newspaperId, postId) => {
  const res = await axios.put(`/newspapers/${newspaperId}/backlog`, {post: postId})
  return res.data
}

export const deleteFromBacklog = async (newspaperId, postId) => {
  const res = await axios.delete(`/newspapers/${newspaperId}/backlog`, { data: {post: postId}})
  return res.data
}

export const publishBacklog = async (newspaperId, postIds) => {
  const res = await axios.post(`/newspapers/${newspaperId}/backlog/publish`, postIds)
  return res.data
}

export const signUp = async (user) => {
  const res = await axios.post('/signup', user)
  return res.data
}

export const updateProfile = async (profile) => {
  const res = await axios.patch('/profile', profile)
  return res.data
}

export const changePassword = async ({oldPassword, newPassword}) => {
  const res = await axios.post('/change-password', {oldPassword, newPassword})
  return res.data
}

export const getExploreTab = async (tab) => {
  const res = await axios.get(`/explore/${tab}`)
  return res.data
}
