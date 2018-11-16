<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop>
      <header>
        <h1>{{ newspaper ? 'Modify newspaper' : 'Create new newspaper' }}</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>

      <edit-newspaper-view>
        <div class="title">
          <input placeholder="What's the newspaper name?" v-model="title">
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

            <template v-else-if="periodicity.frequency == '6x_per_day'">
              6x per day at 6:00, 9:00, 12:00, 15:00, 18:00 and 21:00
            </template>

            <template v-else>
              {{ periodicity.frequency }} {{ DAYS_OF_WEEK[periodicity.dow - 1] }} {{ periodicity.time }}
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
            <textarea id="editorial" v-model="description" placeholder="What this newspaper is about?"></textarea>
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
              :prefill="this.newspaper && this.newspaper.picture"
              :customStrings="{
                drag: 'Drag or upload image'
              }">
            </picture-input>
          </picture>

        </div>
      </edit-newspaper-view>

      <footer>
        <button @click="submit">{{ this.newspaper ? 'Save' : 'Create newspaper' }}</button>
      </footer>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import { mapActions, mapState } from 'vuex'

import PictureInput from '@/lib/vue-picture-input/PictureInput'
import { DAYS_OF_WEEK } from '@/utils/period'
import DialogWindow from '@/components/modals/Dialog'
import PeriodWidget from '@/components/widgets/PeriodWidget'

export default {
  name: 'EditNewspaperModal',

  props: {
    newspaper: Object,
    closeModal: Function,
    onCreated: Function
  },

  components: {
    PeriodWidget,
    PictureInput,
    DialogWindow
  },

  data() {
    return {
      title: this.newspaper ? this.newspaper.title : '',
      description: this.newspaper ? this.newspaper.description : '',
      periodicity: this.newspaper ? this.newspaper.periodicity : null,
      image: null,
      DAYS_OF_WEEK
    }
  },

  computed: mapState({
    user: state => state.auth.user
  }),

  methods: {
    onPictureChange(image) {
      this.image = image
    },

    selectPeriodicity(periodicity) {
      this.periodicity = periodicity
    },

    async submit() {
      const errors = []

      if (this.title.trim() === '') {
        errors.push("Title is empty")
      }

      if (this.description.trim() === '') {
        errors.push("Editorial is empty")
      }

      if (this.periodicity === null) {
        errors.push("Periodicity is not selected")
      }

      if (errors.length) {
        // TODO show validation in form
        alert(errors.join("\n"))
        return
      }

      if (this.newspaper) {
        const fields = {}
        if (this.title !== this.newspaper.title) {
          fields.title = this.title
        }
        if (this.description !== this.newspaper.description) {
          fields.description = this.description
        }
        if (this.periodicity) { //TODO compare periodicity
          fields.periodicity = this.periodicity
        }
        if (this.image) {
          fields.image = this.image
        }
        await this.updateNewspaper({
          fullName: this.newspaper.fullName,
          fields
        })
      } else {
        const createdNewspaper = await this.startNewspaper({
          authorId: this.user.id,
          newspaper: {
            title: this.title,
            description: this.description,
            periodicity: this.periodicity,
            image: this.image
          }
        })
        this.onCreated(createdNewspaper)
      }

      this.closeModal()
    },

    ...mapActions(['startNewspaper', 'updateNewspaper'])
  }
}
</script>

<style lang="sass">
edit-newspaper-view
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

      @media (max-width: $mobile)
        font-size: $fs-3

  .periodicity
    position: relative

    padding: $baseline/4 0

    border-bottom: 1px solid #ddd
    border-top: 1px solid #ddd

    text-align: center

    > span
      font-family: $ff-serif

      cursor: pointer

    > button
      +subscribed-button

  .description
    display: grid
    grid-template-columns: 1fr 2fr
    grid-column-gap: $baseline
    grid-template-rows: auto
    margin-top: $baseline

    @media (max-width: $mobile)
      grid-template-columns: 1fr

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
