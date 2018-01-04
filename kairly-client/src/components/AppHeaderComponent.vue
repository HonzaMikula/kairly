<template>
  <app-header>
    <div>
      <app-header--nav role="navigation">
        <ul>
          <li class="home"><router-link to="/">Home</router-link></li>
          <!--li class="new-post"><router-link to="/editor">New Post</router-link></li-->
          <li class="your-editions"><router-link to="/editions">Your Editions</router-link></li>
          <li class="reading-list"><router-link to="/read-later">Reading List</router-link></li>
        </ul>
        </app-header--nav>

        <app-header--search>
          <input type="search" placeholder="Search"/>
        </app-header--search>

        <app-header--user-profile v-if="user" v-on:click="openDropDownMenu">
          <img src="../assets/user.png" :alt="user.name"/>
        </app-header--user-profile>

        <app-header--user-profile-menu v-if="user && isDropDownMenuOpen" v-on:mouseleave="closeDropDownMenu">
          <h3>{{ user.name }}</h3>
          <ul>
            <!--li><a href="">Profile</a></li>
            <li><a href="">Settings</a></li-->
            <li><a href="/accounts/logout/">Logout</a></li>
          </ul>
        </app-header--user-profile-menu>

        <app-header--user-profile-login v-if="!user">
          <h3>Sign In to Kairly</h3>
          <form method="POST" v-on:submit="get_token">
            <input name="username" v-model="username" placeholder="Username" /><br>
            <input name="password" type="password" v-model="password" placeholder="Password" /><br>
            <button type="submit">Sign In</button>
          </form>

          <p>Do you want to try Kairly? <br> Write at <a href="mailto:jan.mikula@hotmail.com">jan.mikula@hotmail.com</a>.</p>

        </app-header--user-profile-login>
    </div>
  </app-header>
</template>

<script>
import request from 'superagent'
import store from '@/store'
import * as api from '@/api'

export default {
  name: 'AppHeaderComponent',
  data: function() {
    return {
      user: null,
      username: null,
      password: null,
      isDropDownMenuOpen: false
    }
  },
  methods: {
    get_token: function(ev) {
      ev.preventDefault()
      api
        .getToken(this.username, this.password)
        .then(() => {
          api.getProfile().then(user => { this.user = user })
        })
    },

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
    api.getProfile().then(user => { this.user = user })
  }
}
</script>
