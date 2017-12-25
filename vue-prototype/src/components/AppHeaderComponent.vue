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

        <app-header--user-profile v-on:click="openDropDownMenu()">
          <img src="https://pbs.twimg.com/profile_images/522497269447147520/uGF7lbPY.jpeg" alt="Jan Mikula"/>
        </app-header--user-profile>

        <app-header--user-profile-menu v-if="isDropDownMenuOpen" v-on:mouseleave="closeDropDownMenu()">
          <h3>Jan Mikula</h3>
          <ul>
            <li><a href="">Profile</a></li>
            <li><a href="">Settings</a></li>
            <li><a href="">Logout</a></li>
          </ul>
        </app-header--user-profile-menu>
    </div>
  </app-header>
</template>

<script>

export default {
  name: 'AppHeaderComponent',
  data: function() {
    return {
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
}
</script>