<template>
  <app-header>
    <div>
      <app-header--nav role="navigation">
        <ul>
          <li class="home"><router-link to="/">Home</router-link></li>
          <li class="new-post"><router-link to="/editor">New Post</router-link></li>
          <li class="your-editions"><router-link to="/editions">Your Editions</router-link></li>
          <li class="reading-list"><router-link to="/read-later">Reading List</router-link></li>
        </ul>
        </app-header--nav>

        <app-header--search>
          <input type="search" placeholder="Search"/>
        </app-header--search>

        <app-header--user-profile v-if="user" v-on:click="openDropDownMenu()">
          <img :src="user.picture" :alt="user.name"/>
        </app-header--user-profile>

        <app-header--user-profile-menu v-if="user && isDropDownMenuOpen" v-on:mouseleave="closeDropDownMenu()">
          <h3>{{ user.name }}</h3>
          <ul>
            <!--li><a href="">Profile</a></li>
            <li><a href="">Settings</a></li-->
            <li><a href="/accounts/logout/">Logout</a></li>
          </ul>
        </app-header--user-profile-menu>

        <app-header--user-profile v-if="!user">
          <a href="/accounts/login/">Login</a>
        </app-header--user-profile>
    </div>
  </app-header>
</template>

<script>
import request from 'superagent'

export default {
  name: 'AppHeaderComponent',
  data: function() {
    return {
      user: null,
      isDropDownMenuOpen: false
    }
  },
  methods: {
    openDropDownMenu: function () {
      this.isDropDownMenuOpen = true
      this.$forceUpdate()
    },

    closeDropDownMenu: function () {
      this.isDropDownMenuOpen = false;
      this.$forceUpdate();
    }
  },

  created: function () {
    request
      .get(process.env.BACKEND_BASE + '/api/profile')
      .then(res => {
        this.user = res.body.user
      })
  }
}
</script>
