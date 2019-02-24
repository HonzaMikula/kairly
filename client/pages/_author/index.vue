<template>
  <app-layout :name="$t('Author\'s profile')">
    <author-detail-view
      v-infinite-scroll="loadPosts"
      infinite-scroll-disabled="loadingPosts"
      infinite-scroll-distance="100"
      itemtype="https://schema.org/Person"
      itemscope
    >
      <author-detail--header>
        <picture>
          <img v-if="author.picture" itemprop="image" :src="author.picture" :alt="author.name">
          <img v-else src="~assets/user.png" :alt="author.name">
        </picture>

        <section>
          <h1 itemprop="name">{{ author.name }}</h1>
          <p itemprop="description">{{ author.bio }}</p>
        </section>

        <author-detail--subscribe v-if="loggedIn">
          <AuthorSubscription if="subscription" :author="author" :subscription="subscription"/>
        </author-detail--subscribe>
      </author-detail--header>

      <author-detail--newspapers v-if="newspapers.length">
        <h2>{{ author.name }}'s newspapers</h2>

        <div :class="{'show-all': showAllNewspapers}">
          <NewspaperWidget
            v-for="newspaper in visibleNewspapers"
            :key="newspaper.fullName"
            v-bind:newspaper="newspaper"
          />
        </div>

        <button
          v-if="newspapers.length > 3"
          @click="toggleNewspapers()"
        >{{ !showAllNewspapers ? this.$t('Show all newspapers') : this.$t('Hide newspapers') }}</button>
      </author-detail--newspapers>

      <author-detail--posts v-if="posts.length">
        <h2>{{ author.name }}'s Posts</h2>

        <PostWrapper v-for="post in posts" :post="post" :isSubscribed="true" :key="post.id"/>
      </author-detail--posts>

      <div class="author-detail--empty" v-if="!newspapers.length && !posts.length && !loadingPosts">
        <template v-if="test.user.id !== author.id">
          <p>{{ $t("User didn't write any posts and didn't start any newspaper.") }}</p>
        </template>

        <template v-else>
          <p>{{ $t("You didn't write any post and didn't start any newspaper.") }}</p>

          <nuxt-link :to="{name: 'newspapers'}">{{ $t('Start a newspaper') }}</nuxt-link>
        </template>
      </div>

      <loading-spinner v-if="loadingPosts"></loading-spinner>
    </author-detail-view>
  </app-layout>
</template>


<script>
import { mapMutations, mapState } from "vuex"
import { errorToParams } from "@/utils/errors"

import AppLayout from "@/components/layout/AppLayout"
import NewspaperWidget from "@/components/widgets/NewspaperWidget"
import PostWrapper from "@/components/PostWrapper"
import AuthorSubscription from "@/components/widgets/AuthorSubscription"

export default {
  name: "AuthorDetail",
  auth: false,

  head() {
    const { id, name, bio, picture } = this.author;
    return {
      title: `${name} – Kairly`,
      meta: [
        { hid: "description", name: "description", content: bio },
        { hid: `og:title`, property: "og:title", content: `${name} – Kairly` },
        { hid: `og:description`, property: "og:description", content: bio },
        { hid: `og:image`, property: "og:image", content: picture },
        { hid: `og:image:alt`, property: "og:image:alt", content: name },
        { hid: `og:type`, property: "og:type", content: "profile" },
        {
          hid: `og:url`,
          property: "og:url",
          content: `https://www.kairly.com/${id}`
        },
        { hid: `twitter:card`, property: "twitter:card", content: "summary" },
        {
          hid: `twitter:site`,
          property: "twitter:site",
          content: "@kairlyapp"
        },
        {
          hid: `twitter:title`,
          property: "twitter:title",
          content: `${name} – Kairly`
        },
        {
          hid: `twitter:description`,
          property: "twitter:description",
          content: bio
        },
        { hid: `twitter:image`, property: "twitter:image", content: picture }
      ]
    };
  },

  components: {
    AppLayout,
    NewspaperWidget,
    PostWrapper,
    AuthorSubscription
  },

  data() {
    return {
      showAllNewspapers: false
    };
  },

  computed: {
    ...mapState({
      loggedIn: state => state.auth.loggedIn,
      test: state => state.auth
    }),

    visibleNewspapers() {
      const mq = window.matchMedia("(max-width: 640px)")
      if (mq.matches) {
        return this.newspapers
      }
      else {
        return this.showAllNewspapers
          ? this.newspapers
          : this.newspapers.slice(0, 3);
      }
    },

    subscription() {
      return this.$store.getters.getAuthorSubscription(this.author);
    }
  },

  methods: {
    unsubscribe() {
      this.$store.dispatch("unsubscribeAuthor", {
        author: this.author
      });
      document.activeElement.blur();
    },

    renewSubscription() {
      this.$store.dispatch("subscribeAuthor", {
        author: this.author
      });
      document.activeElement.blur();
    },

    toggleNewspapers() {
      this.showAllNewspapers = !this.showAllNewspapers;
    },

    async loadPosts() {
      if (this.cursor === null) {
        return;
      }
      const { author: authorId } = this.$route.params;

      this.loadingPosts = true;

      const { posts, cursor } = await this.$axios.$get(
        `/authors/${authorId}/posts`,
        { params: { cursor: this.cursor } }
      );

      posts.forEach(post => this.posts.push(post));
      this.cursor = cursor;
      this.loadingPosts = false;
    }
  },

  async asyncData({ app, store, params: { author: authorId }, error }) {
    if (store.state.auth.loggedIn) {
      await store.dispatch("getSubscriptions");
    }

    try {
      const { author, newspapers } = await store.dispatch(
        "getAuthor",
        authorId
      );

      const data = {
        author,
        newspapers
      };

      if (process.server) {
        const { posts, cursor } = await app.$axios.$get(
          `/authors/${authorId}/posts`,
          { params: { cursor: 0 } }
        );
        data.posts = posts;
        data.cursor = cursor;
        data.loadingPosts = false;
      } else {
        // load all in created function to make transition faster
        data.posts = [];
        data.cursor = 0;
        data.loadingPosts = true;
      }

      return data;
    } catch (err) {
      error(errorToParams(err));
    }
  },

  created() {
    if (process.client && this.cursor === 0) {
      this.loadPosts();
    }
  }
};
</script>

