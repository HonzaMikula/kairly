<template>
  <div class="homepage-view" itemscope itemtype="http://schema.org/WebPage">

    <section class="homepage--cover">
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
    </section>

    <ExploreNewspapers />

    <section class="homepage--process">

      <h2>How to start?</h2>

      <ul>
        <li class="rss">
          <nuxt-link to="/rss-reader">{{ $t('Import your RSS feeds') }}</nuxt-link>
        </li>

        <li class="twitter">
          {{ $t('Connect to your Twitter') }}
        </li>

        <li class="newspaper">
          {{ $t('Subscribe to digital newspapers') }}
        </li>
      </ul>

    </section>

    <section class="homepage--readers">
      <picture>
        <img src="~assets/homepage/kairly-1.jpg" />
      </picture>

      <div>
        <h2>{{ $t('Subscribe to a digital newspapers informing you on topics you are interested in.') }}</h2>
        <div v-html="$t('@homepage/readers')"></div>

        <!--
        <p>
          <strong>Editoři vybírají nejlepší články a tweety</strong> napříč všemi autory publikujícími na Kairly.
          Pravidelně budete dostávat (například každý den v 9:00) ten nejlepší obsah na dané téma.
        </p>

        <p>
          <strong>Editorem se může stát každý</strong>. Záleží pouze na tom, zda editor dokáže připravovat kvalitní vydání novin.
          <strong>Nezávislost a objektivita vzniká v otevřeném a férovém prostředí</strong>.
        </p>

        <p>
          Na Kairly nejsou žádné reklamy. Nesledujeme vás.
          Nesloužíme žádným byznysovým ani politickým zájmům.
          Za noviny se vždy platilo a <strong>zakoupením předplatného novin si kupujete kvalitní a nezávislý obsah</strong>.
        </p>
         -->
      </div>
    </section>

    <section class="homepage--quote">
      <blockquote>
        <div v-html="$t('@homepage/quote/honza')" itemprop="citation"></div>
        <!--
        <p>
          Sociální sítě se nás snaží přehltit zábavným či šokujícím obsahem, aby vydělali co nejvíce na reklamě.
          To není místo pro zpravodajství, které má být věcné a pravdivé. Kairly děláme pro lidi,
          kteří chtějí být skutečně informovaní a chtějí stimulovat své kritické uvažování.
        </p>

        <p>
          Na Kairly vás nerušíme žádnými notifikacemi, nesnažíme se vám neustále podstrčit nový
          rádoby zajímavý obsah. Pravidelně a vždy ve stejný čas zobrazujeme jen ten obsah,
          který jste si objednal a to od lidí, kterým věříte a kteří vás skutečně intelektuálně obohacují.
        </p>
         -->

        <footer>
          <img src="~assets/profiles/jan-mikula.jpg" alt="Jan Mikula" />
          <strong>Jan Mikula</strong> {{ $t('founder of Kairly') }}
        </footer>
      </blockquote>
    </section>

    <section class="homepage--readers">
      <picture>
        <img src="~assets/homepage/kairly-3.jpg" />
      </picture>

      <div>
        <h2>{{ $t('Are you a journalist? Start making money by publishing content or as a newspaper editor.') }}</h2>

        <div v-html="$t('@homepage/editors')"></div>
        <!--
        <p>
          Nás baví design a technologie. <strong>Vytváříme unikátní platformu pro vás novináře a vaše čtenáře.</strong>
          Vy se soustřeďte na to, v čem jste dobří - na dobrý obsah.
        </p>

        <p>
          <strong>Založte si noviny a vybírejte ty nejlepší články a tweety</strong> pro další vydání napříč všemi autory na Kairly.
          Za zajímavý vámi zprostředkovaný obsah vám <strong>čtenáři budou platit pravidelné měsíční předplatné</strong>.
        </p>

        <p>
          Čtenáři si mohou předplatit i přímo vás jako autora. Ostatní editoři mohou vaše články
          zařadit do svých vydání novin. <strong>Tím získáte podíl i z předplatného novin, ve kterých se vaše články objevily</strong>.
        </p>
         -->
      </div>
    </section>

    <section class="homepage--quote">
      <blockquote>
        <div v-html="$t('@homepage/quote/roman')" itemprop="citation"></div>
        <!--
        <p>
          O placeném obsahu se mluví už roky, ale současné modely pay-wallů zatím úspěchy příliš nesklízejí.
          Novináři jsou stále závislí na reklamním duopolu Googlu a Facebooku. Výsledkem je neustále snižování
          stavů redakcí a omezování nákladů. Čas na kvalitní novinářskou práci v podstatě není.
        </p>

        <p>
          Náš koncept placeného obsahu jde mnohem dál než obyčejný pay-wall. Využíváme principů absolutní otevřenosti
          a síťového efektu, kterými si nás před lety získaly sociální sítě. Právě proto věříme, že Kairly přináší
          vysněný fungující model placeného obsahu na internetu.
        </p>
        -->

        <footer>
          <img src="~assets/profiles/roman-krejcik.jpg" alt="Roman Krejčík" />
          <strong>Roman Krejčík</strong> {{ $t('founder of Kairly') }}
        </footer>
      </blockquote>
    </section>

    <!-- <section class="homepage--newspapers">
      <h2>{{ $t('Check out some of our newspapers.') }}</h2>

      <div>
        <NewspaperWidget
          v-for="newspaper in newspapers"
          :key="newspaper.fullName"
          :newspaper="newspaper"
        />
      </div>
    </section> -->

    <HowItWorks />

    <section class="homepage--quote">
      <h2>{{ $t('Was said about us.') }}</h2>

      <blockquote>
        <div v-html="$t('@homepage/quote/zouzalik')" itemprop="citation"></div>
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

        <footer>
          <img src="~assets/profiles/marek-zouzalik.jpg" alt="Marek Zouzalík" />
          <strong>Marek Zouzalík</strong> <a href="https://www.sncr-praha.cz/" target="_blank">{{ $t('chairman of the Prague Syndicate of Journalists') }}</a>
        </footer>
      </blockquote>
    </section>  

    <!-- <OfficialStart /> -->

    <div itemprop="author" itemscope itemtype="http://schema.org/Organization">
      <Footer />

      <FooterLinks />
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'

