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

function getTimeline() {
  if (!token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/timeline')
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

export { clearToken, createToken, getProfile, getTimeline, getPost }
