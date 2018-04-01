import request from 'superagent'

let token = localStorage.getItem("token")

export const clearToken = () => {
  localStorage.removeItem("token")
  token = null;
}

export const createToken = (username, password) => {
  return request
    .post(process.env.BACKEND_BASE + '/api/token')
    .send({username, password})
    .then(res => {
       token = res.body.token
       localStorage.setItem('token', token)
       return token;
    })
}

export const getProfile = () => {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/profile')
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body.user)
}

export const getTimeline = (cursor) => {
  if (!token) return Promise.reject();
  let url = process.env.BACKEND_BASE + '/api/timeline'
  if (cursor) {
    url += '?cursor=' + cursor
  }
  return request
    .get(url)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

export const getEditions = () => {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/editions')
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

export const getEditionDetail = (editionId) => {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/editions/' + editionId)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

export const getAuthorDetail = (authorId) => {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/author/' + authorId)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

export const getAuthorPosts = (authorId, cursor) => {
  if (!token) return Promise.reject();
  let url = process.env.BACKEND_BASE + '/api/author/' + authorId + '/posts'
  if (cursor) {
    url += '?cursor=' + cursor
  }
  return request
    .get(url)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

export const getPost = (postId) => {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/post/'  + postId)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body.post)
}

export const postSubscription = (editionId, subscribe) => {
  if (!token) return Promise.reject();
  return request
    .post(process.env.BACKEND_BASE + '/api/subscribe/' + editionId)
    .set('Authorization', 'Bearer ' + token)
    .send({subscribe})
    .then(res => res.body)
}

export const postAuthorSubsription = (author, subscribe) => {
  if (!token) return Promise.reject();
  return request
    .post(process.env.BACKEND_BASE + author.followUrl)
    .set('Authorization', 'Bearer ' + token)
    .send({subscribe})
    .then(res => res.body)
}
