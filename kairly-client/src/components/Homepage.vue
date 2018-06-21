<template>
  <homepage-view>
    <homepage--cover>
      <h1>Kairly</h1>

      <p>We stand for exceptional journalism<br /> &amp; great reading experience.</p>
    </homepage--cover>

    <homepage--login>
      <form v-on:submit.prevent="login">
        <div>
          <input name="username" placeholder="Username" v-model="username" />
        </div>

        <div>
          <input name="password" type="password" placeholder="Password" v-model="password" />
        </div>

        <button type="submit">Sign In</button>

        <homepage--login--error-message v-if="invalidCredentials">
          Wrong login or password
        </homepage--login--error-message>
      </form>
    </homepage--login>

    <homepage--values>
      <h2>What we believe in?</h2>

      <p>
        In the world full of fake news, manipulations and attacks on journalism, we stand for <strong>truth</strong>.
      </p>

      <p>In the world full of censorship and propaganda, we stand for <strong>free speach</strong>.</p>

      <p>
        In the world full of distraction and lack of focus, we stand for
        <strong>control of your time and undistracted reading experience</strong>.
      </p>

      <p>
        In the world where journalist are dependent on advertisment or big corporations with their interests,
        we stand for <strong>fair reward for high-quality content</strong>.
      </p>

      <p>Stand with us!</p>
    </homepage--values>

    <homepage--how-it-works>
      <h2>How it works?</h2>
      <p>
        In old times we bought newspapers every day. Each issue of newspaper was prepared by professional editors who selected the
        best articles from proffesional authors. By buying a newspaper, you pay those editors and authors.
      </p>

      <p>
        In modern world of social media we lost professional editors and authors are dependent on advertisment.
        Now it's your friends who are selecting the content in your timeline. The result is not good.
        Exceptional journalism depends on professional editors and authors, who will get paid fairly.
      </p>

      <div>
        <img src="../assets/homepage/kairly-screenshot.png" alt="Kairly Screenshot"/>
        <img src="../assets/homepage/kairly-screenshot2.png" alt="Kairly Screenshot"/>
      </div>

      <p>
        In Kairly readers are subsribing editions and paying for them.
        Those money are then shared between editors and authors.
      </p>
    </homepage--how-it-works>

    <homepage--help-us>
      <h2>How you can help?</h2>
      <p>You can help us create exceptional journalism in different ways.</p>

      <div>
        <section>
          <h3>Readers</h3>
          <p>
            Do you like the project and you want to help us improve the experience for readers?
            Participate in our user tests and private beta program.
          </p>
        </section>

        <section>
          <h3>Editors</h3>
          <p>
            Do you want to change how current journalism and its business models work?
            Start creating editions in our private beta program.
          </p>
        </section>

        <section>
          <h3>Authors</h3>
          <p>
            Do you want to help improve our payments mechanism for authors?
            Start publishing your blogs and tweets in our private beta program.
          </p>
        </section>

        <section>
          <h3>Investors</h3>
          <p>
            Do you want to help us create enviroonment for exceptional journalism?
            Become one of our investors.
          </p>
        </section>
      </div>

      <homepage--help-us--contact-us>
        <a href="mailto:jan.mikula@hotmail.com">Contact Us</a>
      </homepage--help-us--contact-us>
    </homepage--help-us>

  </homepage-view>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

import * as api from '@/api'

export default {
  name: 'Homepage',

  data() {
    return {
      invalidCredentials: false,
      username: null,
      password: null
    }
  },

  methods: {
    login() {
      this.invalidCredentials = false
      const { username, password } = this
      api.createToken(username, password)
      .then(this.getProfile)
      .catch(err => this.invalidCredentials = true)
    },

    ...mapActions(['getProfile']),
  }
}
</script>

<style lang="sass">
//- Cover
homepage--cover
  display: block
  box-sizing: border-box
  height: 580px
  padding: $baseline*2 $baseline*2 $baseline*2 $baseline*2

  background: url(../assets/homepage/hero.png) center center no-repeat
  background-size: cover

  color: #fff

  font-family: $ff-serif

  //- kairly Heading
  h1
    margin-bottom: $baseline
    
    font-size: 60rem
    line-height: $baseline * 3

  //- motto
  p  
    font-size: $fs-3
    line-height: $baseline * 1.25
    

