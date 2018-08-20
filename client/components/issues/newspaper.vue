<template>
  <timeline-newspaper>
    <header>
      <h1>
        <router-link :to="{name: 'newspaper', params: {author: newspaper.editor.id, newspaper: newspaper.name}}">{{ issue.newspaper.title }}</router-link>&nbsp;<router-link :to="{name: 'issue', params: {author: newspaper.editor.id, newspaper: newspaper.name, issue: issue.number}}">#{{ issue.number }}</router-link>
      </h1>

      <p>
        <timeline-newspaper--editor>
          <router-link :to="{name: 'author', params: {author: newspaper.editor.id}}">
            <img v-if="issue.newspaper.editor.picture" :src="newspaper.editor.picture" :alt="newspaper.editor.name" />
            {{ newspaper.editor.name }}
          </router-link>
        </timeline-newspaper--editor>
        •
        {{ newspaper.periodicity.frequency }}
        •
        {{ issue.time | moment('calendar')}}
      </p>
    </header>
    <slot></slot>
  </timeline-newspaper>
</template>

<script>
export default {
  name: 'issue-newspaper',
  props: ['issue'],

  computed: {
    newspaper() {
      return this.issue.newspaper
    }
  }
}
</script>
