<template>
  <div class="empty-post-placeholder-view">
    <h2><slot /></h2>

    <div class="empty-post-placeholder--instructions">
      <section>
        <h3>{{ $t('Write a post') }}</h3>
        <ul>
          <li>
            {{ $t('Start writing draft of your') }}
            <nuxt-link to="/posts/create/article">{{ $t('article') }}</nuxt-link> {{ $t('or') }}
            <nuxt-link to="/posts/create/tweet">{{ $t('tweet') }}</nuxt-link>.
          </li>
          <li>{{ $t('Set a price and publish the post.') }}</li>
          <li>{{ $t('Share it on social media.') }}</li>
        </ul>
      </section>

      <section>
        <h3>{{ $t('Publish it in newsletters') }}</h3>
        <ul>
          <li>
            {{ $t('Start publishing your own') }}
            <nuxt-link to="/newspapers">{{ $t('newsletter') }}</nuxt-link>.
          </li>
          <li>{{ $t('Let other newsletter editors know about your post.') }}</li>
          <li>{{ $t('Get fair share from newsletters\' subscription revenues where your post appears.') }}</li>
        </ul>
      </section>
    </div>

    <div class="empty-post-placeholder--buttons">
      <nuxt-link to="/posts/create/article">{{ $t('Write an article') }}</nuxt-link>
      <nuxt-link to="/posts/create/tweet">{{ $t('Write a tweet') }}</nuxt-link>
    </div>
  </div>
</template>

<script>

export default {
  name: 'EmptyPostPlaceholder'
}
</script>

<style lang="sass">
@import './styles/components/buttons'

//- Empty placeholder
.empty-post-placeholder-view
  display: block
  margin: $baseline 0
  padding: $baseline

  background: #fff
  border: 1px solid #eee
  box-shadow: 2px 2px 4px #eee, -2px -2px 4px #fff

  text-align: center

  h2
    margin-bottom: $baseline * 1.5

    font-size: $fs-3
    font-weight: 600
    line-height: 1.42

  p
    margin-bottom: $baseline

.empty-post-placeholder--instructions
  display: grid
  grid-auto-columns: 1fr
  grid-auto-flow: column
  grid-column-gap: $baseline
  margin-bottom: $baseline

  text-align: left

  @media (max-width: $mobile)
    grid-auto-flow: row
    grid-row-gap: $baseline

  h3
    margin-bottom: $baseline / 2
    font-size: $fs-1
    font-weight: 600

    @media (max-width: $mobile)
      margin-bottom: 0

  h3 + p
    margin-bottom: auto

  ul,
  ol
    margin-top: $baseline

    @media (max-width: $mobile)
      margin-top: $baseline / 2

    li
      list-style: disc outside
      margin-bottom: $baseline / 4
      margin-left: $baseline * 0.75

      line-height: 1.42

      a
        color: darken($c-base, 10%)

        font-weight: 600

        &:hover,
        &:focus
          color: darken($c-base, 20%)

  ol li
    list-style: decimal outside

.empty-post-placeholder--buttons
  display: flex
  justify-content: center

  a
    +button(primary, medium)

    margin: 0 $baseline

    @media (max-width: $mobile)
      margin: 0 $baseline/4

      +button(primary, small)
</style>