//- Login Form
homepage--login 
  position: absolute
  right: $baseline / 2
  top: $baseline / 2

  border-radius: 5px
  display: block
  padding: $baseline / 2

  background: rgba(#555, 0.7)

  //- wrapper
  form
    position: relative

    display: table
    margin: auto

  div
    display: inline-block  
    margin-right: $baseline / 2

  //- input
  input
    border-radius: 3px
    box-sizing: border-box
    height: $baseline * 1.25
    padding: 0 $baseline / 4

    border: 0
    background: rgba(#fff, 0.7)

    font-weight: 600

    transition: all 0.15s

    &:focus,
    &:hover
      background: #fff

  //- button
  button
    border-radius: 3px
    box-sizing: border-box
    height: $baseline * 1.25
    padding: 0 $baseline / 2

    background: $c-base
    border: 0
    color: #fff

    cursor: pointer
    font-weight: 600

    &:hover,
    &:focus
      background: darken($c-base, 10%)

//-- Error message  
@keyframes homepage-login-error-message
  from 
    opacity: 0


homepage--login--error-message
  position: absolute
  left: 0
  bottom: -$baseline * 3

  border-radius: 3px
  box-sizing: border-box
  padding: $baseline / 2
  width: 100%
  opacity: 0

  background: rgba($c-red, 0.8)
  border: 1px solid darken($c-red, 10%)
  color: #fff

  text-align: center

  animation: homepage-login-error-message .15s

  //- when added to DOM
  &:not(:empty)    
    opacity: 1

    
//- Values
homepage--values
  display: block
  padding: $baseline * 2 $baseline 

  text-align: center

  //- heading
  h2
    margin-bottom: $baseline * 2
    font-size: $fs-3
    font-family: $ff-serif

  //- values
  p 
    margin: 0 auto $baseline auto
    max-width: 700px

    font-size: $fs-1
    font-family: $ff-serif

    strong
      font-weight: 600

    &:last-of-type
      margin-top: $baseline * 2
      font-size: $fs-3  


homepage--how-it-works
  display: block
  padding: $baseline * 2 $baseline 

  background: lighten($c-base, 20%)

  font-family: $ff-serif
  text-align: center

  //- heading
  h2
    margin-bottom: $baseline * 2
    font-size: $fs-3
    font-family: $ff-serif

  p
    max-width: 700px
    margin: 0 auto $baseline auto

    font-size: $fs-1  

  > div
    display: table
    margin: 0 auto $baseline auto

  img
    display: block
    float: left
    margin-right: $baseline
    
    max-width: 300px  



//- Help Us
homepage--help-us
  display: block
  padding: $baseline
  
  background: lighten($c-base, 40%)

  font-family: $ff-serif

  //- Heading
  h2
    margin-bottom: $baseline

    font-size: $fs-3
    font-family: $ff-serif
    text-align: center

  > p
    text-align: center


  //- wrapper
  > div
    display: flex
    max-width: 1200px
    margin: $baseline*2 auto

  //- section
  section
    flex: 1
    margin-right: $baseline * 2

    @media (max-width: $mobile)
      flex: 1 50%
      flex-wrap: wrap

    &:last-of-type
      margin-right: 0

    h3
      margin-bottom: $baseline / 2

      font-weight: 600   
      text-align: center 

      &::before
        +fa-icon()

        display: block
        margin-bottom: $baseline / 2

        font-size: 60px
        text-align: center

  section:nth-of-type(1) h3::before
    content: $fa-var-book

  section:nth-of-type(2) h3::before
   content: $fa-var-newspaper-o

  section:nth-of-type(3) h3::before
    content: $fa-var-pencil

  section:nth-of-type(4) h3::before
   content: $fa-var-money     


//- Contact us button
homepage--help-us--contact-us
  display: block
  
  text-align: center

  a
    display: inline-block
    border-radius: 5px
    padding: 0 $baseline

    background: $c-base
    color: #fff

    font-size: $fs-1
    line-height: $baseline * 1.5

    &:hover,
    &:focus
      background: darken($c-base, 10%)
</style>
