<template>
  <AppLayout>
    <div class="journalists-view">
      <section class="journalists--hero">
        <div>
          <!-- <h1>{{ $t('Are you independent journalist or blogger?') }}</h1> -->
          <h1>Jste čtenáři zpravodajství a publicistiky?</h1>
          <ul>
            <li>Přestaňte bezmyšlenkovitě skrolovat donekonečna. Čtěte jen to, co vás opravdu zajímá.</li>
            <li>Nenechte se otravovat nesmyslnými notifikacemi. Čtětě jen v dobu, kdy chtete a kdy jste na to zvýklí.</li>
            <li>Podpořte kvalitní novináře zakoupením předplatného.</li>
          </ul>

          <!-- <ul>
            <li>{{ $t('Publish on a modern platform that you do not have to maintain.') }}</li>
            <li>{{ $t('Start earning with a unique concept of paid content.') }}</li>
            <li>{{ $t('Become a truly independent author.') }}</li>
          </ul> -->
        </div>
      </section>

      <Faq>
        <img src="~assets/microsite/publishers-1.jpg" alt="Kairly" />
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
          <img src="~assets/microsite/kairly-random-26.jpg" />
        </picture>

        <div>
          <!-- <h2>{{ $t('Publish on a modern platform that you do not have to worry about.') }}</h2> -->
          <h2>Čtěte na platformě, kde je jen obsah, který vás zajímá a nikdo vás tam neruší.</h2>

          <!-- <div v-html="$t('@independent-journalists/modern-platform')">
          </div> -->

          <div>
            <p>
              V dnešní době sociálních sítí a nespočtu aplikací, které se neustále dožadují vaší
              pozornosti, budujeme pro vás místo, kde můžete v klidu číst jen to, co vás zajímá.
            </p>

            <p>
              Nostalgicky vzpomínáme na papírové noviny, kde člověk nemusel donekonečna skrolovat.
              S každým otočením listu papíru dostal čtenář perfektně upravený obsah profesionálním editorem.
              Tohle nám na internetu chybí.
            </p>

            <p>
              Naše unikátní koncepce digitálních novin nabízí čtenářům vysoce personalizovaný obsah, který
              je ale zároveň profesionálně připravený. Naše aplikace nevede k závislosti, ale k vytváření
              prospěšných zvyků při čtení zpravodajství a publicistiky.
            </p>
          </div>
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
          <img src="~assets/microsite/kairly-random-35.jpg" />
        </picture>

        <div>
          <!-- <h2>{{ $t('Start monetizing your content and become a truly independent author.') }}</h2> -->
          <h2>Zakoupením digitálních novin pomáháte dobrým novinářům a publicistům.</h2>

          <!-- <div v-html="$t('@independent-journalists/monetizing-content')"></div> -->

          <div>
            <p>
              Reklama kvalitní novináře nezaplatí. Pokud budou novináři závislí převážně na reklamě,
              budou psát obsah, kterému jde především o počet prokliků. Nám jde o kvalitní obsah,
              proto se u nás za něj platí.
            </p>

            <p>
              Zakoupením předplatného digitálních novin podporujete editory, u kterých si ceníte
              jejich výběru článků a tweetů. Podporujete ale i autory, které se ve vámi předplacených
              novinách objevují.
            </p>

            <p>
              Vaše oblíbené autory, think-tanky či neziskové organizace můžete podpořit nad rámec
              běžného předplatného.
            </p>
          </div>
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

      <OfficialStart />

      <Footer />

      <FooterLinks />

    </div>
  </AppLayout>
</template>

<script>
import { mapState } from 'vuex'
import AppLayout from '@/components/layout/AppLayout'
import Quote from '@/components/microsite/Quote'
import HowItWorks from '@/components/microsite/HowItWorks'
import Footer from '@/components/microsite/Footer'
import FooterLinks from '@/components/microsite/FooterLinks'
import OfficialStart from '@/components/microsite/OfficialStart'
import Faq from '@/components/microsite/Faq'

export default {
  name: 'Readers',

  auth: false,

  components: {
    AppLayout,
    Quote,
    HowItWorks,
    OfficialStart,
    Footer,
    FooterLinks,
    Faq
  },

  head() {
    return {
      title: this.$t('Media platform for readers') +' – Kairly',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: this.$t('Kairly is a media platform for pleasant reading without distraction and endless scrolling.') },
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
  flex-direction: column
  justify-content: center
  height: 400px
  margin-bottom: $baseline * 2
  max-width: none

  background-size: cover
  background: #f5f5f5

  @media (max-width: 950px)
    margin-bottom: 0

  @media (max-width: $mobile)
    height: auto
    padding-bottom: $baseline / 2

  h1
    +heading
    padding: $baseline/2
    margin-bottom: $baseline * 2

    text-align: center

    @media (max-width: $mobile)
      margin: $baseline 0


  ul
    padding: 0 $baseline

    counter-reset: benefits

    @media (max-width: $mobile)
      padding: 0 $baseline/2

  li
    display: flex
    align-items: center
    margin-bottom: $baseline / 2

    font-size: $fs-2

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