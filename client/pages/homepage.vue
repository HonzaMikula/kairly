<template>
  <app-layout>
    <homepage-view>
      <homepage--cover>
        <div>
          <h1>Help us resurrect journalism</h1>

          <!-- Begin Mailchimp Signup Form -->
          <div id="mc_embed_signup">
            <form action="https://honzamikula.us8.list-manage.com/subscribe/post?u=0aa8c0b091d21d477832fbe62&amp;id=7c7468a76d" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
              <div id="mc_embed_signup_scroll">
                <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" placeholder="email address" required>
                <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
                <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_0aa8c0b091d21d477832fbe62_7c7468a76d" tabindex="-1" value=""></div>
                <div class="clear"><input type="submit" value="Request to join" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
              </div>
            </form>
          </div>
          <!--End mc_embed_signup-->

          <p>Become author, editor or reader.</p>
        </div>

      </homepage--cover>
      <homepage--roles>
        <div>
          <h3>Authors</h3>
          <p>
            Authors focus on writing.
            They are creating high quality articles &amp; tweets.
          </p>
        </div>

        <div>
          <h3>Editors</h3>
          <p>
            Editors run their newspaper.
            They are selecting the best articles &amp; tweets from authors.
          </p>
        </div>

        <div>
          <h3>Readers</h3>
          <p>
            Readers choose what they want to read and when.
            They subscribe either directly to authors or to newspapers.
          </p>
        </div>
      </homepage--roles>

      <homepage--how-it-works>
        <div>
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

          <p>
            In Kairly readers are subscribing newspapers and paying for them.
            Those money are then shared between editors and authors.
          </p>

          <div>
            <img src="~assets/homepage/kairly-concept-5.png" alt="Kairly Screenshot"/>
          </div>
        </div>
      </homepage--how-it-works>

      <homepage--values>
        <div>
          <h2>What we believe in?</h2>

          <p>
            In the world full of fake news, manipulations and attacks on journalism, we stand for <strong>truth</strong>.
          </p>

          <p>In the world full of censorship and propaganda, we stand for <strong>free speech</strong>.</p>

          <p>
            In the world full of distraction and lack of focus, we stand for
            <strong>control of your time and undistracted reading experience</strong>.
          </p>

          <p>
            In the world where journalist are dependent on advertisment or big corporations with their interests,
            we stand for <strong>fair reward for high-quality content</strong>.
          </p>

          <p>Stand with us!</p>
        </div>
      </homepage--values>

      <homepage--help-us>
        <h2>How you can help?</h2>
        <p>You can help us create exceptional journalism in different ways.</p>

        <div>
          <section>
            <h3>Readers</h3>
            <ul>
              <li>join our private beta program</li>
              <li>participate in user testing interviews over Skype</li>
            </ul>
          </section>

          <section>
            <h3>Editors</h3>
            <ul>
              <li>start your newspaper on Kairly</li>
              <li>participate in user testing interviews over Skype</li>
            </ul>
          </section>

          <section>
            <h3>Authors</h3>
            <ul>
              <li>start publishing your content on Kairly</li>
              <li>participate in  user testing interviews over Skype</li>
            </ul>
          </section>
        </div>

        <homepage--help-us--contact-us>
          <a href="" @click.prevent="isJoinUsModalOpen = true">Join us</a>
        </homepage--help-us--contact-us>
      </homepage--help-us>

      <portal to="modal" v-if="isJoinUsModalOpen">
        <JoinUsModal :closeModal="closeJoinUs"></JoinUsModal>
      </portal>
    </homepage-view>
  </app-layout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import JoinUsModal from '@/components/modals/JoinUs'

export default {
  name: 'Homepage',

  auth: false,

  components: {
    AppLayout,
    JoinUsModal
  },

  data() {
    return {
      invalidCredentials: false,
      username: null,
      password: null,
      isJoinUsModalOpen: null
    }
  },

  methods: {
    async login() {
      this.invalidCredentials = false
      const { username, password } = this
      try {
        await this.$auth.loginWith('local', {
          data: { username, password }
        })
        this.$router.push("/")
      } catch (e) {
        this.invalidCredentials = true
      }
    },

    closeJoinUs() {
      this.isJoinUsModalOpen = null
    }
  },

  async fetch ({ store, redirect }) {
    if (store.state.auth.loggedIn) {
      redirect('/')
      return
    }
  }
}
</script>

