
export function flattenPosts (layout, includeHeader = false) {
  const posts = []
  layout.forEach(item => {
    if (item.type === 'box') {
      item.columns.forEach(col => {
        col.posts.forEach(p => posts.push(p))
      })
    } else if (item.type !== 'header') {
      posts.push(item)
    } else if (includeHeader && item.title) {
      posts.push(item)
    }
  })
  return posts
}
