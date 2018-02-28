<template>
  <author-detail-view>
    <author-detail--header>
      <picture>
        <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY_400x400.jpeg" alt="Jan Mikula"/>
      </picture>
      <h1>Jan Mikula</h1>
      <p>Mé názory nevyjadřují názory Kairly ani CzechTV.</p>
    </author-detail--header>

    <author-detail--subscribe>
      <button>Subscribe Editions</button>

      <button>Subscribe Posts</button>
    </author-detail--subscribe>

    <author-detail--editions>
      <h2>Jan Mikula's Editions</h2>
     
      <img src="../assets/kairly-temp-editions.png" />

    </author-detail--editions>

    <author-detail--posts>
      <h2>Jan Mikula's Posts</h2>

      <img src="../assets/kairly-temp-posts.png" />
    </author-detail--posts>

  </author-detail-view>
</template>


<script>
export default {
  name: 'AuthorDetail'
}
</script>