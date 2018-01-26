<template>
  <my-editions-view>
    <h1>My Subscription</h1>

    <div>
      <my-editions--item v-for="edition in myEditions" :key="edition.id">
        <picture>
          <img :src="edition.picture" alt="" />
        </picture>

        <h2>{{ edition.title }}</h2>

        <p>{{ edition.description }}</p>

        <my-editions--item--author>
          <img :src="edition.author.picture" :alt="edition.author.name"/>
          {{ edition.author.name }}
        </my-editions--item--author>

        <my-editions--item--subscribe>
          <button v-bind:class="{ 'is-subscribed': edition.isSubscribed }">{{ edition.isSubscribed ? 'Subscribed' : 'Subscribe'}}</button>
          <p>
            10 CZK per month
             • 
            {{ edition.subscribers }} subscribers
            •
            #{{ edition.issues }}  
          </p>
        </my-editions--item--subscribe>
          
      </my-editions--item>
    </div>
    
    
    


  </my-editions-view>
</template>

<script>
import myEditionsData from '@/data/myEditionsData.json'

export default {
  name: 'MyEditions',
  data: function () {
    return {
      myEditions
    }
  },
  created: function () { 
    this.myEditions = myEditionsData
  }
}
</script>
