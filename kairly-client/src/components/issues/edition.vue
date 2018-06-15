<template>
  <timeline-edition>
    <header>
      <h1>
        <router-link :to="`/editions/${issue.edition.id}`">{{issue.title}}</router-link>
        <!-- title link shoul point to whole edition TODO return permalink -->
        <!--router-link :to="`/editions/${issue.edition.id}/${issue.id}`">{{ issue.id }}</router-link-->
      </h1>

      <p>
        <timeline-edition--editor>
          <router-link :to="issue.author.url">
            <img v-if="issue.author.picture" :src="issue.author.picture" :alt="issue.author.name" />
            {{issue.author.name}}
          </router-link>
        </timeline-edition--editor>
        •
        {{ issue.edition.periodicity.frequency }}
        •
        {{ issue.time | moment('calendar')}}
      </p>
    </header>
    <slot></slot>
  </timeline-edition>
</template>

<script>
export default {
  name: 'issue-edition',
  props: ['issue']
}
</script>