<style lang="sass">
//- Imports
@import './styles/components/buttons'


//- AUTHOR DETAIL -//

author-detail-view
  display: block
  padding-top: $baseline
  margin: 0 auto
  max-width: 900px

  @media (max-width: $mobile)
    padding-top: 0


//- Header
author-detail--header
  position: sticky
  top: 0
  z-index: 1

  display: grid
  grid-template-columns: $baseline*4 1fr auto
  grid-column-gap: $baseline
  padding: $baseline/4 $baseline $baseline/4 $baseline
  margin: (-$baseline/4) (-$baseline) $baseline/2 (-$baseline)

  backdrop-filter: blur(10px) saturate(125%)

  font-family: $ff-serif

  @supports not (backdrop-filter: blur(10px))
    background: rgba(250, 250, 250, 0.97)

  @media (max-width: $mobile)
    position: static
    grid-template-columns: $baseline*4 1fr
    grid-template-rows: auto auto
    grid-row-gap: $baseline / 2
    padding: $baseline / 4
    margin: 0

  //- Author name
  h1
    font-size: $fs-3
    font-weight: 600
    line-height: $baseline * 2
    text-shadow: 0 0 5px #fafafa

  //- Bio
  p
    text-shadow: 0 0 5px #fafafa

  picture img
    display: block
    border-radius: 100%
    height: $baseline * 4
    width: $baseline * 4

    object-fit: cover


//- Subsribe
author-detail--subscribe
  position: relative

  display: block
  margin-bottom: $baseline

  color: #555

  font-family: $ff-sans
  line-height: 1.42
  text-align: center

  @media (max-width: $mobile)
    grid-column: 1 / span 2
    margin-bottom: 0

  .author-subscription-view
    //- when author is subscribed
    button.is-subscribed
      +button(primary, medium)

    //- when author is ready to be subsribed
    //- when author is canceled or suspended
    button.to-subscribe,
    button.is-canceled
      +button(secondary, medium)

    //- when author is suspended
    button.is-suspended
      +button(secondary, medium)
      background: lighten($c-base, 10%)
      background: repeating-linear-gradient(135deg, lighten($c-base, 5%) 0px, lighten($c-base, 5%) 2px, lighten($c-base, 15%) 2px, lighten($c-base, 15%) 5px)
      color: #fff

//- Newspapers
author-detail--newspapers
  display: block
  margin-bottom: $baseline

  @media (max-width: $mobile)
    padding: $baseline / 4

  > h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600

  img
    max-width: 100%

  //- wrapper for newspaper items
  > div
    display: grid
    grid-row-gap: $baseline
    grid-template-columns: 1fr 1fr 1fr
    grid-column-gap: $baseline / 2
    grid-row-gap: $baseline / 2
    margin-bottom: $baseline / 2

    @media (max-width: $mobile)
      display: flex
      grid-column-gap: $baseline / 4
      overflow-x: auto
      -webkit-overflow-scrolling: touch

      newspaper-widget-view
        margin-right: $baseline / 2
        max-width: 200px

  //- show/hide more newspapers
  > button
    +button

    display: table
    margin: 0 auto

    @media (max-width: $mobile)
      display: none

//- Posts
author-detail--posts
  display: block
  margin-bottom: $baseline

  > h2
    margin-bottom: $baseline / 2

    font-family: $ff-serif
    font-size: $fs-1
    font-weight: 600

    @media (max-width: $mobile)
      padding: 0 $baseline/4

//- Empty
.author-detail--empty
  padding: $baseline
  margin-top: $baseline * 2

  background: #eee
  border: 1px dashed #ccc

  text-align: center

  a
    +button(primary, large)

</style>
