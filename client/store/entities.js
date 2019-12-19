
import isFunction from 'lodash/isFunction'

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
    issue: 'IssueRef'
  },
  'IssueRef': {
    newspaper: 'Newspaper',
  },

  'Issue': {
    author: 'Author',
    newspaper: 'Newspaper',
    posts: 'PostEditorial',
  },
  'PostEditorial': {
    post: 'Post',
    editorial: 'Editorial'
  },
  'Editorial': {
    author: 'Author',
    tweets: 'Post'
  },
  'NewspaperBacklog': {
    considered: 'PostEditorial',
    next: 'PostEditorial',
    upcoming: 'PostEditorial',
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
      return getters.getAuthor(obj)
    }
    if (type === 'Newspaper') {
      return getters.getNewspaper(obj)
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
