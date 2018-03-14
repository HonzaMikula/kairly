<template>
  <edition-detail-view>

    <div>
      <edition-detail--header>
        <h1>{{ edition.title }}</h1>
      </edition-detail--header>

      <edition-detail--description>
        <p>
          {{ edition.description }}
        </p>

        <div>
          <div>
            <h3>Periodicity</h3>
            <p>{{ issue.period }}</p>
          </div>

          <div>
            <h3>Issues</h3>
            <p>{{ edition.issues }}</p>
          </div>

          <div>
            <h3>Subscribers</h3>
            <p>{{ edition.likes }}</p>
          </div>
        </div>
      </edition-detail--description>

      <edition-detail--subscribe>
        <button
          v-bind:class="{ 'is-subscribed': edition.isSubscribed }"
          v-on:click="subscribe($event)"
        >{{ edition.isSubscribed ? 'Subscribed' : 'Subscribe Edition'}}</button>

        <p>10 CZK per month</p>
      </edition-detail--subscribe>

      <edition-detail--picture>
        <img :src="edition.picture" :alt="edition.title"/>
      </edition-detail--picture>
    </div>


    <edition-detail--last-edition v-if="issue">
      <h2><span>Check the Last Issue</span></h2>

      <Issue :issue="issue" :isSubscribed="edition.isSubscribed" />
    </edition-detail--last-edition>
  </edition-detail-view>
</template>


<script>
import * as api from '@/api'

import Issue from '@/components/Issue'


export default {
  name: 'EditionDetail',

  components: {
    Issue
  },

  data: function () {
    return {
      'loading': true,
      'edition': null,
      'issue': null,
    }
  },

  methods: {
    subscribe(ev) {
      this.$store.dispatch('subscribe', {
        edition: this.edition,
        value: !this.edition.isSubscribed
      })
      this.edition.isSubscribed = !this.edition.isSubscribed
      ev.target.blur()
    }
  },

  created() {
    api.getEditionDetail(this.$route.params.editionId).then(resp => {
      this.edition = resp.edition
      this.issue = resp.issue
      this.loading = false
    })
  }
}
</script>
