
import isFunction from 'lodash/isFunction'
import isString from 'lodash/isString'

import Vue from 'vue'

function getNextRelease({ frequency, time, dow }) {
  const now = Vue.moment()
  const m = Vue.moment()
  if (frequency === '3x_per_day' || frequency === '6x_per_day') {
    if (now.hour() < 6) {
      m.hour(6)
    } else if (now.hour() < 9 && frequency === '6x_per_day') {
      m.hour(9)
    } else if (now.hour() < 12) {
      m.hour(12)
    } else if (now.hour() < 15 && frequency === '6x_per_day') {
      m.hour(15)
    } else if (now.hour() < 18) {
      m.hour(18)
    } else if (now.hour() < 21 && frequency === '6x_per_day') {
      m.hour(21)
    } else {
      m.add(1, 'd').hour(6)
    }
  } else if (frequency === 'daily') {
    const h = parseInt(time)
    if (now.hour() < h) {
      m.hour(h)
    } else {
      m.add(1, 'd').hour(h)
    }
  } else if (frequency === 'weekly') {
    const h = parseInt(time)
    m.isoWeekday(dow).hour(h).startOf('hour') // startOi is needed to get correct isBefore comparison
    if (m.isBefore(now)) {
      m.add(7, 'd')
    }
  }
  return m.startOf('hour').format()
}

export const state = () => {
  return {
    newspapers: {},
    authors: {},
  }
}

export const mutations = {
  resetState(state) {
    state.newspapers = {}
    state.authors = {}
  },

  newspaper(state, { newspaper }) {
    newspaper.nextRelease = getNextRelease(newspaper.periodicity)
    state.newspapers[newspaper.fullName] = newspaper
  },

  author(state, { author }) {
    state.authors[author.id] = author
  },
}

const schemas = {
  'Post': (post) => {
    if (post.type === 'recommendation-issue') {
      return {
        author: 'Author',
        ref: 'Issue',
      }
    }
    if (post.type === 'recommendation-post') {
      return {
        author: 'Author',
        ref: 'Post',
      }
    }
    return {
      author: 'Author'
    }
  },
  'EditorialRef': {
    author: 'Author',
    tweets: 'Post',
    issue: 'IssueRef',
  },
  'IssueRef': {
    newspaper: 'Newspaper',
  },

  'Issue': {
    author: 'Author',
    newspaper: 'Newspaper',
    posts: 'Post',
  },
  'PostEditorial': {
    post: 'Post',
    editorial: 'Editorial'
  },
  'Editorial': {
    author: 'Author',
    tweets: 'Post'
  },
  'Transaction': {
    source: 'TransactionParty',
    target: 'TransactionParty'
  },
  'TransactionParty': {
    newspaper: 'Newspaper',
    author: 'Author',
    user: 'Author'
  }
}

export const getters = {
  getAuthor: state => id => id ? state.authors[id] : null,
  getNewspaper: (state, getters) => id => {
    if (!id) {
      return null
    }

    let newspaper = state.newspapers[id]
    if (!newspaper) {
      return null
    }

    newspaper = {
      ...newspaper, // make a copy
      editor: getters.getAuthor(newspaper.editor),
    }
    if (newspaper.coEditors) {
      newspaper.coEditors = newspaper.coEditors.map(getters.getAuthor)
    }
    return newspaper
  },

  denormalize: (state, getters) => (obj, type) => {
    if (!obj) {
      // null, undefined
      return obj
    }
    if (Array.isArray(obj)) {
      return obj.map(item => getters.denormalize(item, type))
    }

    if (type === 'Author') {
      // if author is inlined, then return it directly
      return isString(obj) ? getters.getAuthor(obj) : obj
    }
    if (type === 'Newspaper') {
      // if newspapper is inlined, then return it directly
      return isString(obj) ? getters.getNewspaper(obj) : obj
    }

    if (!schemas[type]) {
      return obj
    }

    let schema = schemas[type]
    if (isFunction(schema)) {
      schema = schema(obj)
    }

    obj = {...obj}
    Object.entries(schema).forEach(([prop, t]) => {
      if (obj[prop] !== undefined) {
        obj[prop] = getters.denormalize(obj[prop], t)
      }
    })
    return obj
  },
}
