<template>
  <div class="homepage-view">

    <section class="homepage--cover">
      <div>
        <h1>
          {{ $t('Read only what you care about.') }}
        </h1>

        <!-- Begin Mailchimp Signup Form -->
        <div id="mc_embed_signup">
          <form action="https://honzamikula.us8.list-manage.com/subscribe/post?u=0aa8c0b091d21d477832fbe62&amp;id=7c7468a76d" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
            <div id="mc_embed_signup_scroll">
              <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" placeholder="email address" required>
              <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
              <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_0aa8c0b091d21d477832fbe62_7c7468a76d" tabindex="-1" value=""></div>
              <div class="clear"><input type="submit" :value="$t('Request to join')" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
            </div>
          </form>
        </div>
        <!--End mc_embed_signup-->
        <p>{{ $t('Currently Kairly is in a private beta version.') }}</p>
      </div>
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
          <strong>Nezávislost a objektivita vzníká v otevřeném a férovém prostředí</strong>.
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
        <div v-html="$t('@homepage/quote/honza')"></div>
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
          <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY_400x400.jpeg" alt="Jan Mikula" />
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
        <div v-html="$t('@homepage/quote/roman')"></div>
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
          <img src="https://pbs.twimg.com/profile_images/2334147233/ms3jmf3780crdrujahcm_400x400.jpeg" alt="Roman Krejčík" />
          <strong>Roman Krejčík</strong> {{ $t('founder of Kairly') }}
        </footer>
      </blockquote>
    </section>

    <section class="homepage--newspapers">
      <h2>{{ $t('Check out some of our newspapers.') }}</h2>

      <div>
        <NewspaperWidget
          v-for="newspaper in newspapers"
          :key="newspaper.fullName"
          :newspaper="newspaper"
        />
      </div>
    </section>

    <section class="homepage--quote">
      <h2>{{ $t('Was said about us.') }}</h2>

      <blockquote>
        <div v-html="$t('@homepage/quote/zouzalik')"></div>
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
          <img src="https://pbs.twimg.com/profile_images/762976177535475712/JfzxZ0RA_400x400.jpg" alt="Marek Zouzalík" />
          <strong>Marek Zouzalík</strong> <a href="https://www.sncr-praha.cz/" target="_blank">{{ $t('chairman of the Prague Syndicate of Journalists') }}</a>
        </footer>
      </blockquote>
    </section>

    <section class="homepage--howitworks">
      <h2>{{ $t('How the platform works?') }}</h2>

      <picture>
        <img src="~assets/homepage/kairly-howitworks.jpg" width="1200" height="848" />
      </picture>
    </section>

    <footer class="homepage--footer">
      <div>
        <h2><nuxt-link to="/">Kairly</nuxt-link></h2>

        <p>{{ $t('Read only what you care about.') }}</p>

        <div class="homepage--footer--social-media">
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

        <div class="homepage--footer--languages">
          <a
            href="?lang=cs"
            @click.prevent="setLang('cs')"
            :class="{'is-active': currentLocale == 'cs'}">
            Česky
          </a>

          <a
            href="?lang=en"
            @click.prevent="setLang('en')"
            :class="{'is-active': currentLocale == 'en'}">
            English
          </a>
        </div>
      </div>

    </footer>

    <portal to="modal" v-if="isJoinUsModalOpen">
      <JoinUsModal :closeModal="closeJoinUs"></JoinUsModal>
    </portal>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import store from '@/store'
import JoinUsModal from '@/components/modals/JoinUs'
import NewspaperWidget from '@/components/widgets/NewspaperWidget'


export default {
  name: 'Homepage',

  components: {
    JoinUsModal,
    NewspaperWidget
  },

  head() {
    return {
      title: this.$t('Kairly – Read only what you care about'),
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
      isJoinUsModalOpen: null,
      newspapers: null
    }
  },

  computed: {
    ...mapState({
      currentLocale: state => state.locale || 'en'
    }),
  },

  async created() {
    const newspapersToShow = [
        'janmikula/malostranskenoviny',
        'farin/nej-novinari-na-twitteru',
        'janmikula/technologicky-denik'
      ]
    this.newspapers = await this.$store.dispatch('getNewspapers', newspapersToShow)
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
    },

    setLang(locale) {
      this.setLocale(locale)
      this.$auth.$storage.setUniversal('locale', locale)
    }
  },

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
  height: 400px
  margin-bottom: $baseline * 2
  max-width: none

  //background: url("~assets/homepage/hero-new.jpg") bottom center no-repeat
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

    @media (max-width: $mobile)
      margin: $baseline 0


  p
    font-size: $fs-0
    text-align: center

  //- Mailchimp
  #mc_embed_signup
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


//- Image how it works
.homepage--howitworks
  margin-bottom: $baseline * 2

  @media (max-width: 950px)
    padding: $baseline $baseline 0 $baseline

  @media (max-width: $mobile)
    padding: $baseline $baseline/2
    margin-bottom: 0

  h2
    +heading

    margin-bottom: $baseline

  picture
    display: block
    margin: 0 (-$baseline*2)

    @media (max-width: 1050px)
      margin: 0

    @media (max-width: $mobile)
      margin: 0

  img
    width: 100%


//- Footer
.homepage--footer
  position: relative

  display: flex
  align-items: center
  justify-content: center
  height: 400px
  max-width: none

  background: url("~assets/homepage/hero-new.jpg") bottom center no-repeat
  background-size: cover

  color: #fff

  font-family: $ff-serif
  text-align: center

  h2
    display: table
    padding: 0 $baseline/2
    margin: 0 auto
    margin-bottom: $baseline

    background: #fff
    color: #000
    text-shadow: 0 0 3px #fff

    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: left

    @media (max-width: $mobile)
      font-size: $fs-3
      line-height: $baseline * 1.5

    a
      color: #000

  p
    display: table
    padding: 0 $baseline/2
    margin: 0 auto
    margin-bottom: $baseline

    background: #fff
    color: #000
    text-shadow: 0 0 3px #fff

    font-size: $fs-2
    font-weight: 600
    line-height: $baseline * 1.5

//- Social media links
.homepage--footer--social-media
  display: flex
  justify-content: center

  a
    border-radius: 100%
    display: inline-block
    height: $baseline * 1.5
    margin: 0 $baseline/2
    width: $baseline * 1.5

    background: #fff
    color: #555

    font-size: $fs-3
    line-height: $baseline * 1.5
    text-align: center

    transition: 0.15s all

    &:focus,
    &:hover
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


//- Social media links
.homepage--footer--languages
  display: flex
  justify-content: center
  margin-top: $baseline

  a
    +button

    margin: 0 $baseline/4

    background: rgba(255, 255, 255, 0.5)
    color: #000

    &:hover,
    &:focus
      background: #fff

</style>
