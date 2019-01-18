<template>
  <div class="kairly-promo">
    <div>
      <h2><nuxt-link to="/">Kairly</nuxt-link></h2>
      <p>{{ $t('Help us create exceptional journalism.') }}</p>

      <!-- Begin Mailchimp Signup Form -->
      <div id="mc_embed_signup">
        <form action="https://honzamikula.us8.list-manage.com/subscribe/post?u=0aa8c0b091d21d477832fbe62&amp;id=7c7468a76d" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
          <div id="mc_embed_signup_scroll">
            <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" placeholder="email address" required>
            <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
            <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_0aa8c0b091d21d477832fbe62_7c7468a76d" tabindex="-1" value=""></div>
            <div class="clear"><input type="submit" :value="$t('Request to join private beta')" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
          </div>
        </form>
      </div>
      <!--End mc_embed_signup-->
      <div class="kairly-promo--learn-more">
        <nuxt-link to="/">{{ $t('Learn more about Kairly') }}</nuxt-link>
      </div>

      <div class="kairly-promo--social-media">
        <a
          href="https://www.facebook.com/kairlynews/"
          class="facebook"
          :title="$t('Follow us on Facebook')"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
        </a>

        <a
          href="https://twitter.com/kairlynews"
          class="twitter"
          :title="$t('Follow us on Twitter')"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
        </a>

        <a
          href="https://www.linkedin.com/company/kairly/"
          class="linkedin"
          :title="$t('Follow us on LinkedIn')"
          v-b-tooltip="{delay:{ 'show': 500, 'hide': 0 }}">
        </a>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'KairlyPromo'
}
</script>

<style lang="sass">
//- Kairly Promo -//

.kairly-promo
  display: flex
  align-items: center
  justify-content: center
  box-sizing: border-box
  height: 400px
  padding: $baseline

  background: url("~assets/homepage/hero-new.jpg") bottom center no-repeat
  background-size: cover

  color: #fff

  font-family: $ff-serif

  > div
    text-align: center


  h2
    margin-bottom: $baseline

    color: #000
    text-shadow: 0 0 3px #fff

    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2

    @media (max-width: $mobile)
      font-size: $fs-3
      line-height: $baseline * 1.5

    a
      color: #000

  p
    margin-bottom: $baseline

    color: #000
    text-shadow: 0 0 3px #fff

    font-size: $fs-2
    font-weight: 600


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

//- Learn more links
.kairly-promo--learn-more
  a
    color: #000
    text-shadow: 0 0 3px #fff

    font-family: $ff-sans
    text-decoration: underline

    &:hover,
    &:focus
      text-decoration: none


//- Social media links
.kairly-promo--social-media
  padding-top: $baseline

  a
    border-radius: 100%
    display: inline-block
    height: $baseline * 1.5
    margin: 0 $baseline/2
    width: $baseline * 1.5

    background: rgba(0, 0, 0, 0.1)
    color: #fff

    font-size: $fs-3
    line-height: $baseline * 1.5
    text-align: center

    transition: 0.15s all

    &:focus,
    &:hover
      background: #fff
      color: #000

    &::before
      +fa-icon()
      @extend .fab
      line-height: $baseline * 1.5
      vertical-align: top

    &.facebook::before
      content: fa-content($fa-var-facebook)

    &.twitter::before
      content: fa-content($fa-var-twitter)

    &.linkedin::before
      content: fa-content($fa-var-linkedin)
</style>