<style lang="sass">
//- Cover
homepage--cover
  display: flex
  align-items: center
  justify-content: center
  box-sizing: border-box
  height: 400px
  padding: $baseline * 1

  background: url("~assets/homepage/hero.png") center center no-repeat
  background-size: cover

  color: #fff

  font-family: $ff-serif


  > div
    text-align: center

  h1
    margin-bottom: $baseline

    font-size: $fs-4
    line-height: $baseline * 2
    text-shadow: 0 0 10px #000

    @media (max-width: $mobile)
      font-size: $fs-3
      line-height: $baseline * 1.5

  p
    text-shadow: 0 0 10px #000

  //- MailChimp
  #mc_embed_signup
    input[type=email]
      border-radius: 5px
      height: $baseline * 1.5
      padding: 0 $baseline/2
      margin-bottom: $baseline / 2
      width: 250px

      background: #fff
      box-shadow: 0 0 5px #000
      border: 0
      opacity: 0.9

      font-family: $ff-sans
      font-size: $fs-0
      line-height: $baseline * 1.5

      transition: 0.15s opacity

      &:focus
        opacity: 1

    input[type=submit]
      border-radius: 5px
      padding: $baseline/4 $baseline
      margin-bottom: $baseline

      background: $c-base
      box-shadow: 0 0 5px #555
      border: 0
      color: #fff

      cursor: pointer
      font-size: $fs-1
      font-family: $ff-sans

      &:focus,
      &:hover
        background: darken($c-base, 10%)


  #mc-embedded-subscribe-form input[type=checkbox]
    display: inline
    width: auto
    margin-right: 10px

  #mergeRow-gdpr
    margin-top: 20px

  #mergeRow-gdpr fieldset label
    font-weight: normal

  #mc-embedded-subscribe-form .mc_fieldset
    border: none
    min-height: 0px
    padding-bottom: 0px

//- Roles
homepage--roles
  display: flex
  max-width: 900px
  margin: 0 auto

  font-family: $ff-serif

  @media (max-width: $mobile)
    flex-direction: column

  div
    position: relative

    flex: 1
    padding: $baseline 0
    margin-right: $baseline*2

    @media (max-width: $mobile)
      padding: $baseline

    &:last-of-type
      margin-right: 0

  h3
    margin-bottom: $baseline / 2

    font-size: $fs-3
    font-family: $ff-serif


//- Values
homepage--values
  display: block
  padding: $baseline * 2 $baseline

  > div
    margin: 0 auto
    max-width: 900px

  //- heading
  h2
    margin-bottom: $baseline * 2
    font-size: $fs-3
    font-family: $ff-serif

    @media (max-width: $mobile)
      margin-bottom: $baseline

  //- values
  p
    margin: 0 auto $baseline auto
    max-width: 900px

    font-size: $fs-1
    font-family: $ff-serif

    @media (max-width: $mobile)
      font-size: $fs-0

    strong
      font-weight: 600

    &:last-of-type
      margin-top: $baseline * 2
      font-size: $fs-3


homepage--how-it-works
  display: block
  padding: $baseline*2 $baseline $baseline $baseline

  background: #eee

  font-family: $ff-serif

  > div
    margin: 0 auto
    max-width: 900px

  //- heading
  h2
    margin-bottom: $baseline * 2
    font-size: $fs-3
    font-family: $ff-serif

    @media (max-width: $mobile)
      margin-bottom: $baseline

  p
    max-width: 900px
    margin: 0 auto $baseline auto

    font-size: $fs-1

    @media (max-width: $mobile)
      font-size: $fs-0

      &:last-of-type
        margin: 0

  > div > div
    display: table
    margin: 0 auto

  img
    display: block
    margin-right: $baseline

    max-width: 824px

    @media (max-width: $mobile)
      float: none
      margin: 0 0 $baseline 0
      width: 100%

      &:last-of-type
        margin: 0

//- Help Us
homepage--help-us
  display: block
  padding: $baseline

  background: #eee

  font-family: $ff-serif
  text-align: center

  @media (max-width: $mobile)
    text-align: left

  //- Heading
  h2
    margin-bottom: $baseline

    font-size: $fs-3
    font-family: $ff-serif


  //- wrapper
  > div
    display: flex
    max-width: 900px
    margin: $baseline*2 auto

    @media (max-width: $mobile)
      display: block

  //- section
  section
    flex: 1
    margin-right: $baseline * 2

    text-align: left

    @media (max-width: $mobile)
      margin: 0 0 $baseline 0


    &:last-of-type
      margin-right: 0

    h3
      margin-bottom: $baseline / 2

      font-weight: 600

      @media (max-width: $mobile)
        font-size: $fs-1

    ul li
      list-style: disc
      text-align: left



//- Contact us button
homepage--help-us--contact-us
  display: block

  text-align: center

  a
    display: inline-block
    border-radius: $baseline / 4
    padding: 0 $baseline

    background: $c-base
    color: #fff

    font-family: $ff-sans
    font-size: $fs-1
    line-height: $baseline * 1.5

    &:hover,
    &:focus
      background: darken($c-base, 10%)
</style>
