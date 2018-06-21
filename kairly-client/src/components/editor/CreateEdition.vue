
<template>
  <dialog-window :onClose="closeModal">
    <modal-dialog role="dialog"  @click="$event.stopPropagation()">
      <div class="dev-create-edition">
        <h1>Create new edition</h1>

        <picture-input
          ref="pictureInput"
          @change="onPictureChange"
          width="450"
          height="300"
          margin="16"
          accept="image/jpeg,image/png"
          size="10"
          buttonClass="btn"
          :customStrings="{
            drag: 'Drag or upload image'
          }">
        </picture-input>

        <div class="row">
          Edition Title
          <input v-model="title">
        </div>

        <div class="row">
          Description
          <textarea v-model="description"></textarea>
        </div>

        <div class="row">
          Period / release time

          <button
            @click="$refs.periodWidget.openSubscribeWidget()">
            Select period
          </button>

          <br>
          Selected: <span v-if="periodicity">{{ periodicity.frequency }} / {{ periodicity.dow }} / {{ periodicity.time }}</span>

          <div class="period-wrapper">
            <period-widget
              ref="periodWidget"
              :onSelect="selectPeriodicity" />
          </div>
        </div>

        <button
          @click="submit">
          Create
        </button>
      </div>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import { mapActions } from 'vuex'

import DialogWindow from '@/components/modals/Dialog'
import PictureInput from 'vue-picture-input'
import PeriodWidget from '@/components/widgets/PeriodWidget'

export default {
  name: 'CreateEditionModal',

  props: {
    'onClose': Function
  },

  components: {
    PeriodWidget,
    PictureInput,
    DialogWindow
  },

  data() {
    return {
      title: '',
      description: '',
      periodicity: null,
      time: null,
      dow: null
    }
  },

  methods: {
    closeModal() {
      this.onClose()
    },
    
    onPictureChange(image) {
      this.image = image
    },

    selectPeriodicity(periodicity) {
      this.periodicity = periodicity
    },

    submit() {
      const { authorId } = this.$route.params

      this.startNewEdtion({
        authorId,
        edition: {
          title: this.title,
          description: this.description,
          periodicity: this.periodicity,
          time: this.time,
          dow: this.dow,
          image: this.image
        }
      })
    },

    ...mapActions(['startNewEdtion'])
  }
}
</script>

<style lang="sass">
.dev-create-edition
  width: 800px
  margin: 0 auto
  margin-top: 40px

  h1
    font-size: 26px
    margin-bottom: 20px

  .row
    margin-bottom: 20px

  .period-wrapper
    position: relative
</style>
