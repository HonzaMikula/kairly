<template>
  <div class="homepage-view">

    <section class="homepage--cover">
      <div>
        <h1>
          Sociální sítě máme na zábavu.<br />
          Na zpravodajství je tu Kairly.
        </h1>
      </div>
    </section>

    <section class="homepage--image">

    </section>

    <section class="homepage--readers">
      <picture>
        <img src="~assets/homepage/kairly-1.jpg" />
      </picture>

      <div>
        <h2>Odebírejte digitální noviny informující o tématech, které vás zajímají.</h2>

        <p>
          <strong>Editoři vybírají nejlepší články a tweety</strong> napříč všemi autory publikujícími na Kairly.
          Pravidelně budete dostávat (například každý den v 9:00) ten nejlepší obsah na dané téma.
        </p>

        <p>
          <strong>Editorem se může stát každý</strong>. Záleží pouze na tom, zda editor dokáže připravovat kvalitní vydání novin.
          <strong>Nezávislost a objektivita vzníká v otevřeném a férovém prostředí</strong>.
        </p>

        <p>
          Na Kairly nejsou žádné reklamy. Nesledujeme vás.
          Nesloužíme žádným byznysovým ani politickým zájmům.
          Za noviny se vždy platilo a <strong>zakoupením předplatného novin si kupujete kvalitní a nezávislý obsah</strong>.
        </p>
      </div>
    </section>

    <section class="homepage--quote">
      <blockquote>
        <p>
          "Sociální sítě se nás snaží přehltit zábavným či šokujícím obsahem, aby vydělali co nejvíce na reklamě.
          To není místo pro zpravodajství, které má být věcné a pravdivé. Kairly děláme pro lidi,
          kteří chtějí být skutečně informovaní a chtějí stimulovat své kritické uvažování.
        </p>

        <p>
          Na Kairly neotravujeme žádnými notifikacemi, nesnažíme se vám neustále podstrčit nový
          rádoby zajímavý obsah. Pravidelně a vždy ve stejný čas zobrazujeme jen ten obsah,
          který jste si objednal a to od lidí, kterým věříte a kteří vás skutečně intelektuálně obohacují."
        </p>

        <footer>
          <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY_400x400.jpeg" alt="Jan Mikula" />
          <strong>Jan Mikula</strong>, zakladatel Kairly
        </footer>
      </blockquote>
    </section>

    <section class="homepage--readers">
      <picture>
        <img src="~assets/homepage/kairly-3.jpg" />
      </picture>

      <div>
        <h2>Jste novinář? Začnete vydělávat publikováním obsahu nebo jako editor novin</h2>

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
      </div>
    </section>

    <section class="homepage--quote">
      <blockquote>
        <p>
          "O placeném obsahu se mluví už roky, ale současné modely pay-wallů zatím úspěchy příliš nesklízejí.
          Novináři jsou stále závislí na reklamním monopolu Googlu a Facebooku. Výsledkem je neustále snižování
          stavů redakcí a omezování nákladů. Čas na kvalitní novinářskou práci v podstatě není.
        </p>

        <p>
          Náš koncept placeného obsahu jde mnohem dál než obyčejný pay-wall. Využíváme principů absolutní otevřenosti
          a síťového efektu, kterými si nás před lety získaly sociální sítě. Právě proto věříme, že právě Kairly přináší
          vysněný fungující model placeného obsahu na internetu."
        </p>

        <footer>
          <img src="https://pbs.twimg.com/profile_images/2334147233/ms3jmf3780crdrujahcm_400x400.jpeg" alt="Roman Krejčík" />
          <strong>Roman Krejčík</strong>, zakladatel Kairly
        </footer>
      </blockquote>
    </section>

    <section class="homepage--newspapers">
      <h2>Prohlédněte si poslední vydání novin.</h2>

      <img src="~assets/homepage/kairly-4.jpg" />
    </section>

    <section class="homepage--quote">
      <h2>Řekli o nás.</h2>

      <blockquote>
        <p>
          "Nowadays, when attacks on journalists, including physical ones, are increasing, we need to find a
          sustainable economic model for journalism. Only in this way can we keep independent journalism on
          politicians and large private corporations. And only in this way we can resist the phenomena of fake
          news and ensure that the complete freedom of speech is preserved.
        </p>

        <p>
          Kairly comes up with an interesting concept of paid content on the internet, which is significantly
          different from the current not very successful attempts. "
        </p>

        <footer>
          <img src="https://pbs.twimg.com/profile_images/762976177535475712/JfzxZ0RA_400x400.jpg" alt="Roman Krejčík" />
          <strong>Marek Zouzalík</strong>, prezident Syndikátu novinářů Prahy a Středočeského kraje
        </footer>
      </blockquote>
    </section>

    <portal to="modal" v-if="isJoinUsModalOpen">
      <JoinUsModal :closeModal="closeJoinUs"></JoinUsModal>
    </portal>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import store from '@/store'
