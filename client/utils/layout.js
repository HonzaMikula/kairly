
export function flattenPosts (layout) {
  const posts = []
  layout.forEach(item => {
    if (item.type === 'box') {
      item.columns.forEach(col => {
        col.posts.forEach(p => posts.push(p))
      })
    } else if (item.type !== 'header') {
      posts.push(item)
    }
  })
  return posts
}
