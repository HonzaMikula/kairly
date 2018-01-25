<template>
  <my-editions-view>
    <h1>My Subscription</h1>

    <div>
      <my-editions--item v-for="edition in myEditions" :key="edition.id">
        <picture>
          <img :src="edition.picture" alt="" />
        </picture>

        <div>
          <h2>{{ edition.title }}</h2>

          <p>{{ edition.description }}</p>

          <my-editions--item--subscribe>
            <button>Subscribe</button>
            <p>10 CZK per month</p>
          </my-editions--item--subscribe>
          
        </div>
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
