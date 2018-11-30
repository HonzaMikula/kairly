<template>
  <timeline-welcome>
    <div class="welcome-view">
      <h1>Welcome to Kairly!</h1>

      <section class="welcome--topics">
        <h2>1) In which topic are you interested in?</h2>

        <ul>
          <li v-for="topic in topics" :key="topic">
            <a href="" @click.stop.prevent="chooseTopic(topic)" :class="{'is-active': chosenTopic == topic}">{{ topic }}</a>
          </li>
        </ul>
      </section>

      <section class="welcome--newspapers" v-if="chosenTopic != null">
        <h2>2) Subscribe to newspapers</h2>
        <div>
          <NewspaperWidget
            v-for="newspaper in newspapers"
            :key="newspaper.fullName"
            :newspaper="newspaper"
          />

          <NewspaperWidget
            v-for="newspaper in newspapers2"
            :key="newspaper.fullName"
            :newspaper="newspaper"
          />
        </div>
      </section>

      <section class="welcome--roles" v-if="chosenTopic != null">
        <h2>3) Start using Kairly</h2>
        <div>
          <section>
            <h3>As a reader</h3>
            <p>
              Are you interested in more newspapers and authors?
            </p>
            <p><a href="">Explore more content</a></p>
          </section>

          <section>
            <h3>As an editor</h3>
            <p>
              Do you want to start a newspaper and pick the best content for others?
            </p>

            <p><a href="">Start a newspaper</a></p>
          </section>

          <section>
            <h3>As an author</h3>
            <p>
              Do you want to start writing articles and tweets?
            </p>

            <p><a href="">Write a new post</a></p>
          </section>
        </div>

        <a href="">Go Home to start reading</a>
      </section>

    </div>
  </timeline-welcome>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import NewspaperWidget from '@/components/widgets/NewspaperWidget'

export default {
  name: 'Welcome',

  components: {
    NewspaperWidget
  },

  data() {
    return {
      topics: ['News', 'Politics', 'Sport', 'Technology', 'Life'],
      chosenTopic: null,
      newspapers: [ { "name": "malostranskenoviny", "fullName": "janmikula/malostranskenoviny", "title": "Malostranské noviny", "picture": "https://cdn.kairly.com/media/editions/malostranskenoviny.jpg", "description": "Přehled toho nejzajímavějšího, co se událo v české politice.", "editor": { "id": "janmikula", "name": "Jan Mikula", "picture": "https://cdn.kairly.com/media/users/janmikula.jpg", "kind": "personal", "medium": "Kairly", "bio": "Přemýšlím, jak nastartovat kvalitní žurnalistiku. Proto se po večerech lopotím na Kairly. " }, "periodicity": { "frequency": "daily", "dow": null, "time": "09:00" }, "nextRelease": "2018-11-30T09:00:00+01:00", "issues": 126, "likes": 13 }, { "name": "domaci", "fullName": "aktualnecz/domaci", "title": "Deník Aktuálně – Domácí", "picture": "https://cdn.kairly.com/media/editions/aktualnecz_uQ4fenH.jpg", "description": "(automaticky generované noviny)", "editor": { "id": "aktualnecz", "name": "Aktuálně.cz", "picture": "https://cdn.kairly.com/media/users/aktualnecz.png", "kind": "medium", "medium": "", "bio": "Aktuálně.cz - kompletní zpravodajství, zprávy z domova i ze světa." }, "periodicity": { "frequency": "3x_per_day", "dow": null, "time": null }, "nextRelease": "2018-11-30T12:00:00+01:00", "issues": 1151, "likes": 5 }, { "name": "technologicky-denik", "fullName": "janmikula/technologicky-denik", "title": "Technologický deník", "picture": "https://cdn.kairly.com/media/editions/janmikula-technologicky-denik.jpg", "description": "Přinášíme přehled technologických a vědeckých novinek. Zajímáme se o novinky v oblasti mobilních zařízení, chytré elektroniky, počítačů a dalšího hardwaru.", "editor": { "id": "janmikula", "name": "Jan Mikula", "picture": "https://cdn.kairly.com/media/users/janmikula.jpg", "kind": "personal", "medium": "Kairly", "bio": "Přemýšlím, jak nastartovat kvalitní žurnalistiku. Proto se po večerech lopotím na Kairly. " }, "periodicity": { "frequency": "daily", "dow": null, "time": "09:00" }, "nextRelease": "2018-11-30T09:00:00+01:00", "issues": 102, "likes": 13 } ],
      newspapers2: [ { "name": "sport", "fullName": "aktualnecz/sport", "title": "Deník Aktuálně – Sport", "picture": "https://cdn.kairly.com/media/editions/aktualnecz_ivSYA8r.jpg", "description": "(automaticky generované noviny)", "editor": { "id": "aktualnecz", "name": "Aktuálně.cz", "picture": "https://cdn.kairly.com/media/users/aktualnecz.png", "kind": "medium", "medium": "", "bio": "Aktuálně.cz - kompletní zpravodajství, zprávy z domova i ze světa." }, "periodicity": { "frequency": "3x_per_day", "dow": null, "time": null }, "nextRelease": "2018-11-30T12:00:00+01:00", "issues": 657, "likes": 0 }, { "name": "sport", "fullName": "rozhlas/sport", "title": "iRozhlas – Sport", "picture": "https://cdn.kairly.com/media/editions/irozhlas_N9P7Ryw.jpg", "description": "(automaticky generované noviny)", "editor": { "id": "rozhlas", "name": "Rozhlas.cz", "picture": "https://cdn.kairly.com/media/users/rozhlas.jpg", "kind": "medium", "medium": "", "bio": "Spolehlivé zprávy Českého rozhlasu na internetu." }, "periodicity": { "frequency": "3x_per_day", "dow": null, "time": null }, "nextRelease": "2018-11-30T12:00:00+01:00", "issues": 367, "likes": 0 }, { "name": "sport", "fullName": "idnescz/sport", "title": "MF Dnes – Sport", "picture": "https://cdn.kairly.com/media/editions/mfdnes_Sjkjs4p.jpg", "description": "(automaticky generované noviny)", "editor": { "id": "idnescz", "name": "iDnes.cz", "picture": "https://cdn.kairly.com/media/users/idnescz.jpg", "kind": "medium", "medium": "", "bio": "Nejnovější zprávy z vašeho kraje, České republiky a celého světa." }, "periodicity": { "frequency": "3x_per_day", "dow": null, "time": null }, "nextRelease": "2018-11-30T12:00:00+01:00", "issues": 391, "likes": 0 } ]
    }
  },

  methods: {
    chooseTopic(topic) {
      this.chosenTopic = topic

      console.log(this.newspapers)
    }
  },
}
</script>

