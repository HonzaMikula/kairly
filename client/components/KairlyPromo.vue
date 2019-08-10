<template>
  <div class="kairly-promo">
    <div>
      <section>
          <h1>
            {{ $t('Stop be distracted.') }}
            <br />
            {{ $t('Grow healthy reading habits.') }}
          </h1>

          <ul>
            <li>{{ $t('No notifications. No endless scrolling. No addiction and FOMO.') }}</li>
            <li>{{ $t('Read your sources at regular time you want. E.g. every day at 9am.') }}</li>
            <li>{{ $t('We update your timeline only every 3 hours. Because that\'s sane.') }}</li>
            <li>{{ $t('No magic algorithms. The content is chosen by you and the professional editors you trust.') }}</li>
          </ul>
        </section>

      <SignUpForm></SignUpForm>
    </div>
  </div>
</template>

<script>
import SignUpForm from '@/components/microsite/SignUpForm'

export default {
  name: 'KairlyPromo',

  components: {
    SignUpForm
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Kairly Promo -//

.kairly-promo
  position: relative

  display: flex
  align-items: center
  justify-content: center
  padding: $baseline

  background: #eee

  @media (max-width: $mobile)
    padding: 0 $baseline / 2

  > div
    display: grid
    grid-template-columns: 2fr 1fr
    max-width: 900px

    @media (max-width: $mobile)
      grid-template-columns: auto
      grid-row-gap: $baseline 

  section
    display: flex
    flex-direction: column
    align-items: flex-start
    justify-content: center

    h1
      font-size: $fs-4
      font-weight: 900
      line-height: 1.42
        
      padding: 0
      margin-bottom: $baseline * 2

      @media (max-width: $mobile)
        margin: $baseline 0
        width: 100%

        font-size: $fs-3
        line-height: $baseline * 1.2
        text-align: center


    > p
      font-size: $fs-0
      text-align: center

    ul
      padding: 0 $baseline 0 0

      counter-reset: benefits

      @media (max-width: $mobile)
        padding: 0 $baseline/4

    li
      display: flex
      align-items: center
      margin-bottom: $baseline / 2

      font-size: $fs-1
      line-height: 1.42

      @media (max-width: $mobile)
        font-size: $fs-0
        line-height: 1.42

      &:last-of-type
        margin-bottom: 0

      &::before
        display: inline-block
        margin-right: $baseline / 2
        border-radius: 100%
        height: $baseline * 1.25
        width: $baseline * 1.25
        flex: 0 0 $baseline * 1.25

        background: #fff

        font-size: $fs-0
        font-weight: 600
        line-height: $baseline * 1.25
        text-align: center

        counter-increment: benefits
        content: counter(benefits)


</style>
