<template>
  <div class="newspaper-settings-view">
    <h1>{{ $t('Newspaper settings') }}</h1>

    <main>
      <section class="newspaper-settings--general">
        <h2>General</h2>
        <div>
          <label for="name">{{ $t('Newspaper name') }}</label>
          <input
            id="name"
            v-model="title"
          />
        </div>

        <div>
          <label for="description">{{ $t('Short description') }}</label>
          <textarea
            id="description"
            v-model="description"
            :placeholder="$t('What this newspaper is about?')"
          />
          <p>{{ $t('Maximum 160 characters.') }}</p>
        </div>

        <h2>{{ $t('Subscription') }}</h2>

        <div class="periodicity">
          <label>{{ $t('Periodicity') }}</label>
          <button
            v-if="!periodicity"
            @click.stop="showPeriodicityWidget = true"
          >
            {{ $t('Select periodicity') }}
          </button>

          <span
            v-if="periodicity"
            @click.stop="showPeriodicityWidget = true"
          >
            <template v-if="periodicity.frequency == '3x_per_day'">{{ $t('At 6:00, 12:00 and 18:00') }}</template>
            <template v-else-if="periodicity.frequency == '6x_per_day'">{{ $t('Every 3 hours') }}</template>
            <template v-else-if="periodicity.frequency == '6x_per_day'">
              {{ $t('Continously every 3 hours.') }}
            </template>
            <template v-else>
              {{ periodicity.frequency }} {{ getDayOfWeekLabel(periodicity.dow) }} {{ periodicity.time }}
            </template>
          </span>

          <PeriodWidget
            v-if="showPeriodicityWidget"
            @changePeriodicity="changePeriodicity"
          />
        </div>

        <div>
          <label for="price">{{ $t('Subscription price') }}</label>
          <select
            id="price"
            v-model="price"
          >
            <option value="0">{{ $t('Free') }}</option>
            <option value="25">25 Kč</option>
            <option value="75">75 Kč</option>
            <option value="175">175 Kč</option>
          </select>
        </div>
      </section>

      <section class="newspaper-settings--side">
        <div class="picture">
          <h2>{{ $t('Picture') }}</h2>
          <picture>
            <picture-input
              ref="pictureInput"
              width="364"
              height="156"
              accept="image/jpeg, image/png"
              size="10"
              buttonClass="btn"
              :prefill="this.newspaper && this.newspaper.picture"
              :customStrings="{
                drag: $t('Upload image')
              }"
              @change="onPictureChange"
            />
          </picture>
        </div>

        <h2>{{ $t('Editors') }}</h2>

        <div class="newspaper-settings--editors">
          <ul>
            <EditorCard
              :editor="editor"
              :role="$t('Main editor')"
              :can-delete="false"
            />

            <EditorCard
              v-for="(editor, idx) in coEditors"
              :key="editor.id"
              :editor="editor"
              :role="$t('Co-editor')"
              :can-delete="true"
              @delete="coEditors.splice(idx, 1)"
            />
          </ul>

          <h3>{{ $t('Add co-editor') }}</h3>

          <div class="newspaper-settings--editors--add-editor">
            <input
              v-model="coEditorSlug"
              type="search"
              :placeholder="$t('Type username slug')"
              @keyup.enter="addCoEditor"
            />
            <button
              :disabled="coEditorSlug === ''"
              @click="addCoEditor"
            >{{ $t('Add co-editor') }}</button>
          </div>
        </div>
      </section>
    </main>

    <footer>
      <button @click="submit">{{ this.newspaper ? $t('Save') : $t('Create newspaper') }}</button>
    </footer>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

import AppLayout from '@/components/layout/AppLayout'
import EditorCard from '@/components/editor/EditorCard'
import PeriodicityMixin from '@/mixins/PeriodicityMixin'
import PictureInput from '@/lib/vue-picture-input/PictureInput'
import DialogWindow from '@/components/modals/DialogWindow'
import PeriodWidget from '@/components/widgets/PeriodWidget'


