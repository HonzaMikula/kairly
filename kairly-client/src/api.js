import request from 'superagent'

let token = localStorage.getItem("token")

function clearToken() {
  localStorage.removeItem("token")
  token = null;
}

function createToken(username, password) {
  return request
    .post(process.env.BACKEND_BASE + '/api/token')
    .send({username, password})
    .then(res => {
       token = res.body.token
       localStorage.setItem('token', token)
       return token;
    })
}

function getProfile() {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/profile')
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body.user)
}

function getTimeline(page) {
  if (!token) return Promise.reject();
  let url = process.env.BACKEND_BASE + '/api/timeline'
  if (page) {
    url += '?page=' + page
  }
  return request
    .get(url)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

function getEditions() {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/editions')
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

function getEditionDetail(editionId) {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/editions/' + editionId)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}

function getAuthorDetail(authorId) {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/author/' + authorId)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body)
}


function getPost(postId) {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/post/'  + postId)
    .set('Authorization', 'Bearer ' + token)
    .then(res => res.body.post)
}

function postSubscription(editionId, subscribe) {
  if (!token) return Promise.reject();
  return request
    .post(process.env.BACKEND_BASE + '/api/subscribe/' + editionId)
    .set('Authorization', 'Bearer ' + token)
    .send({subscribe})
    .then(res => res.body)
}

function postAuthorSubsription(author, subscribe) {
  if (!token) return Promise.reject();
  return request
    .post(process.env.BACKEND_BASE + author.followUrl)
    .set('Authorization', 'Bearer ' + token)
    .send({subscribe})
    .then(res => res.body)
}

export {
  clearToken, createToken, getProfile, getTimeline, getPost,
  getEditions, getEditionDetail, getAuthorDetail, postSubscription,
  postAuthorSubsription
}
