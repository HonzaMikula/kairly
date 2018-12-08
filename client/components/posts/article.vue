<template>
  <post :post="post">
    <timeline-post--article>
      <h2>
        <span v-if="post.draft">{{ post.content.title }}</span>
        <nuxt-link v-else :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }}">{{ post.content.title }}</nuxt-link>
      </h2>

      <timeline-post--article--content>
        <div v-html="post.content.perex"></div>
        <timeline-post--continue-reading v-if="post.timeRead && !post.draft">
          <template v-if="post.content.protected">
            <a :href="post.source" target="_blank">{{ $t('Read the article') }}</a>
            ({{ post.timeRead }} {{ $t('read') }})
          </template>
          <template v-else>
            <div v-if="isSubscribed">
              <nuxt-link :to="{ name: 'author-post', params: { author: post.author.id, post: post.slug }, hash: '#continue'}">
                {{ $t('Continue reading') }}
              </nuxt-link>
            </div>
            <div v-else>
              {{ $t('Subscribe newspaper to continue reading') }}
            </div>
            ({{ post.timeRead }} {{ $t('read') }})
          </template>
        </timeline-post--continue-reading>
      </timeline-post--article--content>
    </timeline-post--article>

    <template slot="extendedControls">
      <slot v-if="post.source" name="extendedControls">
        <a
          :href="post.source"
          class="external-link"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}"
          :title="$t('Original article')">
        </a>
      </slot>
    </template>

    <template slot="controls"><slot name="controls"></slot></template>
  </post>
</template>

<script>
import post from './post';

export default {
  name: 'post-article',
  props: ["post", "isSubscribed"],
  components: { post }
}
</script>


<style lang="sass">
timeline-post--article
  font-family: $ff-serif

  //- Title
  > h2
    display: block
    margin-bottom: $baseline / 2

    font-size: $fs-1
    font-weight: 600
    line-height: 1.58

    @media (max-width: $mobile)
      font-size: $fs-0

    a
      color: #000

  a
    color: $c-base

//- Content
timeline-post--article--content
  position: relative

  column-count: 3
  column-rule: 1px dotted #ddd
  column-gap: $baseline
  display: block

  line-height: 1.58
  hyphens: auto

  @media (max-width: $mobile)
    column-count: 2
    column-gap: $baseline / 2

    font-size: $fs--1
    line-height: 1.58


  +article-perex


//- Continue Reading
timeline-post--continue-reading
  display: block

  color: #999

  font-family: $ff-sans
  font-size: $fs--1
  text-align: center

  a[href]
    display: table
    border-radius: 15px
    clear: both
    margin: $baseline / 2 auto 0 auto
    padding: 0 $baseline / 2

    border: 1px solid transparent
    color: $c-base

    font-size: $fs--1
    line-height: 1.58
    text-transform: uppercase
    text-decoration: none

    &:focus,
    &:hover
      background: $c-base
      color: #fff

</style>
