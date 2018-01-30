<template>
  <timeline-welcome>
    <h1>Welcome to Kairly</h1>
    <p>Start with selecting editions you want to subscribe.</p>

    <timeline-welcome--my-editions>
      <my-editions--item v-for="edition in [1,2,3]" :key="edition.id">
        <picture>
          <img src="http://kairly.com/media/editions/volby_omSw6dr.jpg" alt="" />
        </picture>

        <h2>Prezidentské volby</h2>

        <p>Nejdůležitější informace z probíhajících prezidentských voleb.</p>

        <my-editions--item--author>
          <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY_400x400.jpeg" alt=""/>
          Jan Mikula
        </my-editions--item--author>

        <my-editions--item--subscribe>
          <button>Subscribe</button>
          <p>
            10 CZK per month
            •
            {{ 123 }} subscribers
            •
            #{{ 12 }}
          </p>
        </my-editions--item--subscribe>

      </my-editions--item>
    </timeline-welcome--my-editions>

    <timeline-welcome--more-editions>
      <router-link to='/my-editions'>View more editions</router-link>
      <br />
      <button>Show me editions</button>
    </timeline-welcome--more-editions>
  </timeline-welcome>
</template>

<script>
import * as api from '@/api'

import Welcome from '@/components/Welcome'

export default {
  name: 'Welcome',

  data: function () {
    return {}
  },

  methods: {
  },

  created: function () {
    api.getEditions().then(myEditions => {
      this.myEditions = myEditions
    })
  }
}
</script>
