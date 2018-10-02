<template>
  <timeline-welcome>
    <div class="welcome-view">
      <h1>Welcome to Kairly!</h1>

      <h2>How it works?</h2>

      <div class="welcome--roles">
        <div>
          <section>
            <h3>Authors</h3>
            <p>
              Authors focus on writing.
              They are creating high quality articles &amp; tweets.
            </p>
          </section>

          <section>
            <h3>Editors</h3>
            <p>
              Editors run their newspaper.
              They are selecting the best articles &amp; tweets from authors.
            </p>
          </section>

          <section>
            <h3>Readers</h3>
            <p>
              Readers choose what they want to read and when.
              They subscribe either directly to authors or to newspapers.
            </p>
          </section>
        </div>
      </div>

      <h2>How to start?</h2>

      <div class="welcome--tutorial">
        <ol>
          <li>Go to <nuxt-link to="/explore">Explore</nuxt-link></li>
          <li>Subscribe newspapers</li>
          <li>Or authors directly and choose when you want to read them</li>
          <li>Go on your <nuxt-link to="/"><span class="icon"></span></nuxt-link> <nuxt-link to="/">Timeline</nuxt-link></li>
        </ol>

        <div class="welcome--tutorial--illustration">
          <div>
            <div class="picture"></div>
            <div class="title"></div>
            <p>Daily at 9:00</p>
            <div class="description"></div>
            <div class="subscribe">Subscribe</div>
          </div>
          <figcaption>Illustration of newspaper widget</figcaption>
        </div>
      </div>

      <nuxt-link to="/explore">Start exploring authors &amp; newspapers</nuxt-link>
    </div>
  </timeline-welcome>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Welcome',
}
</script>

<style lang="sass">
//- Welcome Newspaper
timeline-welcome
  > a
    +subscribed-button

    display: table
    margin: 0 auto

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5


//- Welcome box
.welcome-view
  display: block
  margin-bottom: $baseline * 2

  > h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center

  > h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-2
    font-weight: 600
    text-align: center

  > a
    +subscribed-button

    display: table
    margin: 0 auto

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

//- Roles
.welcome--roles
  max-width: 900px
  margin: 0 auto $baseline auto
  padding: $baseline

  background: #fff

  font-family: $ff-serif

  > div
    display: flex

  section
    position: relative

    flex: 1
    margin-right: $baseline*2

    &::after
      +fa-icon()

      position: absolute
      right: -$baseline * 1.25
      top: $baseline * 2

      content: $fa-var-arrow-right

    &:last-of-type
      margin-right: 0

      &::after
        display: none

  h3
    margin-bottom: $baseline / 2
    font-size: $fs-1
    font-weight: 600

//- How to start
.welcome--tutorial
  display: flex
  align-items: center

  padding: $baseline
  margin-bottom: $baseline

  background: #fff

  font-family: $ff-serif

  counter-reset: step

  ol
    flex: 1

  ol li
    margin-bottom: $baseline / 2

    &::before
      display: inline-block
      border-radius: 100%
      height: $baseline * 1.5
      margin-right: $baseline / 2
      width: $baseline * 1.5

      background: #eee

      line-height: $baseline * 1.5
      text-align: center

      counter-increment: step
      content: counter(step)

    a
      color: #000

      text-decoration: underline

    .icon
      display: inline-block
      border-radius: 100%
      margin-left: $baseline / 4
      height: $baseline * 1.25
      width: $baseline*1.25

      background: #f5f5f5

      line-height: $baseline * 1.25
      text-align: center
      vertical-align: middle

      &::before
        +fa-icon()

        font-size: 21px

        content: $fa-var-home


//- Illustration on newspaper widget
.welcome--tutorial--illustration
  text-align: center

  figcaption
    padding: $baseline/4 0

    color: #999

    font-family: $ff-sans
    font-size: $fs--1
    line-height: $baseline


  //- frame
  > div
    border-radius: 5px
    padding: $baseline / 4
    width: 200px

    background: #fff
    border: 1px solid #eee

  //- picture
  .picture
    height: $baseline * 3
    margin-bottom: $baseline / 2

    background: #eee

  //- title
  .title
    height: $baseline / 2
    margin-bottom: $baseline / 4
    width: 75%

    background: #eee

  p
    margin-bottom: $baseline / 2

    color: #999

    font-family: $ff-sans
    font-size: $fs--1
    font-weight: 600
    line-height: $baseline * 0.8
    text-align: left

  //- description
  .description
    &::after,
    &::before
      display: block
      height: $baseline / 4
      margin-bottom: $baseline / 4

      border-bottom: $baseline / 4 solid #eee
      border-top: $baseline / 4 solid #eee

      content: ''

  //- subscribe
  .subscribe
    display: inline-block
    border-radius: $baseline
    margin: 0 auto
    padding: 0 $baseline/2

    border: 1px solid #eee
    color: #999

    font-family: $ff-sans
    font-size: $fs--1

</style>
