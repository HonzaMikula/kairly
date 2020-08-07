<template>
  <DialogWindow
    v-if="active"
    custom-class="publish-post-dialog"
    @close="closeModal"
  >
    <template #header>
      <h1>{{ $t('Publish post') }}</h1>
    </template>

    <h2>{{ post.content.title ? post.content.title : post.content.content }}</h2>

    <section class="publish-post--price">
      <h2>{{ $t('Set price of the article for editors') }}</h2>
      <div>
        <input v-model="postPrice" step="0.01" type="number" min="0.00" max="100000.00">
        {{ $t('Kč per subscriber') }}
      </div>
      <p v-html="$t('You will recieve <strong>{price} Kč</strong> from each subscriber from newsletter where your post will appear.', { price: postPrice })" />
    </section>

    <section v-if="showSchedule" class="publish-post--scheduling">
      <h2>{{ $t('Schedule a time to publish') }}</h2>
      <input type="datetime-local">
    </section>

    <template #footer>
      <button class="publish-now" @click="submit">
        {{ showSchedule ? $t('Schedule post') : $t('Publish now') }}
      </button>

      <!--button class="schedule" @click="showSchedule = !showSchedule">
          {{ showSchedule ? $t('Cancel scheduling') : $t('Schedule for later') }}
        </button-->
    </template>
  </DialogWindow>
</template>

<script>
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'PublishPostModal',

  components: {
    DialogWindow
  },

  mixins: [ModalMixin],

  props: {
    post: { type: Object, required: true },
    price: { type: String, required: true }
  },

  data () {
    return {
      postPrice: this.price ? this.price : '0.00',
      showSchedule: null
    }
  },

  methods: {
    submit () {
      this.$emit('publish', this.price)
      this.closeModal()
    }
  }
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

//- NEWSPAPER SUBSCRIPTION DIALOG -//
.modal-dialog.publish-post-dialog
  display: block
  max-width: 360px

  main
    padding: $baseline/2 $baseline/2 0 $baseline/2

    h2
      margin-bottom: $baseline / 2

      font-weight: 600

//- setting up price
.publish-post--price
  padding: $baseline/2 $baseline/2 $baseline*3/4 $baseline/2
  margin: 0 (-$baseline/2)

  background: #fafafa
  border-top: 1px solid #eee

  //- input field
  input
    border-radius: 5px
    box-sizing: border-box
    height: $baseline * 1.25
    padding: 0 $baseline/4
    width: 120px

    border: 1px solid #eee

    font-family: $ff-sans
    font-size: $fs-0
    font-weight: 600

    &::placeholder
      font-weight: 400

  p
    margin-top: $baseline / 2

    font-size: $fs--1
    line-height: 1.42

//- scheduling post
.publish-post--scheduling
  padding: $baseline/2 0

  border-top: 1px solid #eee

  input[type=datetime-local]
    font-family: $ff-sans

//- Footer with buttons
.publish-post-dialog footer

  //- publish button
  button.publish-now
    +button

  //- schedule button
  button.schedule
    +button
    display: table
    margin: $baseline/2 auto 0 auto

    background: transparent
    border: 0
    color: darken($c-base, 10%)

    &:focus,
    &:hover
      background: transparent
      color: darken($c-base, 20%)
</style>
