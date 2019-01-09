<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop class="join-us">
      <header>
        <h1>{{ $t('Are you interested in Kairly?') }}</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>
      <main>
        <h3>{{ $t('Participate in user testing') }}</h3>
        <p>
          {{ $t('@joinus/usertesting') }}
          <!--
          We are doing 30 - 60 minutes user testing interviews over Skype (or some other communication tool).
          We will give you access to Kairly. You will share screen with us. We will observe how you use Kairly.
          Together we will discuss what you like, what you don't like and how we can improve the app.
          -->
        </p>

        <p>
          <a href="mailto:info@kairly.com?subject=Kairly user testing&amp;body=Hi, I would like to do user testing for Kairly.">{{ $t('Schedule user testing interview') }}</a>
        </p>

        <h3>{{ $t('Join Facebook group') }}</h3>
        <p>
          {{ $t('@joinus/joinfacebook') }}
          <!--
          We have Kairly group on Facebook, where we regularly share what's new in Kairly and what we are planning for next weeks.
          It's place where people give us feedback and propose ideas, how we can improve Kairly.
          -->
        </p>

        <p>
          <a href="https://www.facebook.com/groups/276916213077456/">{{ $t('Join Facebook group') }}</a>
        </p>

        <h3>{{ $t('Follow us on social media') }}</h3>
        <div class="social-media">
          <a
            href="https://www.facebook.com/kairlynews/"
            class="facebook"
            :title="$t('Follow us Facebook')">
          </a>

          <a
            href="https://twitter.com/kairlynews"
            class="twitter"
            :title="$t('Follow us Twitter')">
          </a>

          <a
            href="https://www.linkedin.com/company/kairly/"
            class="linkedin"
            :title="$t('Follow us LinkedIn')">
          </a>
        </div>

        <h3>{{ $t('Join private beta') }}</h3>
        <p>
          {{ $t('@joinus/joinprivatebeta') }}
          <!--
          We are inviting limited number of people to use Kairly and give us feedback about the app.
          Based on the feedback we are improving the app every week. Although there can be many bugs in the app,
          you can experience our ideas how to improve current state of journalism.-->
        </p>

        <!-- Begin Mailchimp Signup Form -->
        <div id="mc_embed_signup">
          <form action="https://honzamikula.us8.list-manage.com/subscribe/post?u=0aa8c0b091d21d477832fbe62&amp;id=7c7468a76d" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
            <div id="mc_embed_signup_scroll">
              <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" :placeholder="$t('email address')" required>
              <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
              <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_0aa8c0b091d21d477832fbe62_7c7468a76d" tabindex="-1" value=""></div>
              <div class="clear"><input type="submit" :value="$t('Request to join')" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
            </div>
          </form>
        </div>
        <!--End mc_embed_signup-->
      </main>
    </modal-dialog>
  </dialog-window>
</template>


<script>
import DialogWindow from '@/components/modals/Dialog'

export default {
  name: 'JoinUsDialog',

  props: {
    closeModal: Function
  },

  components: {
    DialogWindow
  }
}
</script>

<style lang="sass">
modal-dialog.join-us
  max-width: 600px

  > header h1
    @media (max-width: $mobile)
      padding: 0 $baseline/2

  main
    padding: $baseline
    overflow: auto
    -webkit-overflow-scrolling: touch

    background: #fff

    @media (max-width: $mobile)
      padding: $baseline/2

  h3
    margin: $baseline 0 $baseline/2 0
    font-weight: 600
    font-size: $fs-1

    &:first-of-type
      margin-top: 0

  p
    margin-bottom: $baseline / 2

    line-height: 1.42


  a
    display: inline-block
    border-radius: 5px
    padding: 0 $baseline/2

    background: $c-base
    border: 1px solid $c-base
    color: #fff

    cursor: pointer
    font-family: $ff-sans
    font-size: $fs-0
    line-height: $baseline

    &:focus,
    &:hover
      background: darken($c-base, 10%)

  //- Mailchimp
  #mc_embed_signup
    #mc_embed_signup_scroll
      display: flex
      justify-content: center

      @media (max-width: $mobile)
        display: block

    input[type=email]
      box-sizing: border-box
      border-radius: 5px 0 0 5px
      height: $baseline * 1.5
      padding: 0 $baseline/2
      margin-bottom: $baseline / 2
      width: 250px

      background: #fff
      border: 1px solid #ddd
      opacity: 0.9

      font-family: $ff-sans
      font-size: $fs-0
      line-height: $baseline * 1.5

      transition: 0.15s opacity

      &:focus
        opacity: 1

    input[type=submit]
      box-sizing: border-box
      border-radius: 0 5px 5px 0
      height: $baseline * 1.5
      padding: 0 $baseline
      margin-bottom: $baseline

      background: $c-base
      border: 0
      color: #fff

      cursor: pointer
      font-size: $fs-1
      font-family: $ff-sans
      line-height: $baseline * 1.5

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


  .social-media
    a
      border-radius: 5px
      display: inline-block
      height: $baseline * 1.5
      margin-right: $baseline / 2
      width: $baseline * 1.5

      background: #eee
      border: 0
      color: #555

      font-size: $fs-3
      line-height: $baseline * 1.5
      text-align: center

      &:focus,
      &:hover
        background: #ddd

      &::before
        +fa-icon()
        @extend .fas

    a.facebook::before
      content: fa-content($fa-var-facebook)

    a.twitter::before
      content: fa-content($fa-var-twitter)

    a.linkedin::before
      content: fa-content($fa-var-linkedin)
</style>
