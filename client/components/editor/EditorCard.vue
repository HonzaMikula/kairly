<template>
  <li>
    <picture>
      <AuthorPicture :author="editor" />
    </picture>

    <h3>{{ editor.name }}</h3>

    <p>{{ role }}</p>

    <button
      v-if="canDelete"
      @click="$emit('delete')"
      v-b-tooltip
      :title="$t('Remove co-editor')"
    ></button>
  </li>
</template>

<script>
import AuthorPicture from '@/components/widgets/AuthorPicture'

export default {
  name: "EditorCard",

  props: {
    editor: Object,
    role: String,
    canDelete: Boolean
  },

  components: {
    AuthorPicture
  },
};
</script>

<style lang="sass">
@import './styles/components/buttons'

//- Editors
.newspaper-settings--editors
  li
    display: grid
    grid-column-gap: $baseline / 2
    grid-template-areas: "nse-picture nse-name nse-remove" "nse-picture nse-role nse-remove"
    grid-template-columns: $baseline*2 auto min-content
    grid-template-rows: $baseline
    margin-bottom: $baseline / 2

    //- picture of the editor
    picture
      grid-area: nse-picture

      img
        border-radius: 100%
        height: 100%
        width: 100%

        object-fit: cover

    //- name of the editor
    h3
      grid-area: nse-name

      font-size: $fs-0
      font-weight: 600

    //- role
    p
      grid-area: nse-role

    //- remove co-editor button
    button
      grid-area: nse-remove
      place-self: center
      height: $baseline

      background: transparent
      border: 0
      color: #999

      cursor: pointer

      &:focus,
      &:hover
        color: #000

      &::after
        +fa-icon()
        @extend .fas
        content: fa-content($fa-var-times)

</style>