export default {
  name: "NewspaperSettings",

  components: {
    AppLayout,
    EditorCard,
    PeriodWidget,
    PictureInput,
    DialogWindow
  },

  mixins: [PeriodicityMixin],

  props: {
    newspaper: Object,
  },

  data() {
    return {
      title: this.newspaper ? this.newspaper.title : "",
      description: this.newspaper ? this.newspaper.description : "",
      periodicity: this.newspaper ? this.newspaper.periodicity : null,
      price: this.newspaper ? ~~this.newspaper.price : 25,
      coEditors: this.newspaper ? [...this.newspaper.coEditors] : [],
      coEditorSlug: '',
      image: null,
      showPeriodicityWidget: false
    }
  },

  computed: {
    ...mapState({
      user: state => state.auth.user,
    }),

    editor() { return this.newspaper ? this.newspaper.editor : this.user }
  },

  methods: {
    onPictureChange(image) {
      this.image = image;
    },

    changePeriodicity(frequency, dow, time) {
      this.showPeriodicityWidget = false

      this.periodicity = {
        "frequency": frequency,
        "dow": dow,
        "time": time
      }
    },

    updateComponentData({ title, description, price }) {
      this.title = title
      this.description = description
      this.price = ~~price
    },

    async addCoEditor() {
      const slug = this.coEditorSlug.trim()
      if (slug === '') {
        return
      }

      try {
        const { author: editor } = await this.$store.dispatch("getAuthor", slug)
        if (editor.id != this.editor.id && !this.coEditors.find(item => item.id === editor.id)) {
          this.coEditors.push(editor)
        }
        this.coEditorSlug = ''
      } catch (e) {
        return
      }
    },

    async submit() {
      const errors = [];
      let fullName = null;

      if (this.title.trim() === "") {
        errors.push(this.$t("Title is empty"));
      }

      if (this.description.trim() === "") {
        errors.push(this.$t("Editorial is empty"));
      }

      if (this.periodicity === null) {
        errors.push(this.$t("Periodicity is not selected"));
      }

      if (errors.length) {
        // TODO show validation in form
        alert(errors.join("\n"));
        return;
      }

      if (this.newspaper) {
        const fields = {};
        fullName = this.newspaper.fullName

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
        const actualCoEditors = this.newspaper.coEditors.map(editor => editor.id)
        const newCoEditors = this.coEditors.map(editor => editor.id)
        if (JSON.stringify(actualCoEditors) !== JSON.stringify(newCoEditors)) {
          fields.coEditors = newCoEditors
        }

        await this.updateNewspaper({
          fullName,
          fields
        });
      } else {
        const created = await this.startNewspaper({
          authorId: this.user.id,
          newspaper: {
            title: this.title,
            description: this.description,
            periodicity: this.periodicity,
            price: this.price,
            image: this.image,
            coEditors: this.coEditors.map(editor => editor.id),
          }
        });
        fullName = created.fullName
      }

      window.localStorage.setItem('manageNewspapers.selected', fullName)
      this.$router.push('/newspapers')
    },

    ...mapActions(["startNewspaper", "updateNewspaper"])
  }
};
</script>

<style lang="sass">
@import './styles/components/buttons'

//- EDIT NEWSPAPER -//
.newspaper-settings-view
  display: block
  padding: $baseline
  max-width: 900px
  margin: 0 auto

  //- Heading
  > h1
    margin-bottom: $baseline

    font-size: $fs-3
    font-weight: 600

  //- Sections heading
  h2
    margin-bottom: $baseline / 2
    font-size: $fs-2
    font-weight: 600

  //- Section template
  main
    display: grid
    grid-column-gap: $baseline
    grid-template-areas: "newspaper-settings-general newspaper-settings-side"
    grid-template-columns: auto auto
    grid-template-rows: auto

  .newspaper-settings--general
    grid-area: newspaper-settings-general

  .newspaper-settings--side
    grid-area: newspaper-settings-side


  section
    margin-bottom: $baseline

  //- form fields
  section > div
    display: table
    width: $baseline * 14
    margin-bottom: $baseline

    //- label
    label
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

    button
      +button(primary, small)

    > span
      cursor: pointer

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
      width: 100%
      height: 156px
      padding-bottom: $baseline

    button
      margin-top: $baseline / 4

  //- Footer
  footer
    button
      +button(primary, large)


//- Editors
.newspaper-settings--editors
  > h3
    font-weight: 600


//- Add editor form
.newspaper-settings--editors--add-editor
  display: flex

  input
    flex: 1
    border-radius: 5px 0 0 5px

  button
    +button

    border-radius: 0 5px 5px 0
    padding: 0 $baseline/2
</style>
