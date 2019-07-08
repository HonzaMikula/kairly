<template>
  <div class="editorial-post--editorial article">
    <article role="article" class="post newspaper editorial">
      <header>
        <picture>
          <a href="/janmikula" class="">
            <img src="https://cdn.kairly.com/media/users/janmikula.jpg" alt="Dojnice">
          </a>
        </picture>
        <h3>
          <a href="/janmikula" class="">Jan Mikula, editor</a>
        </h3>
      </header>
      <timeline-post--article>
        <h2>Nebezpečný Babiš</h2>
        <timeline-post--article--content>
          <img src="http://cdn.xsd.cz/resize/e884c16700743e3cb6718cbd0f7c113e_extract=91,0,1959,1102_resize=640,360_.jpg?hash=c688b6b5977eaee434011a70e0afe8a3"/>
          <p>Všichni tady lamentujeme nad Babišem a jeho nejrůznějšími nekalými dotačními praktiky. Co se takhle spojit?</p>

          <p>Ne, proti Babišovi. Ale proti dotacím, ať už na evropské či národní úrovni. Zrušme je.</p>
          
        </timeline-post--article--content>
      </timeline-post--article>
    </article>
  </div>
</template>



<script>

export default {
  name: 'EditorialTweets',

}
</script>
<style lang="sass">
.editorial-post .editorial-post--editorial.article
  align-self: start

.editorial-post--editorial .post.newspaper.editorial
  timeline-post--article--content
    column-count: 1

</style>
