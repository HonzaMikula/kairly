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

      <div class="input">
        <input type="radio" id="howOftenDaily" value="daily" v-model="howOften" />
        <label for="howOftenDaily">Daily</label>
      </div>

      <div class="input">
        <input type="radio" id="howOftenWeekly" value="weekly" v-model="howOften" />
        <label for="howOftenWeekly">Weekly</label>
      </div>

      <div class="input">
        <input type="radio" id="howOftenMonthly" value="monthly" v-model="howOften" />
        <label for="howOftenMonthly">Monthly</label>
      </div>
    </section>

    <section v-if="howOften == 'weekly'">
      <h2>Which day(s)?</h2>

      <div class="input" v-for="(day, index) in days" :key="day">
        <input type="checkbox" :id="'day'+ index"/>

        <label :for="'day'+ index">{{ day }}</label>
      </div>
      
    </section>

    <section v-else-if="howOften == 'monthly'">
      <h2>Which day(s)?</h2>

      <table class="calendar">
        <tbody>
          <tr v-for="week in [0,1,2,4]" :key="week">
            <template v-if="week != 4">
              <td v-for="day in [1,2,3,4,5,6,7]" :key="day">
                {{ week * 7 + day }}
              </td>
            </template>

            <template v-else>
              <td v-for="day in [1,2,3]" :key="day">
                {{ week * 7 + day }}
              </td>
            </template>
          </tr>
        </tbody>

      </table>
    </section>

    <section>
      <h2>What time(s)?</h2>

      <div class="input" v-for="(time, index) in times" :key="time">
        <input type="checkbox" v-if="howOften == 'daily'" :id="'time'+ index"/>
        <input type="radio" v-else :id="'time'+ index"/>

        <label :for="'time'+ index">{{ time }}</label>
      </div>
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
      howOften: null,
      days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      times: ['6:00', '9:00', '12:00', '15:00', '18:00', '21:00']
    }
  },
}
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'
@import './styles/components/mixins'

.modal-dialog.select-periodicity-view
  width: 700px

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
    

    section
      display: grid
      grid-column-gap: $baseline / 2
      grid-template-columns: 1fr 1fr 1fr 1fr

    h2
      grid-column: 1 / span 4
      margin-bottom: $baseline / 4
      font-weight: 600

    section + section
      margin-top: $baseline

  .input
    input
      position: absolute
      
      height: 0
      width: 
      
      opacity: 0

      cursor: pointer

    input + label
      display: flex
      margin-bottom: $baseline / 4  

      &::before
        display: inline-block
        height: $baseline * 0.75
        margin-right: $baseline / 4 
        width: $baseline * 0.75

        background: #eee
        border: 2px solid #ddd
        
        content: ''
        cursor: pointer
        text-align: center

    input[type=radio] + label::before
      border-radius: 100%

    input:checked + label::before
      background: $c-base
      border: 2px solid darken($c-base, 30%)
      color: #fff

      +fa-icon()
      @extend .fas
      line-height: $baseline *0.75
      font-size: $fs--2

      content: fa-content($fa-var-check)


  .calendar
    border: 1px solid #eee
    width: 300px

    td
      border: 1px solid #eee

      text-align: center

      &:hover
        background: lighten($c-base, 30%)
        cursor: pointer


</style>
