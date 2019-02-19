<template>
  <app-layout>
    <div class="independent-journalists">
      <section class="independent-journalists--hero">
        <div>
          <h1>Jste nezávislí novináři či blogeři?</h1>
          <ul>
            <li>Publikujte na moderní publikační platformě, o kterou se nemusíte starat.</li>
            <li>Začnětě vydělávat s unikátním konceptem placeného obsahu.</li>
            <li>Staňte se skutečně nezávislým autorem.</li>
          </ul>
        </div>
      </section>

      <section class="independent-journalist--faq">
        <div>
          <h2>Co je Kairly?</h2>
          <p>
            Kairly je vznikající platforma pro novináře a jejich čtenáře, která nabízí unikátní koncept placeného obsahu.
          </p>

          <h2>V čem je unikátní?</h2>
          <p>
            Vracíme do žurnalistiky roli editorů. Editoři na Kairly vydávají noviny. Do nich zařazují nejlepší články a tweety od autorů napříč
            celou platformou. Čtenáři platí za noviny předplatné. Peníze jsou pak rozděleny mezi editora a autory, kteří se
            ve vydáních novin objevili.
          </p>

          <h2>V čem je unikátní pro čtenáře?</h2>
          <p>
            Nemáme žádnou reklamu. Nikoho nesledujeme. U nás čtenáři neskrolují donekonečna. Čtou je to, co opravdu chtějí číst a vždy v době,
            kdy to chtějí číst.
          </p>
        </div>

        <picture>
          <img src="~assets/microsite/kairly-independent-journalist-1.jpg" alt="Kairly" />
        </picture>

      </section>

      <QuoteZouzalik></QuoteZouzalik>

      <section class="independent-journalists--benefits">
        <div>
          <h2>Publikační platforma, o kterou se nemusíte starat</h2>


          <ul>
            <li>Kairly je moderní publikační platforma, díky které</li>

            <li>
              Vracíme do hry profesi editorů, kteří vydávájí digitální noviny.
              Za kvalitní výběr obsahu čtenáři platí předplatné.

               Věříme, že obsah by měli pro
              čtenáře vybírat lidi, nikoliv neprůhledné algoritmy.
            </li>

            <li>
              Editoři zařazují do svých výdání novin ty nejlepší články a tweety od všech autorů.
              Čtenáři se je předplácí. Editoři z
            </li>
          </ul>
        </div>

        <div>
          <h2>Začněte vydělávat na svém obsahu</h2>


          <ul>
            <li>
              Vydělávejte na předplatném pro váš obsah.
            </li>
            <li>
              Za články a tweety, které si editoři vyberou do svých vydání novin, budete odměněni.
            </li>
            <li>
              Čtenáři mají možnost vás odměnit nad rámec běžného předplatného.
            </li>
          </ul>
        </div>

      </section>



      <section class="independent-journalists--launch">
        <h2>Na ostro startujeme</h2>
        <p>3. čtvrtletí 2019</p>

        <p>
          Zapojte se do uzavřené betaverze, pomozte nám platformu vyladit a
          buďte mezi prvními, kdo začne na ní vydělávat.
        </p>
      </section>
    </div>
  </app-layout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout'
import QuoteZouzalik from '@/components/microsite/QuoteZouzalik'

export default {
  name: 'IndependentJournalists',

  auth: false,

  components: {
    AppLayout,
    QuoteZouzalik
  },

  head() {
    return {
      title: 'Independent Journalists – Kairly',
      meta: [
        { hid: 'description', name: 'description', content: '' },
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

.independent-journalists
  background: #fff

  > *
    max-width: 900px
    margin: 0 auto

//- Hero
.independent-journalists--hero
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
    font-size: $fs-2

    counter-reset: benefits

  li
    margin-bottom: $baseline / 2

    &::before
      display: inline-block
      margin-right: $baseline / 2
      border-radius: 100%
      height: $baseline * 1.25
      width: $baseline * 1.25

      background: #fff

      font-size: $fs-0
      font-weight: 600
      line-height: $baseline * 1.25
      text-align: center

      counter-increment: benefits
      content: counter(benefits)

//- FAQ
.independent-journalist--faq
  display: grid
  grid-template-columns: 2fr 1fr
  grid-column-gap: $baseline
  padding-bottom: $baseline * 2

  h2
    margin-bottom: $baseline / 2
    font-size: $fs-3
    font-weight: 600

  p
    margin-bottom: $baseline * 1.5

    font-size: $fs-1

    &:last-of-type
      margin-bottom: 0

  img
    height: 100%
    width: 100%
    object-fit: cover

//- Benefits
.independent-journalists--benefits
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

//- Launch
.independent-journalists--launch
  display: flex
  flex-direction: column
  align-items: center
  justify-content: center
  padding: $baseline*2 0

  background: #f5f5f5

  h2
    margin-bottom: $baseline * 2
    font-size: $fs-1

  h2 + p
    margin-bottom: $baseline * 2
    font-size: 48px
    font-weight: 600


</style>
