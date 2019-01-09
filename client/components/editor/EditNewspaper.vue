<template>
  <dialog-window :closeModal="closeModal">
    <modal-dialog role="dialog" @click.stop>
      <header>
        <h1>{{ newspaper ? $t('Modify the newspaper') : $t('Start a new newspaper') }}</h1>
        <button-close tabindex="0" role="button" @click="closeModal()"></button-close>
      </header>

      <main class="edit-newspaper-view">
        <div>
          <label for="name">{{ $t('Newspaper name') }}</label>
          <input id="name" v-model="title" />
        </div>

        <div>
          <label for="description">{{ $t('Short description') }}</label>
          <textarea
            id="description"
            v-model="description"
            :placeholder="$t('What this newspaper is about?')"
          ></textarea>
          <p>Maximum 160 characters.</p>
        </div>

        <div class="periodicity">
          <label>{{ $t('Periodicity') }}</label>
          <button
            v-if="!periodicity"
            @click="$refs.periodWidget.openSubscribeWidget()"
          >
            {{ $t('Select periodicity') }}
          </button>

          <span v-if="periodicity" @click="$refs.periodWidget.openSubscribeWidget()">
            <template v-if="periodicity.frequency == '3x_per_day'">{{ $t('At 6:00, 12:00 and 18:00') }}</template>

            <template v-else-if="periodicity.frequency == '6x_per_day'">{{ $t('Every 3 hours') }}</template>

            <template v-else-if="periodicity.frequency == '6x_per_day'">
              {{ $t('Continously every 3 hours.') }}
            </template>

            <template v-else>
              {{ periodicity.frequency }} {{ getDayOfWeekLabel(periodicity.dow) }} {{ periodicity.time }}
            </template>
          </span>

          <period-widget ref="periodWidget" :onSelect="selectPeriodicity"/>
        </div>

        <div>
          <label for="price">{{ $t('Subscription price') }}</label>
          <select id="price" v-model="price">
            <option value="0">{{ $t('Free') }}</option>
            <option value="25">25 Kč</option>
            <option value="75">75 Kč</option>
            <option value="175">175 Kč</option>
          </select>
        </div>

        <div class="picture">
          <label>Picture</label>
          <picture>
            <picture-input
              ref="pictureInput"
              @change="onPictureChange"
              width="182"
              height="78"
              accept="image/jpeg, image/png"
              size="10"
              buttonClass="btn"
              :prefill="this.newspaper && this.newspaper.picture"
              :customStrings="{
                drag: $t('Drag or upload image')
              }"
            ></picture-input>
          </picture>
        </div>
      </main>

      <footer>
        <button @click="submit">{{ this.newspaper ? $t('Save') : $t('Create newspaper') }}</button>
      </footer>
    </modal-dialog>
  </dialog-window>
</template>

<script>
import { mapActions, mapState } from "vuex";

import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import PictureInput from '@/lib/vue-picture-input/PictureInput'
import DialogWindow from '@/components/modals/Dialog'
import PeriodWidget from '@/components/widgets/PeriodWidget'

export default {
  name: "EditNewspaperModal",

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

  mixins: [PeriodicityMixin],

  data() {
    return {
      title: this.newspaper ? this.newspaper.title : "",
      description: this.newspaper ? this.newspaper.description : "",
      periodicity: this.newspaper ? this.newspaper.periodicity : null,
      price: this.newspaper ? ~~this.newspaper.price : 25,
      image: null,
    }
  },

  computed: mapState({
    user: state => state.auth.user
  }),

  methods: {
    onPictureChange(image) {
      this.image = image;
    },

    selectPeriodicity(periodicity) {
      this.periodicity = periodicity;
    },

    async submit() {
      const errors = [];

      if (this.title.trim() === "") {
        errors.push("Title is empty");
      }

      if (this.description.trim() === "") {
        errors.push("Editorial is empty");
      }

      if (this.periodicity === null) {
        errors.push("Periodicity is not selected");
      }

      if (errors.length) {
        // TODO show validation in form
        alert(errors.join("\n"));
        return;
      }

      if (this.newspaper) {
        const fields = {};
        if (this.title !== this.newspaper.title) {
          fields.title = this.title;
        }
        if (this.description !== this.newspaper.description) {
          fields.description = this.description;
        }
        if (this.price != this.newspaper.price) {
          fields.price = this.price;
        }
        if (this.periodicity) {
          //TODO compare periodicity
          fields.periodicity = this.periodicity;
        }

        if (this.image) {
          fields.image = this.image;
        }
        await this.updateNewspaper({
          fullName: this.newspaper.fullName,
          fields
        });
      } else {
        const createdNewspaper = await this.startNewspaper({
          authorId: this.user.id,
          newspaper: {
            title: this.title,
            description: this.description,
            periodicity: this.periodicity,
            price: this.price,
            image: this.image
          }
        });
        this.onCreated(createdNewspaper);
      }

      this.closeModal();
    },

    ...mapActions(["startNewspaper", "updateNewspaper"])
  }
};
</script>

<style lang="sass">
//- EDIT NEWSPAPER -//
.edit-newspaper-view
  display: block
  padding: $baseline

  //- form fields
  > div
    display: table
    width: $baseline * 14
    margin-bottom: $baseline


    //- label
    label, h3
      display: table

      font-size: $fs--1
      font-weight: 600

    //- input fields
    input
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: $baseline * 8

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--1


    //- textarea
    textarea
      box-sizing: border-box
      height: $baseline * 2.5
      padding: $baseline/4
      width: $baseline * 14

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--1

      @media (max-width: $mobile)
        width: 100%


    //- select
    select
      box-sizing: border-box
      height: $baseline * 1.25
      padding: 0 $baseline/4
      width: $baseline * 8

      border: 1px solid #ddd

      font-family: $ff-sans
      font-size: $fs--1


    //- help
    p
      color: #555

      font-size: $fs--1
      line-height: 1.42

      a
        color: darken($c-base, 20%)

        font-weight: 600
        text-decoration: underline

        &:hover,
        &:focus
          text-decoration: none


  //- periodicity
  .periodicity
    position: relative

    .period-widget
      left: 0
      top: 80px

      margin-left: 0

      &::after
        left: 70px


  //- picture
  .picture
    picture
      display: block
      height: $baseline * 2
      padding-bottom: $baseline

    button
      margin-top: $baseline / 4

</style>
