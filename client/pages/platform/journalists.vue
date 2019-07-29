<template>
  <AppLayout>
    <div class="journalists-view">
      <section class="journalists--hero">
        <div>
          <section>
            <h1>{{ $t('Are you independent journalist or blogger?') }}</h1>
            <ul>
              <li>{{ $t('Publish on a modern platform that you do not have to maintain.') }}</li>
              <li>{{ $t('Start earning with a unique concept of paid content.') }}</li>
              <li>{{ $t('Become a truly independent author.') }}</li>
            </ul>
          </section>

          <SignUpForm></SignUpForm>
        </div>
      </section>

      <ExploreNewspapers />

      <Faq>
        <img src="~assets/microsite/kairly-independent-journalist-1.jpg" alt="Kairly" />
      </Faq>

      <Quote :heading="$t('Was said about us.')" :quote="$t('@homepage/quote/zouzalik')">
        <!--
        <p>
          Nowadays, when attacks on journalists, including physical ones, are increasing, we need to find a
          sustainable economic model for journalism. Only in this way can we keep independent journalism on
          politicians and large private corporations. And only in this way we can resist the phenomena of fake
          news and ensure that the complete freedom of speech is preserved.
        </p>

        <p>
          Kairly comes up with an interesting concept of paid content on the internet, which is significantly
          different from the current not very successful attempts.
        </p>
        -->
        <img src="~assets/profiles/marek-zouzalik.jpg" alt="Marek Zouzalík" />
        <strong>Marek Zouzalík</strong>
        <a href="https://www.sncr-praha.cz/" target="_blank">{{ $t('chairman of the Prague Syndicate of Journalists') }}</a>
      </Quote>


      <section class="microsite--section">
        <picture>
          <img src="~assets/microsite/kairly-independent-journalist-2.jpg" />
        </picture>

        <div>
          <h2>{{ $t('Publish on a modern platform that you do not have to worry about.') }}</h2>

          <div v-html="$t('@independent-journalists/modern-platform')">
          </div>
            <!-- <p>
              Tvoříme pro vás moderní digitální platformu, která je šita na míru novinářům a publicistům.
              Čtenářům nabízíme prostor pro nerušené čtení, ať už používají počítač, mobil, tablet či v budoucnu elektronickou čtečku.
            </p>

            <p>
              Jsme milovníci starých dobrých papírových novin a časopisů. Design platformy kombinuje to nejlepší z éry tištěných periodik
              a moderní trendy UX ze současných mobilních a webových aplikací.
            </p>

            <p>Na platformě můžete publikovat zdarma. Ve chvíli, kdy vám čtenáři začnou platit, budeme si účtovat 15 % z ceny předplatného.</p> -->

        </div>
      </section>

      <Quote :quote="$t('@independent-journalists/quote/jan-mikula')">
        <!-- <p>
            Pro novináře, publicisty a blogery tvoříme otevřenou platformu po vzoru sociálních sítí,
            kde autoři budou férově soutěžit, kdo dokáže nejlépe a nejzajímavěji informovat čtenáře.
            A dostávat za to zaslouženě zaplaceno.
          </p>

          <p>
            V dnešní době plné nekonečného proudu nedůležitých informací a neustáleho vyrušování notifikacemi vytváříme pro čtenáře prostor,
            kde mohou nerušeně číst, to co opravdu chtějí číst a v době, kdy jsou na to zvyklý. Zkrátka doba, kdy jsme si cestou do práce
            koupili noviny a četli si je autobuse měla něco do sebe.
          </p> -->

        <img src="~assets/profiles/jan-mikula.jpg" alt="Jan Mikula" />
        <strong>Jan Mikula</strong> {{ $t('founder of Kairly') }}
      </Quote>

      <section class="microsite--section">
        <picture>
          <img src="~assets/microsite/kairly-independent-journalist-5.jpg" />
        </picture>

        <div>
          <h2>{{ $t('Start monetizing your content and become a truly independent author.') }}</h2>

          <div v-html="$t('@independent-journalists/monetizing-content')"></div>
            <!-- <p>
              Reklama kvalitní obsah nezaplatí. Čtenáře musíme naučit opět platit za kvalitní obsah.
              Musíme na to chytře. Zapojte se do našeho unikátního systému placeného obsahu.
            </p>

            <p>
              Čtenáři si vás buď mohou předplatit napřímo, nebo si předplácí noviny od editorů, kteří
              vaše články a tweety považují za kvalitní a zařazují je do svých vydání. Vy za to dostanete
              spravedlivý podíl z peněz, které editoři vybrali za své noviny.
            </p>

            <p>
              Pokud píšete mimořádně zajímavý obsah, čtenáři mají možnost vám poslat peníze nad
              rámec běžného předplatného.
            </p> -->
        </div>
      </section>

      <Quote :quote="$t('@independent-journalists/quote/roman-krejcik')">
        <!-- <p>
            Reklama kvalitní novinářskou a publicistickou tvorbu nezaplatí. Speciálně, když tu máme duopol Googlu a Facebooku.
            Placený obsah se vrací. Jde to ale z těžka. Většina současných pokusů není příliš úspěšných. Musíme na to chytřeji.
          </p>

          <p>
            Využijme toho, co udělalo sociální sítě tak úspěšné. Kairly využívá absolutní otevřenosti a síťového efektu,
            díky kterému mohou čtenáři číst opravdu jen to, co chtějí a to od autorů na příč celou platformou.
            Tato vysoká personalizace obsahu je klíč k úspěšněmu modelu placeného obsahu.
          </p> -->

        <img src="~assets/profiles/roman-krejcik.jpg" alt="Roman Krejčík" />
        <strong>Roman Krejčík</strong> {{ $t('founder of Kairly') }}
      </Quote>

      <HowItWorks />

      <Footer />

      <FooterLinks />

    </div>
  </AppLayout>
