<template>
  <div>
    <timeline-edition>
      <h1>{{issue.title}}</h1>

      <p>
        <timeline-edition--editor>
          <router-link :to="issue.author.url">
            <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
            {{issue.author.name}}
          </router-link>
        </timeline-edition--editor>
        •
        {{issue.edition.period}}
        •
        {{issue.time | moment('calendar')}}
      </p>
    </timeline-edition>

    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'issue-edition',
  props: ['issue']
}
</script>
