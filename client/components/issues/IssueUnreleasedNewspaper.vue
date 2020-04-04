<template>
  <div class="timeline-newspaper issue-unreleased">
    <header>
      <h1>
        <nuxt-link
          :id="`issue-newspaper-${$_uid}`"
          :to="`/${newspaper.editor.id}/${newspaper.name}`"
        >
          <slot name="newspaper-title">{{ issue.newspaper.title }}</slot>
        </nuxt-link>
      </h1>

      <NewspaperPopup
        :target="`issue-newspaper-${$_uid}`"
        :newspaper="newspaper"
      />

      <p>
        <span class="timeline-newspaper--editor">
          <nuxt-link
            :id="`issue-newspaper-author-${$_uid}`"
            :to="{name: 'author', params: {author: newspaper.editor.id}}"
          >
            <AuthorPicture :author="newspaper.editor" />
            {{ newspaper.editor.name }}
          </nuxt-link>
        </span>
        <span>• {{ frequencyLabel }}</span>
        <template v-if="!hideDate"> • {{ issue.time | moment('calendar') }}</template>
      </p>

      <AuthorPopup
        :target="`issue-newspaper-author-${$_uid}`"
        :author="newspaper.editor"
      />
    </header>

    <article>
      {{ $t('We are very sorry, but {editor} didn\'t prepare a new release for you.', {editor: newspaper.editor.name}) }}
    </article>
  </div>
</template>

<script>
import AuthorPicture from '@/components/widgets/AuthorPicture'
import AuthorPopup from '@/components/widgets/AuthorPopup'
import NewspaperPopup from '@/components/widgets/NewspaperPopup'

export default {
  name: 'IssueUnreleasedNewspaper',

  components: {
    AuthorPicture,
    AuthorPopup,
    NewspaperPopup,
  },

  props: {
    issue: { type: Object, required: true },
    hideDate: { type: Object, required: true }
  },

  computed: {
    newspaper () {
      return this.issue.newspaper
    },

    frequencyLabel () {
      const { frequency } = this.newspaper.periodicity
      if (frequency === '6x_per_day') { return this.$t('6× per day') }
      if (frequency === '3x_per_day') { return this.$t('3× per day') }
      if (frequency === 'weekly') { return this.$t('Weekly') }
      if (frequency === 'daily') { return this.$t('Daily') }
      return ''
    }
  }

}
</script>

<style lang="sass">
.issue-unreleased article
  font-family: $ff-serif
  font-size: $fs-1
  text-align: center
</style>
