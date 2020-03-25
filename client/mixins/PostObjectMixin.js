import isString from 'lodash/isString'
import keyBy from 'lodash/keyBy'

export default {
  computed: {
    postsById() {
      return keyBy(this.issue.posts, 'id')
    },
  },
  methods: {
    getPostObject(item, idx) {
      if (Array.isArray(item)) {
        const id = Math.random().toString(36).substring(2)
        const css = isString(item[0]) ? item[0] : null
        const columns = css === null ? item : item.slice(1)
        return {
          id,
          type: 'box',
          css,
          columns: columns.map(c => {
            return  {
              css: isString(c[0]) ? c[0] : '',
              posts: (isString(c[0]) ? c.slice(1) : c).map(item => this.postsById[item.post])
            }
          })
        }
      }
      if (item.post) {
        return this.postsById[item.post]
      }
      if (item.header !== undefined) { // header can be null!
        return { type: 'header', id: Math.random().toString(36).substring(2), title: item.header }
      }
      console.log(item)
      throw new Error("Unknown type")
    }
  }
}