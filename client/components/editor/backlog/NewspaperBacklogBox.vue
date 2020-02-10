<template>
  <compotent
    :is="Array.isArray(post) ? 'BoxWrapper' : 'PostWrapper'"
    :post="post"
    :isSubscribed="true"
    @click.native="toggleMobileControls"
  >
    <template #controls>
      <span v-if="post.type !== 'comment'" class="price">{{ post.price }} Kč</span>
    </template>

    <template #aside>
       <div
        :class="{'newspaper-backlog-controls': true, 'hide-mobile-controls': mobileControls}"
      >
        <div class="newspaper-backlog-controls--arrows">
          <button
            class="up"
            :id="`backlog-controls-up-${post.id}`"
            @click.stop="moveUp(post.id)"
            :disabled="!canMoveUp"
          ></button>

          <button
            class="down"
            :id="`backlog-controls-down-${post.id}`"
            @click.stop="moveDown(post.id)"
            :disabled="!canMoveDown"
          ></button>

          <button
            class="remove"
            @click.stop="removePost(post.id)"
            v-b-tooltip
            title="Remove post"
          ></button>

          <b-popover
            v-if="source !== 'upcoming'"
            :target="`backlog-controls-up-${post.id}`"
            placement="leftbottom"
            :delay="{ show: 400, hide: 100 }"
            triggers="hover"
            @click.stop
          >
            <ul>
              <li
                v-if="source !== 'upcoming'"
                tabindex="0"
                @click="moveUp(post.id, 'upcoming')"
              >
                <h6>{{ $t('Move to upcoming issue') }}</h6>
                <p></p>
              </li>
              <li
                v-if="source === 'considered'"
                @click="moveUp(post.id, 'next')"
              >
                <h6>{{ $t('Move to next issue') }}</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>

          <b-popover
            v-if="source !== 'considered'"
            :target="`backlog-controls-down-${post.id}`"
            placement="leftbottom"
            :delay="{ show: 400, hide: 100 }"
            triggers="hover"
            @click.stop
          >
            <ul>
              <li
                v-if="source === 'upcoming'"
                tabindex="0"
                @click="moveDown(post.id, 'next')"
              >
                <h6>{{ $t('Move to next issue') }}</h6>
                <p></p>
              </li>
              <li
                v-if="source !== 'considered'"
                @click="moveDown(post.id, 'considered')"
              >
                <h6>{{ $t('Move to backlog issue') }}</h6>
                <p></p>
              </li>
            </ul>
          </b-popover>
        </div>

        <!--div
          v-if="post.type != 'tweet' || isAdmin"
          class="newspaper-backlog-controls--options">
          <button
            v-if="!log.editorial && !editorType"
            class="add-editorial"
            @click="showCrossroad('right')"
          ></button>

          <template v-else>
            <button
              class="change-position"
              @click="changeEditorialPosition"
              v-b-tooltip
              :title="$t('Change position')"
            ></button>

            <button
              class="menu"
              :id="`backlog-controls-option-${post.id}`"
              @click.stop
              v-b-tooltip
              :title="$t('Editorial menu')"
            ></button>

            <b-popover
              :target="`backlog-controls-option-${post.id}`"
              placement="bottomleft"
              triggers="click blur"
              @click.stop
            >
              <ul>
                <li
                  v-show="!editorType"
                  tabindex="0"
                  @click="editEditorial"
                >
                  <h6>{{ $t('Update editorial comment') }}</h6>
                  <p>{{ $t('Write short comment to the topic') }}</p>
                </li>
                <li
                  v-show="!editorType"
                  tabindex="0"
                  @click="removeEditorial"
                >
                  <h6>{{ $t('Remove editorial') }}</h6>
                  <p>{{ $t('Remove existing editorial') }}</p>
                </li>
                <li
                  v-show="editorType"
                  tabindex="0"
                  @click="cancelEditorialEdit"
                >
                  <h6>{{ $t('Cancel edit') }}</h6>
                  <p>{{ $t('Your changes will be lost') }}</p>
                </li>
              </ul>
            </b-popover>
          </template>

          <button
            v-if="post.type == 'comment'"
            class="edit-comment"
            @click="editComment"
          ></button>

        </div-->
      </div>
    </template>
  </compotent>
</template>

<script>
import PostWrapper from '@/components/PostWrapper'
import BoxWrapper from '@/components/BoxWrapper'

export default {
  name: 'NewspaperBacklogBox',

  components: {
    PostWrapper,
    BoxWrapper
  },

  props: {
    newspaper: Object,
    post: [Object, Array],
    canMoveUp: Boolean,
    canMoveDown: Boolean,
    source: String,
  },

  data() {
    return {
      mobileControls: false
    }
  },

  computed: {
    isAdmin() {
      const { user } = this.$store.state.auth
      return user.isAdmin
    }
  },

  methods: {
    toggleMobileControls() {
      this.mobileControls = !this.mobileControls
    }
  }
}
</script>

<style lang="sass">
@import './styles/components/buttons'
@import './styles/components/mixins'

//- Backlog controls
.newspaper-backlog-controls.hide-mobile-controls
  @media (max-width: $mobile)
    display: none

.newspaper-backlog-controls--arrows
  position: absolute
  left: (-$baseline * 1.5)
  top: 0

  display: grid
  grid-template-row: auto auto
  grid-row-gap: $baseline / 4

  @media (max-width: $mobile)
    left: $baseline/4
    top: 40%

  //- button up
  .up
    +button-icon($fa-var-arrow-up)

  //- button down
  .down
    +button-icon($fa-var-arrow-down)

  //- button down
  .remove
    +button-icon($fa-var-times)

.newspaper-backlog-controls--options
  position: absolute
  right: (-$baseline * 1.5)
  top: 0

  display: grid
  grid-template-row: auto auto
  grid-row-gap: $baseline / 4

  @media (max-width: $mobile)
    right: $baseline/4
    top: 40%

  //- button add editorial
  .add-editorial
    +button-icon($fa-var-font)

  //- button add comment
  .edit-comment
    +button-icon($fa-var-pencil-alt)

  //- button menu
  .menu
    +button-icon($fa-var-ellipsis-v)

  //- change position button
  .change-position
    +button-icon($fa-var-exchange-alt)


.sortable-drag
  .newspaper-backlog-controls
    display: none

</style>
