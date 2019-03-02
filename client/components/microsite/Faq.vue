<template>
  <section class="microsite-faq">
    <div v-html="$t('@independent-journalists/faq')">

    </div>
    <!-- <h2>Co je Kairly?</h2>
      <p>
        Kairly je vznikající platforma pro novináře a jejich čtenáře, která nabízí <strong>unikátní koncept placeného obsahu</strong>.
      </p>

      <h2>V čem je unikátní?</h2>
      <p>
        Vracíme do žurnalistiky roli editorů. Editoři na Kairly vydávají noviny. Do nich zařazují nejlepší články a tweety od autorů napříč
        celou platformou. <strong>Čtenáři platí za noviny předplatné</strong>.
        <strong>Peníze jsou pak rozděleny mezi editora a autory</strong>, kteří se
        ve vydáních novin objevili.
      </p>

      <h2>Co přináší čtenářům?</h2>
      <p>
        Nemáme žádnou reklamu. Nikoho nesledujeme. U nás čtenáři neskrolují donekonečna. <strong>Čtou jen to, co opravdu chtějí číst a vždy v době,
        kdy to chtějí číst</strong>.
      </p> -->

    <picture>
      <slot>
        <img src="~assets/microsite/publishers-1.jpg" alt="Kairly" />
      </slot>
    </picture>
  </section>
</template>

<script>
export default {
  name: 'Faq'
}
</script>

<style lang="sass">
//- FAQ
.microsite-faq
  display: grid
  grid-template-columns: 540px 334px
  grid-column-gap: $baseline
  padding-bottom: $baseline * 2

  @media (max-width: 950px)
    grid-template-columns: auto
    padding: 0

  h2
    margin-bottom: $baseline / 2
    font-size: $fs-3
    font-weight: 600

  p
    margin-bottom: $baseline * 1.5

    font-size: $fs-1

    &:last-of-type
      margin-bottom: 0


  @media (max-width: 950px)
    picture
      grid-row: 1

    div
      padding: $baseline

  @media (max-width: $mobile)
    div
      padding: $baseline / 2

  img
    height: 100%
    width: 100%
    object-fit: cover

    @media (max-width: 940px)
      max-height: 300px
</style>
