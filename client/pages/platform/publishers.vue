<template>
  <AppLayout>
    <div class="journalists-view">
      <section class="journalists--hero">
        <div>
          <section>
            <h1>{{ $t('Are you an independent publisher?') }}</h1>

            <p>{{ $t('Publish modern newsletters and allow readers to contribute you for your content.') }}</p>

            <ul>
              <li><span v-html="$t('<strong>Build a base of regular readers </strong> by sending daily, weekly, or monthly newsletters.')" /></li>
              <li><span v-html="$t('<strong>Let readers consume content as they like. </strong> We can send newsletters to email, RSS readers, Kindle or readers can use modern mobile and web applications.')" /></li>
              <li><span v-html="$t('<strong>Earn additional revenues </strong> by charging a newsletter or voluntary donations.')" /></li>
            </ul>

            <div class="journalists--hero--call-to-action">
              <button @click="openRequestSolutionModal()">{{ $t('Request demo') }}</button>
              <a href="/downloads/kairly-brozura.pdf" download @click="downloadPDF()">{{ $t('Download PDF brochure') }}</a>
            </div>
          </section>

          <picture>
            <img src="~assets/microsite/newsletter-illustration4.png" alt="Newsletter illustration">
          </picture>
        </div>
      </section>

      <section class="microsite--section">
        <picture>
          <img src="~assets/microsite/kairly-random-25.jpg">
        </picture>

        <div>
          <h2>{{ $t('Why you should publish regular newsletters for your readers?') }}</h2>

          <div v-html="$t('@publishers/why-newsletters')" />
          <!-- <p>
              Ve věku sociálních médiích je těžké si udržet věrné čtenáře. Pravidelné
              newslettery v moderním provedením jsou způsobem, jak si vytvořit věrnou
              čtenářskou základnu.
            </p>

            <p>
              Naše newslettery se inspirují papírovými novinami s krásnou typografií a
              layoutem a kombinují je s moderními formáty internetu, jako jsou například tweety.
            </p>

            <p>
              Profesionální placený obsah je na vzestupu. Podívejte se na HBO Go, Spotify a další.
              Kvalitně připravené newslettery se zajímavým obsahem je způsob, jak čtenáře naučit znovu platit
              za zpravodajství a publicistiku. Cílem naší platformy je být Netflixem v oblasti zpravodajství.
            </p>

            <p>
              Papírové noviny a časopisy jsou věčné. My se snažíme alespoň část jejich kouzla dostat na
              všechny moderní kanály. Distribuujeme newslettery na emaily, RSS čtečky,
              Kindle a jiné ebooky. Máme i moderní desktopovou a mobilní aplikaci.
            </p> -->
        </div>
      </section>

      <ExploreNewspapers>
        <div v-html="$t('Few examples of newsletters <br /> that are published on our platform')" />
      </ExploreNewspapers>

      <section class="microsite--newsletters-are-in">
        <h2>{{ $t('Newsletters are popular') }}</h2>

        <div class="microsite--newsletters-are-in--quotes">
          <blockquote class="quote-lupa">
            <p>
              „Mohli byste namítnout, že e-mail vyšel z módy, ale třeba pro starší diváky
              je to důležitý kanál. Máme velký úspěch s nejrůznějšími newslettery pod
              značkou CNN a neustále přemýšlíme nad tím, jaké další by šly ještě
              připravit,“ tvrdí digitální editor CNN Nick Thomson.
            </p>

            <footer>
              <a href="https://www.lupa.cz/clanky/kdyz-web-a-mobil-nestaci-cnn-v-praze-ukazala-ze-chce-byt-uplne-vsude/" target="_blank">
                <strong>
                  Když web a mobil nestačí. CNN v Praze ukázala, že chce být úplně všude
                </strong>
                — Filip Rožánek, Lupa.cz
              </a>
            </footer>
          </blockquote>

          <blockquote class="quote-finmag">
            <p>
              Vydavatelé už před několika lety pochopili, že závislost na distribuci
              obsahu přes Facebook a Google je časem přivede na mizinu, a tak pro
              podporu čtenosti, zapojení a utužování čtenářské komunity začali
              experimentovat se (staro)novými distribučními platformami včetně
              newsletterů. New York Times v současnosti nabízejí přes 60
              nejrůznějších tematických newsletterů, od denních zpravodajských
              shrnutí přes týdenní specializované newslettery.
            </p>

            <p>
              Podle webu Digiday měly NYT už v roce 2017 přes 13 milionů odběratelů svých
              newsletterů, za tři roky se jejich počet víc než zdvojnásobil. I další
              mediální domy nabízejí obrovské množství newsletterů (jen Washington Post
              jich má přes 70) a vedle nich existuje a stále se rozrůstá mnohem širší a
              zajímavější scéna individuálních newsletterů celebrit, novinářů, umělců,
              nezávislých publicistů i podivínů všeho druhu
            </p>

            <footer>
              <a href="https://finmag.penize.cz/kaleidoskop/410091-rekneme-vam-co-cist-usvit-newsletteru" target="_blank">
                <strong>Řekneme vám, co číst. Úsvit newsletterů</strong>
                — Matouš Hrdina, Finmag
              </a>
            </footer>
          </blockquote>

          <blockquote class="quote-missionorg">
            <p>
              In an age where attention spans are shorter than ever and digital distractions
              have never been more rampant, it may seem strange that a relic from the
              internet’s early years has come back stronger than before but it
              actually makes perfect sense the deeper you look into it.
            </p>

            <footer>
              <a href="https://medium.com/the-mission/how-on-earth-did-email-newsletters-become-popular-again-3fcee1addc7e" target="_blank">
                <strong>How On Earth Did Email Newsletters Become Popular Again?</strong>
                — Richard Bertin, Mission.org
              </a>
            </footer>
          </blockquote>
        </div>

        <div class="microsite--newsletters-are-in--examples">
          <h3>{{ $t('Who for example relies on newsletters?') }}</h3>

          <a href="https://www.nytimes.com/newsletters" target="_blank">
            <img src="~assets/microsite/new-york-times-logo.png" alt="New York Times">
          </a>

          <a href="https://subscribe.washingtonpost.com/newsletters/#/newsletters" target="_blank">
            <img src="~assets/microsite/washington-post-logo.svg" alt="The Washington Post">
          </a>

          <a href="https://edition.cnn.com/email/subscription" target="_blank">
            <img src="~assets/microsite/cnn-logo.png" alt="CNN">
          </a>

          <a href="https://finmag.penize.cz/newsletter" target="_blank">
            <img src="~assets/microsite/finmag-logo.svg" alt="FinMag">
          </a>
        </div>
      </section>

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
        <img src="~assets/profiles/marek-zouzalik.jpg" alt="Marek Zouzalík">
        <strong>Marek Zouzalík</strong>
        <a href="https://www.sncr-praha.cz/" target="_blank">{{ $t('chairman of the Prague Syndicate of Journalists') }}</a>
      </Quote>

      <section class="microsite--newsletter-benefits">
        <!-- <h2>Publikujte s námi moderní newslettery</h2> -->
        <h2>{{ $t('Publish modern newsletters with us') }}</h2>

        <ul>
          <li>
            {{ $t('We can easily connect to your current CMS.') }}
          </li>
          <li>
            {{ $t('We can make newsletters available on your domain. Example. newsletters.yourdomain.com.') }}
          </li>
          <li>
            {{ $t('We can also send newsletters to ebooks, eventually prepare a branded mobile app.') }}
          </li>
          <li>
            {{ $t('With us you can charge newsletters or ask readers for a voluntary contribution to get new income.') }}
          </li>
        </ul>

        <div>
          <button @click="openRequestSolutionModal()">{{ $t('Request solution') }}</button>
          <a href="/downloads/kairly-brozura.pdf" download @click="downloadPDF()">{{ $t('Download PDF brochure') }}</a>
        </div>
      </section>

      <FooterLinks />

      <RequestSolutionModal
        :active.sync="isRequestSolutionModalOpen"
      />
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import Quote from '@/components/microsite/Quote'
import FooterLinks from '@/components/microsite/FooterLinks'
import ExploreNewspapers from '@/components/microsite/ExploreNewspapers'
import RequestSolutionModal from '@/components/modals/RequestSolution'

