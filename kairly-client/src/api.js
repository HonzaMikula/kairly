import request from 'superagent'
import store from '@/store'


function getToken(username, password) {
  return request
    .post(process.env.BACKEND_BASE + '/api/token')
    .send({username, password})
    .then(res => {
       store.token = res.body.token
       localStorage.setItem('token', store.token)
       return store.token
    })
}

function getProfile() {
  if (!store.token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/profile')
    .set('Authorization', 'Bearer ' + store.token)
    .then(res => {
      store.user = res.body.user
      return store.user
    })
}

function getTimeline() {
  if (!store.token) return Promise.reject();
  return request
    .get(process.env.BACKEND_BASE + '/api/timeline')
    .set('Authorization', 'Bearer ' + store.token)
    .then(res => res.body)
}

export { getToken, getProfile, getTimeline }
