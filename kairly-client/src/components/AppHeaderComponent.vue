<template>
  <app-header>
    <div>
      <app-header--nav role="navigation">
        <ul v-if="user">
          <li class="home"><router-link to="/">Home</router-link></li>
          <li class="your-editions"><router-link to="/my-editions">My Subscription</router-link></li>
          <!-- li class="new-post"><router-link to="/editor">New Post</router-link></li -->
          <!-- li class="your-editions"><router-link to="/editions">Create Edition</router-link></li>
          <li class="reading-list"><router-link to="/read-later">Reading List</router-link></li -->
        </ul>
        </app-header--nav>

        <!--app-header--search>
          <input type="search" placeholder="Search"/>
        </app-header--search-->

        <app-header--user-profile v-if="user" v-on:click="openDropDownMenu">
          <img src="../assets/user.png" :alt="user.name"/>
          <!--
            Gravatar url handles default itself (it can generate 404 url or some dafault),
            but it is problematic handle it on client side identify default and replace it with own default
          -->
          <!--img :src="user.picture" :alt="user.name"/-->
        </app-header--user-profile>

        <app-header--user-profile-menu v-if="user && isDropDownMenuOpen" v-on:mouseleave="closeDropDownMenu">
          <h3>{{ user.name }}</h3>
          <ul>
            <!--li><a href="">Profile</a></li>
            <li><a href="">Settings</a></li-->
            <li><a href="" v-on:click.prevent="logout">Logout</a></li>
          </ul>
        </app-header--user-profile-menu>
    </div>
  </app-header>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import store from '@/store'

export default {
  name: 'AppHeaderComponent',
  data: function() {
    return {
      username: null,
      password: null,
      isDropDownMenuOpen: false
    }
  },
  computed: {
    ...mapState({
      user: state => state.user
    }),
    ...mapGetters(['loadingUser'])
  },
  methods: {
    ...mapActions(['login', 'logout']),

    openDropDownMenu: function () {
      this.isDropDownMenuOpen = true
      this.$forceUpdate()
    },

    closeDropDownMenu: function () {
      this.isDropDownMenuOpen = false;
      this.$forceUpdate();
    }
  }
}
</script>