</template>

<script>
import { mapState } from 'vuex'

import SignUpForm from '@/components/microsite/SignUpForm'
import AppLayout from '@/components/layout/AppLayout'
import Quote from '@/components/microsite/Quote'
import HowItWorks from '@/components/microsite/HowItWorks'
import Footer from '@/components/microsite/Footer'
import FooterLinks from '@/components/microsite/FooterLinks'
import Faq from '@/components/microsite/Faq'
import ExploreNewspapers from '@/components/microsite/ExploreNewspapers'

export default {
  name: 'IndependentJournalists',

  auth: false,

  components: {
    AppLayout,
    Quote,
    HowItWorks,
    Footer,
    FooterLinks,
    Faq,
    SignUpForm,
    ExploreNewspapers
  },

  head() {
    return {
      title: this.$t('Digital Publishing Platform for Journalists and Bloggers') +' – Kairly',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: this.$t('Kairly is a digital publishing platform for independent journalists and bloggers who wants to start earning money for writing good content.') },
      ]
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Mixin
=heading
  font-size: $fs-5
  font-weight: 900
  line-height: $baseline * 2

  @media (max-width: $mobile)
    font-size: $fs-3
    line-height: $baseline * 1.2

.journalists-view
  background: #fff

  > *
    max-width: 900px
    margin-left: auto
    margin-right: auto

//- Hero
.journalists--hero
  position: relative

  display: flex
  align-items: center
  justify-content: center
  min-height: 400px
  margin-bottom: $baseline * 2
  padding: $baseline
  max-width: none

  background-size: cover
  background: #f5f5f5

  @media (max-width: 950px)
    margin-bottom: 0

  @media (max-width: $mobile)
    height: auto
    padding: 0
    padding-bottom: $baseline / 2

  > div  
    display: grid
    grid-template-columns: 2fr 1fr
    max-width: 900px

    @media (max-width: $mobile)
      grid-template-columns: auto

  section
    display: flex
    flex-direction: column
    align-items: flex-start
    justify-content: center

  h1
    +heading
    padding: 0
    margin-bottom: $baseline * 2

    @media (max-width: $mobile)
      margin: $baseline $baseline/2
      width: 100%


  > p
    font-size: $fs-0
    text-align: center

  ul
    padding: 0 $baseline 0 0

    counter-reset: benefits

    @media (max-width: $mobile)
      padding: 0 $baseline/2

  li
    display: flex
    align-items: center
    margin-bottom: $baseline / 2

    font-size: $fs-1

    @media (max-width: $mobile)
      font-size: $fs-1

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

//- Section
.microsite--section
  display: grid
  grid-template-areas: "hp-readers-picture hp-readers-text"
  grid-template-columns: 334px 540px
  grid-column-gap: $baseline
  margin-bottom: $baseline * 2

  @media (max-width: 950px)
    grid-template-areas: "hp-readers-picture" "hp-readers-text"
    grid-template-columns: auto
    padding: 0

  @media (max-width: $mobile)
    grid-template-areas: "hp-readers-picture" "hp-readers-text"
    grid-template-columns: auto
    padding: 0

  > picture
    grid-area: hp-readers-picture

    img
      height: 100%
      width: 100%

      object-fit: cover

      @media (max-width: 950px)
        max-height: 300px
        object-position: 0 60%

  > div
    grid-area: hp-readers-text

    @media (max-width: 950px)
      padding: $baseline

    @media (max-width: $mobile)
      padding: $baseline / 2

    h2
      +heading
      margin-bottom: $baseline

    p
      position: relative

      margin-bottom: $baseline
      padding-left: $baseline
      max-width: 600px

      font-size: $fs-1

      &:last-of-type
        margin-bottom: 0

      @media (max-width: $mobile)
        padding-left: 0

      &::before
        position: absolute
        left: 0

        width: $baseline

        font-size: $fs-3
        text-align: center

        content: '•'

        @media (max-width: $mobile)
          content: none


//- Benefits
.journalists--benefits
  display: grid
  grid-template-columns: 1fr 1fr
  grid-column-gap: $baseline * 2

  padding-bottom: $baseline * 2

  div

    h2
      margin-bottom: $baseline

      font-size: $fs-4
      font-weight: 900
      line-height: $baseline * 1.5

    p
      margin-bottom: $baseline

      font-size: $fs-1


    li
      margin-left: $baseline / 2
      margin-bottom: $baseline / 2
      list-style: disc

      font-size: $fs-1

</style>
