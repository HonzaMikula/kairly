<template>
  <header class="app-header-public">
    <div>
      <h1>Kairly</h1>

      <p>We aim for good journalism</p>

      <nav>
        <ul>
          <li><a href="/">Join us</a></li>
          <li><a href="/">Sign In</a></li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>

export default {
  name: 'AppHeaderPublic'
}
</script>

<style lang="sass">
//- HEADER -//
.app-header-public
  display: block
  height: $baseline * 2
  padding: 0 $baseline

  background: #fff
  border-bottom: 1px solid #eee
  color: #555

  line-height: $baseline * 2

  @media (max-width: $mobile)
    padding: 0 $baseline/4 0 0

  //- wrapper
  > div
    position: relative

    margin: 0 auto
    max-width: 900px

  //- logo
  h1
    font-family: $ff-serif
    font-weight: 600
    font-size: $fs-3
    text-align: center

  p
    position: absolute
    left: 0
    top: 0

    font-family: $ff-serif
    font-size: $fs-0


  //- join us / sign in
  nav
    position: absolute
    right: 0
    top: 0

    li
      display: inline-block
      margin-left: $baseline

    a
      color: $c-base


</style>