export default {
  name: 'Publishers',

  auth: false,

  components: {
    AppLayout,
    Quote,
    FooterLinks,
    ExploreNewspapers,
    RequestSolutionModal
  },

  data () {
    return {
      isRequestSolutionModalOpen: false,
    }
  },

  methods: {
    openRequestSolutionModal () {
      this.isRequestSolutionModalOpen = true

      this.$ga.event({
        eventCategory: 'Request for solution form',
        eventAction: 'Publisher'
      })
    },

    downloadPDF () {
      this.$ga.event({
        eventCategory: 'Download PDF brochure',
        eventAction: 'Publisher'
      })
    }
  },

  head () {
    return {
      title: this.$t('Digital Publishing Platform for Publishers') + ' – Kairly',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: this.$t('Kairly is a digital publishing platform for publishers that offers a unique concept of paid content.')
        },
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
      margin-bottom: $baseline

      @media (max-width: $mobile)
        margin: $baseline $baseline/2
        width: 100%

    > p
      margin-bottom: $baseline

      font-size: $fs-3
      line-height: 1.42

      @media (max-width: $mobile)
        padding: 0 $baseline/2

        font-size: $fs-2

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

  picture
    width: 100%

    img
      width: 100%

.journalists--hero--call-to-action
  display: flex
  flex-direction: column
  justify-content: center
  align-self: center

  text-align: center

  button
    +button(primary, large)

  a
    font-size: $fs--1

    color: $c-base

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

//- Newsletter are in
.microsite--newsletters-are-in
  @media (max-width: $mobile)
    margin-top: $baseline

  h2
    +heading

    margin-bottom: $baseline

    @media (max-width: $mobile)
      margin: 0 $baseline/2 $baseline/2 $baseline/2

.microsite--newsletters-are-in--quotes
  display: grid
  align-items: center
  grid-template-columns: 1fr 1fr
  grid-template-rows: auto auto
  grid-column-gap: $baseline
  margin-bottom: $baseline

  @media (max-width: $mobile)
    grid-template-columns: 1fr
    grid-template-rows: auto auto auto
    grid-row-gap: $baseline/2

  > blockquote
    > *
      background: lighten(#EFE1C1, 8%)

    p
      padding: $baseline/2 $baseline/2 0 $baseline/2

      font-family: $ff-serif
      font-size: $fs-0
      line-height: 1.6

    p + p
      padding-top: $baseline

    footer
      padding: $baseline / 2

      color: #555

      line-height: 1.42

      strong
        display: block
        font-weight: 600

      a
        color: #555

  .quote-lupa
    grid-column: 1 / span 1
    grid-row: 1 / span 1

    @media (max-width: $mobile)
      grid-column: 1 / span 1
      grid-row: 1 / span 1

  .quote-finmag
    grid-column: 2 / span 1
    grid-row: 1 / span 2

    @media (max-width: $mobile)
      grid-column: 1 / span 1
      grid-row: 2 / span 1

  .quote-missionorg
    grid-column: 1 / span 1
    grid-row: 2 / span 1

    @media (max-width: $mobile)
      grid-column: 1 / span 1
      grid-row: 3 / span 1

.microsite--newsletters-are-in--examples
  padding-bottom: $baseline

  @media (max-width: $mobile)
    padding: 0 $baseline/2 $baseline/2 $baseline/2

  h3
    margin-bottom: $baseline

    font-size: $fs-2
    font-weight: 600

    @media (max-width: $mobile)
      font-size: $fs-1

  img
    height: 40px
    margin-right: $baseline

.microsite--newsletter-benefits
  border-bottom: 1px solid #eee

  h2
    +heading

    margin-bottom: $baseline

    text-align: center

    @media (max-width: $mobile)
      margin: $baseline/2

  ul
    display: table
    max-width: 480px
    margin: 0 auto $baseline auto

  li
    margin-bottom: $baseline / 2
    margin-left: $baseline
    list-style: disc

    font-size: $fs-1

  > div
    display: table
    margin: 0 auto $baseline auto

    button
      +button(primary, large)

    a
      display: table
      margin: 0 auto

      color: $c-base

      font-size: $fs--1

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
