<template>
  <img
    :itemprop="itemprop"
    :src="author.pictures ? author.pictures[size] : require('~/assets/user.png')"
    :alt="author.name"
  />
</template>

<script>
export default {
  name: 'AuthorPicture',

  props: {
    author: { tupe: Object, required: true },
    size: { type: String, default: () => 'small' },
    itemprop: String
  }
}
</script>