import { errorToParams } from '@/utils/errors'

import SignUpForm from '@/components/microsite/SignUpForm'
import NewspaperWidget from '@/components/widgets/NewspaperWidget'
import HowItWorks from '@/components/microsite/HowItWorks'
import Footer from '@/components/microsite/Footer'
import FooterLinks from '@/components/microsite/FooterLinks'
import OfficialStart from '@/components/microsite/OfficialStart'
import ExploreNewspapers from '@/components/microsite/ExploreNewspapers'

import ogImage from '@/assets/homepage/kairly-1.jpg'

export default {
  name: 'Homepage',

  components: {
    SignUpForm,
    NewspaperWidget,
    HowItWorks,
    OfficialStart,
    Footer,
    FooterLinks,
    ExploreNewspapers
  },

  head() {
    const metaTitle = this.$t('Kairly – Stop be distracted. Grow healthy reading habits.')
    const metaDescription = this.$t('Stop the distraction. Grow healthy reading habits with us. Import your RSS feed and Twitter and start reading the content in healthy way.')
    const metaUrl = 'https://kairly.com/'
    const baseUrl = 'https://kairly.com'

    return {
      title: metaTitle,
      meta: [
        { hid: 'description', name: 'description', content: metaDescription },
        { hid: 'og:title', property: 'og:title', content: metaTitle },
        { hid: 'og:description', property: 'og:description', content: metaDescription },
        { hid: 'og:image', property: 'og:image', content: baseUrl + ogImage },
        { hid: 'og:image:alt', property: 'og:image:alt', content: 'Woman reading' },
        { hid: 'og:type', property: 'og:type', content: 'product' },
        { hid: 'og:url', property: 'og:url', content: metaUrl },
        { hid: 'twitter:card', property: 'twitter:card', content: 'summary' },
        { hid: 'twitter:site', property: 'twitter:site', content: '@kairlynews' },
        { hid: 'twitter:title', property: 'twitter:title', content: metaTitle },
        { hid: 'twitter:description', property: 'twitter:description', content: metaDescription },
        { hid: 'twitter:image', property: 'twitter:image', content: baseUrl + ogImage }
      ]
    }
  },

  data() {
    return {
      invalidCredentials: false
    }
  },
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Mixin
=heading
  font-size: $fs-4
  font-weight: 900
  line-height: 1.42

  @media (max-width: $mobile)
    font-size: $fs-3
    line-height: $baseline * 1.2

//- Homepage -//
.homepage-view
  background: #fff

  > *
    max-width: 900px
    margin: 0 auto

//- Cover
.homepage--cover
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
        margin: $baseline/2 0
        width: 100%

        text-align: center


    > p
      font-size: $fs-0
      text-align: center

    ul
      padding: 0 $baseline 0 0

      counter-reset: benefits

      @media (max-width: $mobile)
        padding: 0 $baseline/2 $baseline/2 $baseline/2

    li
      display: flex
      align-items: center
      margin-bottom: $baseline / 2

      font-size: $fs-1
      line-height: 1.42

      &:last-of-type
        margin-bottom: 0

      @media (max-width: $mobile)
        font-size: $fs-0
        line-height: 1.42

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

//- Process
.homepage--process
  background: #f5f5f5
  padding: $baseline

  @media (max-width: $mobile)
    display: none

  h2
    +heading
    margin-bottom: $baseline / 2
    display: none

  ul
    display: flex
    justify-content: center

    @media (max-width: $mobile)
      flex-direction: column

  li
    display: flex
    align-items: center
    margin-right: $baseline * 2

    font-size: $fs-0
    font-weight: 600

    @media (max-width: $mobile)
      margin-bottom: $baseline / 2

    &:last-of-type
      margin-right: 0

    &::before
      +fa-icon()

      border-radius: 100%
      margin-right: $baseline / 4
      height: $baseline * 1.25
      width: $baseline * 1.25

      font-size: $fs-1
      line-height: $baseline * 1.25
      text-align: center

      background: #fff
    
    a
      color: #000

      text-decoration: underline

      &:hover,
      &:focus
        text-decoration: none

  .rss::before
    @extend .fas

    content: fa-content($fa-var-rss)

  .twitter::before
    @extend .fab

    content: fa-content($fa-var-twitter)

  .newspaper::before
    @extend .fas

    content: fa-content($fa-var-newspaper)


//- Readers
.homepage--readers
  display: grid
  grid-template-areas: "hp-readers-picture hp-readers-text"
  grid-template-columns: 334px 540px
  grid-column-gap: $baseline
  padding: $baseline*2 0

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

.homepage--quote
  padding: $baseline*2
  margin-bottom: $baseline * 2

  background: #f5f5f5

  @media (max-width: 950px)
    margin-bottom: 0

  @media (max-width: $mobile)
    padding: $baseline

  h2
    +heading
    margin-bottom: $baseline

  blockquote
    p
      margin-bottom: $baseline

      font-size: $fs-2

      @media (max-width: $mobile)
        font-size: $fs-1

      &:first-of-type::before
        +fa-icon()
        @extend .fas
        position: absolute
        transform: translateX(-20px)
        font-size: $fs--2

        color: #555

        content: fa-content($fa-var-quote-left)

      &:last-of-type::after
        +fa-icon()
        @extend .fas

        position: absolute
        font-size: $fs--2
        transform: translateX(5px)

        color: #555

        content: fa-content($fa-var-quote-right)


    footer
      display: flex

      font-size: $fs-1
      line-height: $baseline * 1.5

      a
        color: #000

        text-decoration: underline

        &:hover,
        &:focus
          text-decoration: none

      @media (max-width: $mobile)
        flex-direction: column
        align-items: center

        line-height: $baseline
        text-align: center

      strong::after
        margin-right: 4px

        font-weight: 600

        content: ', '

        @media (max-width: $mobile)
          content: none

      img
        margin-right: $baseline / 2
        border-radius: 100%
        height: $baseline * 1.5
        width: $baseline * 1.5

        @media (max-width: $mobile)
          height: $baseline * 2
          margin-right: 0
          width: $baseline * 2


//- Newspapers showcase
.homepage--newspapers
  margin-bottom: $baseline * 2

  @media (max-width: 950px)
    padding: $baseline $baseline 0 $baseline

  @media (max-width: $mobile)
    padding: $baseline $baseline/2
    margin-bottom: 0

  > h2
    +heading

    margin-bottom: $baseline

  //- wrapper
  > div
    display: grid
    grid-row-gap: $baseline
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2

    @media (max-width: $mobile)
      grid-column-gap: $baseline / 4
      overflow-x: auto
      -webkit-overflow-scrolling: touch

      newspaper-widget-view,
      issue-widget-view
        min-width: 200px

</style>
