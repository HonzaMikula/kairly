<template>
  <component
    :is="componentName"
    :key="issue.id"
    :issue="issue"
    :hideDate="hideDate">

    <template slot="newspaperTitle">
      <slot name="newspaperTitle"/>
    </template>

    <section>
      <PostWrapper
        :post="headPosts[0]"
        :isSubscribed="true"
      />

      <article role="article" class="post newspaper editorial">
        <header>
          <picture>
            <a href="/janmikula" class="">
              <img src="https://cdn.kairly.com/media/users/janmikula.jpg" alt="Dojnice">
            </a>
          </picture>
          <h3>
            <a href="/janmikula" class="">Jan Mikula, editor</a>
          </h3>
          </header>
          <timeline-post--article>
            <h2>Nebezpečný Babiš</h2>
            <timeline-post--article--content>
              <img src="http://cdn.xsd.cz/resize/e884c16700743e3cb6718cbd0f7c113e_extract=91,0,1959,1102_resize=640,360_.jpg?hash=c688b6b5977eaee434011a70e0afe8a3"/>
              <p>Všichni tady lamentujeme nad Babišem a jeho nejrůznějšími nekalými dotačními praktiky. Co se takhle spojit?</p>

              <p>Ne, proti Babišovi. Ale proti dotacím, ať už na evropské či národní úrovni. Zrušme je.</p>
              
            </timeline-post--article--content>
          </timeline-post--article>
        </article>
    </section>

    <section>
      <PostWrapper
        :post="headPosts[1]"
        :isSubscribed="true"
      />

      <article role="article" class="post newspaper editorial">
        <header>
          <picture>
            <a href="/janmikula" class="">
              <img src="https://cdn.kairly.com/media/users/janmikula.jpg" alt="Dojnice">
            </a>
          </picture>
          <h3>
            <a href="/janmikula" class="">Jan Mikula, editor</a>
          </h3>
          </header>
          <timeline-post--article>
            <h2>Nebezpečný Babiš</h2>
            <timeline-post--article--content>
              <p>Všichni tady lamentujeme nad Babišem a jeho nejrůznějšími nekalými dotačními praktiky. Co se takhle spojit?</p>

              <p>Ne, proti Babišovi. Ale proti dotacím, ať už na evropské či národní úrovni. Zrušme je. Zrušme tohle prostředí, kde úspěch podnikatele se měří schopností čerpat dotace.</p>
              <p>Vytvořit ekonomické spojení mezi státem a velkým byznysem je ale, jak vidíme, až absurdně snadné.</p>
            </timeline-post--article--content>
          </timeline-post--article>
        </article>
    </section>

    <PostWrapper
        :post="headPosts[2]"
        :isSubscribed="true"
      />
    
    <section>
      <article role="article" class="post newspaper">
        <header><picture><a href="/rozhlas" class="nuxt-link-exact-active nuxt-link-active"><img src="https://cdn.kairly.com/media/users/rozhlas.jpg" alt="Rozhlas.cz"></a></picture> <h3><a href="/rozhlas" class="nuxt-link-exact-active nuxt-link-active">
                  Rozhlas.cz<!----></a></h3> <!----> <time>Jul 4</time> <section> <span><button role="button" tabindex="0" aria-label="Consider for newspaper" title="" class="consider-post" data-original-title="Consider for newspaper"></button> <!----></span></section></header> 
                  <timeline-post--article>
                    <h2><a href="/rozhlas/zive-schuzka-zadne-reseni-neprinesla-rekl-hamacek-po-schuzce--0eed89136" class="">ŽIVĚ: Schůzka žádné řešení nepřinesla, řekl Hamáček po schůzce se Zemanem a Babišem</a></h2> 
                    <timeline-post--article--content><div><figure><p><a href="//www.irozhlas.cz/fotogalerie/7976231?fid=8905537">
        <img src="https://www.irozhlas.cz/sites/default/files/styles/zpravy_otvirak_velky/public/uploader/zuzana_caputova_2_190621-000051_mda.jpg?itok=Yt0z6J5M" alt=""></a>
        </p><figcaption>Prezident Miloš Zeman | Foto: Michaela Danelová | Zdroj: iROZHLAS.cz </figcaption></figure><p>Prezident Miloš Zeman se dosud definitivně nevyjádřil k nominaci Michala Šmardy (ČSSD) na ministra kultury. Po schůzce s hlavou státu a předsedou ČSSD a ministrem vnitra Janem Hamáčkem to řekl premiér Andrej Babiš. Podle něj proběhne další schůzka 12. července, jak bylo dříve avizováno.</p><p>Situace je podle Hamáčka závažná. Musí rozhodnout předsednictvo strany. „Jsem připraven ho (předsednictvo) svolat v nejbližší době,“ řekl Hamáček novinářům.</p><p>Schůze předsednictva by se podle něj mohla konat kolem 15. července. „Uvidíme, jak dopadne ta schůzka 12., ale nejsem velký optimista,“ dodal Hamáček.</p><p>Zeman se měl sejít s&nbsp;představiteli obou vládních stran v&nbsp;úterý večer. Kvůli summitu Evropské unie, na kterém čelní představitelé státu vybírali nového předsedu Evropské komise, byla ale schůzka přesunuta právě na čtvrteční poledne.</p></div> <timeline-post--continue-reading><div><a href="/rozhlas/zive-schuzka-zadne-reseni-neprinesla-rekl-hamacek-po-schuzce--0eed89136#continue" class="">
                      Continue reading
                    </a></div>
                  (1 min read)
                </timeline-post--continue-reading></timeline-post--article--content></timeline-post--article>
      </article>

      <article role="article" class="post tweet editorial"><header><picture><a href="/jindrichsidlo" class="nuxt-link-exact-active nuxt-link-active"><img src="https://cdn.kairly.com/media/users/jindrichsidlo.jpg" alt="Jindřich Šídlo"></a></picture> <h3><a href="/jindrichsidlo" class="nuxt-link-exact-active nuxt-link-active">
          Jindřich Šídlo<span>, Zprávy Seznam.cz</span></a></h3> <!----> <time>Jul 4</time></header> <timeline-post--tweet><div class="tweet-content">Omlouvám se Stanislavu Grossovi, tak slabý premiér nebyl ani on.</div> <!----></timeline-post--tweet>   </article>

      <article role="article" class="post tweet editorial"><header><picture><a href="/eriktabery" class="nuxt-link-exact-active nuxt-link-active"><img src="https://cdn.kairly.com/media/users/eriktabery.jpg" alt="Erik Tabery"></a></picture> <h3><a href="/eriktabery" class="nuxt-link-exact-active nuxt-link-active">
          Erik Tabery<span>, Respekt</span></a></h3> <!----> <time>Jul 4</time> </header> <timeline-post--tweet><div class="tweet-content">Tohle není dobrý týden pro <a href="https://twitter.com/AndrejBabis" title="Andrej Babiš">@AndrejBabis</a>. Nejdříve vše projede v Bruselu, kde sám sebe (a celou zemi) pošle do autu. Poradil mu to totiž Orbán. A následně se potvrdí, že nemá vliv na svou vlastní vládu, protože mu Zeman více méně řekl: Uhni, chlapče, tohle kolo tančím já.</div> <!----></timeline-post--tweet>   </article>
    
      <article role="article" class="post tweet editorial"><header><picture><a href="/karelschwarzenberg" class="nuxt-link-exact-active nuxt-link-active"><img src="https://cdn.kairly.com/media/users/karelschwarzenberg.jpg" alt="Karel Schwarzenberg"></a></picture> <h3><a href="/karelschwarzenberg" class="nuxt-link-exact-active nuxt-link-active">
          Karel Schwarzenberg<span>, falešný kníže</span></a></h3> <!----> <time>Jul 4</time></header> <timeline-post--tweet><div class="tweet-content">Při posledním setkáním se Zemanem jsem mu daroval Ústavu. Štítivě ji odhodil do koše.</div> <!----></timeline-post--tweet>   </article>
    </section>

    <footer class="issue--footer">
      <div class="issue--footer--show-more">
        <button
          v-if="(tailPostsCount > 0 && !expanded)"
          @click.prevent="expandIssue">
          {{ $t('Show more') }} ({{tailPostsCount}})
        </button>
      </div>

      <div class="issue--footer--recommend-button">
        <RecommendButtonIssue
          v-if="loggedIn && issue.type == 'newspaper'"
          :issue="issue"
        />
      </div>
    </footer>
  </component>
