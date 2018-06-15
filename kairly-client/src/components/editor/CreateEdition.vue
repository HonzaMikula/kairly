<template>
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
      Selected: {{ period }} / {{ dow }} / {{ time }}

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
</template>

<script>
import * as api from '@/api'

// import { mapState, mapGetters } from 'vuex'
// import TABS from './exploreTabs'

import PictureInput from 'vue-picture-input'
import PeriodWidget from '@/components/widgets/PeriodWidget'

export default {
  name: 'Explore',

  components: {
    PeriodWidget,
    PictureInput
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
    onPictureChange (image) {
      //console.log(this.$refs.pictureInput.file)
      //console.log(image)
      this.image = image
    },

    selectPeriodicity(periodicity) {
      this.periodicity = periodicity
    },

    submit() {
      const { authorId } = this.$route.params
      api.createEdition(authorId, {
        title: this.title,
        description: this.description,
        periodicity: this.periodicity,
        time: this.time,
        dow: this.dow,
        image: this.image
      })
      .then(resp => {
        this.$router.push('/editions/' + resp.edition.id)
      })
    }
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
