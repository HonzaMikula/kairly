<template>
  <timeline-welcome>
    <h1>Welcome to Kairly</h1>
    <p>Start with selecting editions you want to subscribe.</p>

    <post-component>
      <header>
        <picture>
          <a href="author/janmikula">
            <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY_400x400.jpeg" alt="Jan Mikula" />
          </a>
        </picture>
      
        <h3>
          <a href="author/janmikula">
            Jan Mikula, Kairly
          </a>  
        </h3>

        <time>
          Today
        </time>
      </header>
      <timeline-post--newspaper>
        <h2>Jak Kairly funguje a jak ho používat?</h2>
        <timeline-post--newspaper--content>
          Praha - Týmy, které za sociální demokracii vyjednávají o programu případné vlády s ANO a podporou komunistů, daly dohromady seznam bodů, ve kterých se s Babišovým hnutím neshodují.

          Rozpory bude příští týden řešit nejužší vedení obou stran. Nejvíce času zřejmě zaberou debaty o daních. ANO je zvyšovat nechce, zatímco sociální demokraté prosazují zavedení sektorové daně.

          Podle předsedy sociální demokracie Jana Hamáčka se programy ČSSD a hnutí ANO nejvíce rozcházejí právě otázce daní. Sociální demokraté by rádi prosadili progresivní zdanění příjmů fyzických osob i firem, sektorové daně nebo dědické daně. Ministryně financí za ANO Alena Schillerová je však striktně proti.

          "Shoda nepanuje v daňových otázkách. My stále trváme na tom, aby byla zavedená sektorová daň. A chceme také jednat o snížení daně z přidané hodnoty na základní potraviny. V sociální oblasti je celá řada nevyjasněných věcí. Nevíme

          přesné důvody, proč chce hnutí ANO oddělovat důchodový účet od státního rozpočtu, a máme spor například v oblasti zálohového výživného, což pokládáme za zásadní věc," jmenoval programové neshody s ANO Hamáček.

          Dořešit se zástupci Babišova hnutí bude muset i zvyšování rodičovských příspěvků nebo přídavků na děti.
        </timeline-post--newspaper--content>  
      </timeline-post--newspaper>
    </post-component>

    <post-component class="tweet">
      <header>
        <picture>
          <a href="author/romankrejcik">
            <img src="https://pbs.twimg.com/profile_images/2334147233/ms3jmf3780crdrujahcm_400x400.jpeg" alt="Jan Mikula" />
          </a>
        </picture>
      
        <h3>
          <a href="author/janmikula">
            Roman Krejčík, Kairly
          </a>  
        </h3>

        <time>
          Today
        </time>
      </header>
      <timeline-post--tweet>
        <p>
          Co chystáme na Kairly v nejbližší době?<br />
          - Každý se bude moci stát editorem a sestavovat vlastní edice.<br />
          - Když sledujete autora, budete si moci nastavit, jak často a kdy budete dostávat souhrn autorových příspěvků.
        </p> 
      </timeline-post--tweet>
    </post-component>

    <timeline-welcome--my-editions>
      <h2>Interesting Edition to Follow</h2>
      <div>
        <MyEditionsItem
          v-for="edition in editions"
          :key="edition.id"
          v-bind:edition="edition"
        />
      </div>
    </timeline-welcome--my-editions>
    

    <timeline-welcome--more-editions>
      <router-link to='/my-editions'>View more editions</router-link>
      <br />
      <!-- TODO remove reload hack, instead trigger timeline load -->
      <button v-on:click="$router.go({ name: '/' })">Show me editions</button>
    </timeline-welcome--more-editions>
  </timeline-welcome>
</template>

<script>
import * as api from '@/api'
import { mapState } from 'vuex'

import MyEditionsItem from '@/components/MyEditionsItem'

export default {
  name: 'Welcome',
  components: {
    MyEditionsItem
  },
  computed: {
    ...mapState({
      editions: state => {
        const editions = Object.values(state.editions)
        if (editions.length > 3) {
          editions.splice(3, editions.length - 3)
        }
        return editions
      }
    })
  },
  created() {
    this.$store.dispatch('getEditions')
  }
}
</script>