</template>

<script>
import { mapState } from 'vuex'

import IssueSuspendedAuthor from '@/components/issues/IssueSuspendedAuthor'
import IssueSuspendedNewspaper from '@/components/issues/IssueSuspendedNewspaper'
import IssueUnreleasedNewspaper from '@/components/issues/IssueUnreleasedNewspaper'
import IssueNewspaper from '@/components/issues/IssueNewspaperBeta'
import IssueAuthor from '@/components/issues/IssueAuthor'
import PostWrapper from '@/components/PostWrapper'
import RecommendButtonIssue from '@/components/widgets/RecommendButtonIssue'

const POST_LIMIT = 5

export default {
  name: 'IssueWrapperBeta',

  props: {
    issue: Object,
    subscription: Boolean,
    hideDate: Boolean,
    showTail: Boolean
  },

  components: {
    IssueAuthor,
    IssueNewspaper,
    IssueSuspendedAuthor,
    IssueSuspendedNewspaper,
    IssueUnreleasedNewspaper,
    PostWrapper,
    RecommendButtonIssue
  },

  data() {
    return {
      showAllPosts: false
    }
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn
    }),

    componentName() {
      return 'issue-' + this.issue.type
    },

    expanded() {
      if (this.showTail) {
        return true
      }
      else {
        return !!this.$store.state.timelineExpandedIssues[this.issue.id]
      }
    },

    headPosts() {
      return this.issue.posts.slice(0, POST_LIMIT)
    },

    tailPosts() {
      return this.expanded ? this.issue.posts.slice(POST_LIMIT) : []
    },

    tailPostsCount() {
      return Math.max(0, this.issue.posts.length - POST_LIMIT)
    }

  },

  methods: {
    expandIssue() {
      this.$store.dispatch('expandIssue', this.issue.id)
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- Beta
timeline-newspaper
  > section
    display: grid
    grid-template-columns: 1fr 1fr 1fr
    border: 1px solid #eee
    margin-bottom: $baseline / 2

    &:nth-of-type(1)
      article:nth-of-type(1)
        grid-column: 2 / span 2
        grid-row: 1 / span 1
        margin: 0

        timeline-post--article--content
          column-count: 2

      article:nth-of-type(2)
        grid-column: 1 / span 1
        grid-row: 1 / span 1
        margin: 0

    &:nth-of-type(2)
      article:nth-of-type(1)
        grid-column: 1 / span 2
        grid-row: 1 / span 1
        margin: 0

        timeline-post--article--content
          column-count: 2
      article:nth-of-type(2)
        margin: 0

    &:nth-of-type(3)
      article:nth-of-type(1)
        grid-column: 1 / span 2
        grid-row: 1 / span 3
        margin: 0

        timeline-post--article--content
          column-count: 2

      article:nth-of-type(2)
        grid-column: 3 / span 1
        grid-row: 1 / span 1
        margin-bottom: 0

      article:nth-of-type(3)
        grid-column: 3 / span 1
        grid-row: 2 / span 1
        margin-bottom: 0

      article:nth-of-type(4)
        grid-column: 3 / span 1
        grid-row: 3 / span 1
        margin: 0
        
      
.editorial
  background: #f5f5f5

  timeline-post--article--content
    column-count: 1

.editorial-2
  background: #f5f5f5
  margin-bottom: (-$baseline/2)
  padding-bottom: $baseline

  
//- Newspaper
timeline-newspaper
  display: block
  margin: $baseline*2 0 $baseline

  > header
    margin-bottom: $baseline

    font-family: $ff-serif
    text-align: center

    h1
      margin-bottom: $baseline / 4

      font-size: $fs-2
      line-height: $baseline * 1.25

      img
        float: left
        height: $baseline * 1.25
        margin-right: $baseline / 4
        width: $baseline * 1.25

      a
        display: inline-block

        color: #000

    img
      border-radius: 100%
      height: $baseline
      width: $baseline

      object-fit: cover
      vertical-align: bottom

    p
      font-size: $fs-0

      color: #999

      a
        color: #999

      @media (max-width: $mobile)
        span
          display: none

//- Footer
.issue--footer
  display: flex
  justify-content: center

  > div
    margin: 0 $baseline/4

//- show more button
.issue--footer--show-more button
  +button

//- Issue
.issue-footer
  text-align: center

  button
    display: inline-block
    border-radius: $baseline * 0.7
    height: $baseline * 1.25
    padding: 0 $baseline/2

    background: transparent
    border: 1px solid #ddd
    color: #555

    font-size: $fs-0
    font-family: $ff-sans
    line-height: $baseline * 1.25

    cursor: pointer

    &:hover,
    &:focus
      border: 1px solid $c-base
      color: $c-base


</style>
