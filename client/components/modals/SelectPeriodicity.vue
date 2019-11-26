<template>
  <DialogWindow
    v-if="active"
    custom-class="select-periodicity-view"
    @close="closeModal"
  >
    <template #header>
      <h1>{{ $t('Select periodicity') }}</h1>
    </template>

    <section>
      <h2>How often?</h2>

      <label>
        <input type="radio" name="howOften" />
        Daily
      </label>

      <label>
        <input type="radio" name="howOften" />
        Weekly
      </label>

      <label>
        <input type="radio" name="howOften" />
        Monthly
      </label>
    </section>

    <section>
      <h2>Which days?</h2>

      <label v-for="day in days" :key="day">
        <input type="checkbox" />
        {{ day }}
      </label>
    </section>

    <section>
      <h2>What time?</h2>

      <label v-for="time in times" :key="time">
        <input type="checkbox" />
        {{ time }}
      </label>
    </section>

    <template #footer>
      <button>Save</button> 
    </template>
  </DialogWindow>
</template>

<script>
import DialogWindow from '@/components/modals/DialogWindow'
import ModalMixin from '@/mixins/ModalMixin'

export default {
  name: 'SelectPeriodicityModal',

  components: {
    DialogWindow
  },

  mixins: [ModalMixin],

  data() {
    return {
      days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      times: ['6:00', '9:00', '12:00', '15:00', '18:00', '21:00']
    }
  },
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'

.modal-dialog.select-periodicity-view
  max-width: 700px

  > header h1
    @media (max-width: $mobile)
      padding: 0 $baseline/2

  main
    padding: $baseline / 2
    overflow: auto
    -webkit-overflow-scrolling: touch

    background: #fff

    @media (max-width: $mobile)
      padding: $baseline/2

    h2
      grid-column: 1 / span 4
      font-weight: 600

    section + section
      margin-top: $baseline

    section
      display: grid
      grid-column-gap: $baseline / 2
      grid-template-columns: 1fr 1fr 1fr 1fr


</style>
