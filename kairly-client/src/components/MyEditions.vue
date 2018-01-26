<template>
  <my-editions-view>
    <h1>My Subscription</h1>

    <div>
      <my-editions--item v-for="edition in myEditions" :key="edition.id">
        <picture>
          <img src="http://img.ct24.cz/cache/900x700/article/73/7213/721203.jpg?1515941652" alt="" />
        </picture>

        <h2>{{ edition.title }}</h2>

        <p>{{ edition.description }}</p>

        <my-editions--item--author>
          <img :src="edition.editor.picture" :alt="edition.editor.name"/>
          {{ edition.editor.name }}
        </my-editions--item--author>

        <my-editions--item--subscribe>
          <button v-bind:class="{ 'is-subscribed': edition.isSubscribed }">{{ edition.isSubscribed ? 'Subscribed' : 'Subscribe'}}</button>
          <p>
            10 CZK per month
             •
            {{ edition.likes }} subscribers
            •
            #{{ edition.issues }}
          </p>
        </my-editions--item--subscribe>

      </my-editions--item>
    </div>

  </my-editions-view>
</template>

<script>
import * as api from '@/api'

export default {
  name: 'MyEditions',
  data: function () {
    return {
      myEditions: []
    }
  },
  created: function () {
    api.getSubscription().then(myEditions => {
      this.myEditions = myEditions
    })
  }
}
</script>
