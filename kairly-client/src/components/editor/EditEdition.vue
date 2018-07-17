
<template>
  <dialog-window :onClose="onClose">
    <modal-dialog role="dialog" @click.stop>
      <header>
        <h1>{{ edition ? 'Modify edition' : 'Create new edition' }}</h1>
      </header>

      <edit-edition-view>
        <div class="title">
          <input placeholder="What's the edition name?" v-model="title">
        </div>

        <div class="periodicity">
          <button
            v-if="!periodicity"
            @click="$refs.periodWidget.openSubscribeWidget()">
            Select period
          </button>

          <span
            v-if="periodicity"
            @click="$refs.periodWidget.openSubscribeWidget()">

            <template v-if="periodicity.frequency == '3x_per_day'">
              3x per day at 6:00, 12:00 and 18:00
            </template>

            <template v-else>
              {{ periodicity.frequency }} {{ DAYS[periodicity.dow - 1] }} {{ periodicity.time }}
            </template>
          </span>

          <div class="period-wrapper">
            <period-widget
              ref="periodWidget"
              :onSelect="selectPeriodicity" />
          </div>
        </div>

        <div class="description">
          <section>
            <label for="editorial">Editorial</label>
            <textarea id="editorial" v-model="description" placeholder="What this edition is about?"></textarea>
          </section>

          <picture>
            <picture-input
              ref="pictureInput"
              @change="onPictureChange"
              width="580"
              height="250"
              accept="image/jpeg,image/png"
              size="10"
              buttonClass="btn"
              :prefill="this.edition && this.edition.picture"
              :customStrings="{
                drag: 'Drag or upload image'
              }">
            </picture-input>
          </picture>

        </div>
      </edit-edition-view>

      <footer>
        <button @click="submit">{{ this.edition ? 'Save' : 'Create edition' }}</button>
      </footer>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import DialogWindow from '@/components/modals/Dialog'
import PictureInput from 'vue-picture-input'
import PeriodWidget from '@/components/widgets/PeriodWidget'

export default {
  name: 'EditEditionModal',

  props: {
    edition: Object,
    onClose: Function,
    onCreated: Function
  },

  components: {
    PeriodWidget,
    PictureInput,
    DialogWindow
  },

  data() {
    return {
      title: this.edition ? this.edition.title : '',
      description: this.edition ? this.edition.description : '',
      periodicity: this.edition ? this.edition.periodicity : null,
      DAYS: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
  },

  computed: mapGetters(['user']),

  methods: {
    onPictureChange(image) {
      this.image = image
    },

    selectPeriodicity(periodicity) {
      this.periodicity = periodicity
    },

    submit() {
      // TODO show validation in form
      if (this.title.trim() === '') {
        alert("Title is empty")
        return
      }

      if (this.description.trim() === '') {
        alert("Editorial is empty")
        return
      }

      if (this.periodicity === null) {
        alert("Periodicity is not selected")
        return
      }

      if (this.image === null && !this.edition) {
        alert("Image is not selected")
        return
      }

      if (this.edition) {
        const fields = {}
        if (this.title !== this.edition.title) {
          fields.title = this.title
        }
        if (this.description !== this.edition.description) {
          fields.description = this.description
        }
        if (this.periodicity) { //TODO compare periodicity
          fields.periodicity = this.periodicity
        }
        if (this.image) {
          fields.image = this.image
        }
        this.updateEdtion({
          fullName: this.edition.fullName,
          fields
        })
      } else {
        this.startNewEdtion({
          authorId: this.user.id,
          edition: {
            title: this.title,
            description: this.description,
            periodicity: this.periodicity,
            image: this.image
          }
        }).then(this.onCreated)
      }

      this.onClose()
    },

    ...mapActions(['startNewEdtion', 'updateEdtion'])
  }
}
</script>

<style lang="sass">
edit-edition-view
  display: block
  padding: $baseline

  .title
    padding-bottom: $baseline

    input
      display: block
      box-sizing: border-box
      width: 100%

      border: 0

      font-family: $ff-serif
      font-size: $fs-4
      font-weight: 600
      line-height: $baseline * 2
      text-align: center

  .periodicity
    position: relative

    padding: $baseline/4 0

    border-bottom: 1px solid #ddd
    border-top: 1px solid #ddd

    text-align: center

    > span
      font-family: $ff-serif

      cursor: pointer

  .description
    display: grid
    grid-template-columns: 1fr 2fr
    grid-column-gap: $baseline
    grid-template-rows: auto
    margin-top: $baseline

    label
      display: table

      font-weight: 600

    textarea
      height: 200px
      width: 100%

      border: 0

      font-family: $ff-serif
      font-size: $fs-0
</style>
