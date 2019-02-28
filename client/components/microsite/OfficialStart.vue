<template>
  <section class="microsite-oficial-start">
    <h2>{{ $t('We start officially') }}</h2>
    <p>{{ $t('3rd quarter 2019') }}</p>
    <p>{{ $t('Participate in closed beta and be among the first to begin making money on it.') }}</p>

    <!-- Begin Mailchimp Signup Form -->
    <div id="mc_embed_signup">
      <form action="https://honzamikula.us8.list-manage.com/subscribe/post?u=0aa8c0b091d21d477832fbe62&amp;id=aed6875343" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
        <div id="mc_embed_signup_scroll">
          <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" placeholder="email" required>
          <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
          <div style="position: absolute; left: -5000px;" aria-hidden="true">
            <input type="text" name="b_0aa8c0b091d21d477832fbe62_aed6875343" tabindex="-1" value="">
            <input type="checkbox" value="1" name="group[84725]" checked />
          </div>
          <div class="clear"><input type="submit" :value="$t('Request to join')" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
        </div>
      </form>
    </div>
    <!--End mc_embed_signup-->
  </section>
</template>

<script>
export default {
  name: 'OfficialStart'
}
</script>

<style lang="sass">
//- Launch
.microsite-oficial-start
  display: flex
  flex-direction: column
  align-items: center
  justify-content: center
  padding: $baseline * 2 $baseline * 2 $baseline $baseline * 2
  margin-bottom: $baseline * 2 !important

  background: #f5f5f5

  font-size: $fs-1

  @media (max-width: $mobile)
    margin-bottom: 0
    padding: $baseline

  h2
    margin-bottom: $baseline * 2
    font-size: $fs-1

  h2 + p
    margin-bottom: $baseline * 2
    font-size: 48px
    font-weight: 600

    @media (max-width: $mobile)
      font-size: $fs-5


  //- Mailchimp
  #mc_embed_signup
    margin-top: $baseline

    #mc_embed_signup_scroll
      display: flex
      justify-content: center

      @media (max-width: $mobile)
        align-items: center
        flex-direction: column

    input[type=email]
      box-sizing: border-box
      border-radius: 5px 0 0 5px
      height: $baseline * 1.5
      padding: 0 $baseline/2
      margin-bottom: $baseline / 2
      max-width: 250px

      background: #fff
      border: 1px solid #ddd
      opacity: 0.9

      font-family: $ff-sans
      font-size: $fs-0
      line-height: $baseline * 1.5

      transition: 0.15s opacity

      @media (max-width: $mobile)
        border-radius: 5px


      &:focus
        opacity: 1

    input[type=submit]
      box-sizing: border-box
      border-radius: 0 5px 5px 0
      height: $baseline * 1.5
      padding: 0 $baseline
      margin-bottom: $baseline/2

      background: $c-base
      border: 0
      color: #fff

      cursor: pointer
      font-size: $fs-1
      font-family: $ff-sans
      line-height: $baseline * 1.5

      @media (max-width: $mobile)
        border-radius: 5px

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
</style>
