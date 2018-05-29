<template>
  <post--issue role="article">
    <div>
      <h2><a :href="'/editions/' + post.edition.id">{{ post.title }}</a></h2>
      <picture>
        <a :href="'/editions/' + post.edition.id">
          <img :src="post.edition.picture"/>
        </a>
      </picture>
      <p>{{ post.edition.description }}</p>
    </div>
  </post--issue>
</template>

<script>

export default {
  name: 'PostIssue',
  props: ["post"]
}
</script>

<style lang="sass">
//- POST ISSUE -//
post--issue
  display: block
  padding: $baseline / 2
  width: 576px

  background: #fff


  //- content
  > div
    display: grid
    grid-template-areas: "post-issue-picture post-issue-title" "post-issue-picture post-issue-description"
    grid-template-columns: $baseline*5 auto
    grid-gap: 0 $baseline/2

    font-family: $ff-serif

    //- issue title
    h2
      grid-area: post-issue-title

      font-size: $fs-1
      font-weight: 600

      a
        color: #000

        text-decoration: none

    //- issue picture
    picture
      grid-area: post-issue-picture

    img
      height: $baseline * 3
      width: $baseline * 5

      object-fit: cover

    //- description
    p
      grid-area: post-issue-description
</style>
