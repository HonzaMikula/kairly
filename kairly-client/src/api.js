import request from 'superagent'
import Prefix from 'superagent-prefix'
import store from '@/store'

const prefix = Prefix(process.env.BACKEND_BASE)


function getToken(username, password) {
  return request
    .post('/api/token')
    .use(prefix)
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
    .get('/api/profile')
    .use(prefix)
    .set('Authorization', 'Bearer ' + store.token)
    .then(res => {
      store.user = res.body.user
      return store.user
    })
}

function getTimeline() {
  if (!store.token) return Promise.reject();
  return request
    .get('/api/timeline')
    .use(prefix)
    .set('Authorization', 'Bearer ' + store.token)
    .then(res => res.body)
}

export { getToken, getProfile, getTimeline }