import JoinUsModal from '@/components/modals/JoinUs'

export default {
  name: 'Homepage',

  components: {
    JoinUsModal
  },

  head() {
    return {
      title: this.$t('Kairly – We aim for exceptional journalism'),
      meta: [
        { hid: 'description', name: 'description', content: this.$t('Kairly is new platform that wants to create better environment for journalist and readers.') },
      ]
    }
  },

  data() {
    return {
      invalidCredentials: false,
      username: null,
      password: null,
      isJoinUsModalOpen: null
    }
  },

  computed: mapState({
    currentLocale: state => state.locale || 'en'
  }),

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
    },

    setLang(locale) {
      this.setLocale(locale)
      this.$auth.$storage.setUniversal('locale', locale)
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.homepage-view
  padding-top: $baseline

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
  height: 300px
  margin-bottom: $baseline * 2

  //background: url("~assets/homepage/hero-new.jpg") bottom center no-repeat
  background-size: cover

  h1

    padding: $baseline/2 $baseline

    background: #fafafa

    font-size: 36px
    font-weight: 900
    line-height: $baseline * 2

//- Image
.homepage--image
  display: none

  height: 400px

  background: url("~assets/homepage/hero-new.jpg") bottom center no-repeat
  background-size: cover


//- Readers
.homepage--readers
  display: grid
  grid-template-areas: "hp-readers-picture hp-readers-text"
  grid-template-columns: 330px 540px
  grid-column-gap: $baseline
  padding: $baseline*2 0
  margin-bottom: $baseline * 2

  > picture
    grid-area: hp-readers-picture

    img
      height: 100%
      width: 100%

      object-fit: cover

  > div
    grid-area: hp-readers-text

    h2
      margin-bottom: $baseline
      font-size: 36px
      font-weight: 900
      line-height: $baseline * 2

    p
      position: relative

      margin-bottom: $baseline
      padding-left: $baseline
      max-width: 600px

      font-size: 18px

      &::before
        position: absolute
        left: 0

        width: $baseline

        font-size: $fs-3
        text-align: center

        content: '•'


.homepage--quote
  padding: $baseline*2
  margin-bottom: $baseline * 2

  background: #fafafa

  h2
    margin-bottom: $baseline

    font-size: 36px
    font-weight: 900
    line-height: $baseline * 2

  blockquote

    p
      margin-bottom: $baseline

      font-size: $fs-2

    footer
      display: flex

      font-size: $fs-1
      line-height: $baseline * 1.5

      img
        margin-right: $baseline / 2
        border-radius: 100%
        height: $baseline * 1.5
        width: $baseline * 1.5

.homepage--newspapers
  margin-bottom: $baseline * 2

  h2
    margin-bottom: $baseline

    font-size: 36px
    font-weight: 900
    line-height: $baseline * 2

</style>