<style lang="sass">
//- Welcome view
.welcome-view
  display: block

  //- Welcome heading
  > h1
    margin-bottom: $baseline

    font-family: $ff-serif
    font-size: $fs-4
    font-weight: 600
    line-height: $baseline * 2
    text-align: center

  //- Sections
  > section
    margin-bottom: $baseline * 2

    > h2
      margin-bottom: $baseline

      font-family: $ff-serif
      font-size: $fs-2
      font-weight: 600
      text-align: center


//- Topics
.welcome--topics

  ul
    display: flex
    justify-content: center
    margin-bottom: $baseline * 2

  li
    margin-right: $baseline / 2

  a
    display: block
    border-radius: 5px
    padding: 0 $baseline/2

    background: #eee
    color: #000

    line-height: $baseline * 1.5

    &:hover,
    &:focus
      background: #ddd

    &.is-active
      background: #d5d5d5

//- Newspapers
.welcome--newspapers

  > div
    display: grid
    grid-row-gap: $baseline
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2

    @media (max-width: $mobile)
      grid-column-gap: $baseline / 4
      overflow-x: auto

      newspaper-widget-view
        min-width: 200px


//- Roles
.welcome--roles

  > div
    display: flex
    margin-bottom: $baseline * 2

    @media (max-width: $mobile)
      flex-direction: column

  section
    position: relative

    flex: 1
    margin-right: $baseline * 1.5

    @media (max-width: $mobile)
      margin: 0 0 $baseline 0

    &:last-of-type
      margin-right: 0

  h3
    margin-bottom: $baseline / 2
    font-size: $fs-1
    font-weight: 600

  p + p
    margin-top: $baseline / 2

    a
      color: $c-base

      font-weight: 600

      transition: .15s all

      &:hover
        color: darken($c-base, 10%)

      &::after
        +fa-icon()

        margin-left: $baseline / 2

        opacity: 0.5

        content: $fa-var-arrow-right


      &:hover::after
        opacity: 1

  //- start reading Kairly button
  > a
    +subscribed-button

    display: table
    margin: 0 auto

    border-radius: $baseline * 0.75
    height: $baseline * 1.5
    line-height: $baseline * 1.5

</style>
