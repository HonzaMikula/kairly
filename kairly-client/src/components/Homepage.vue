<template>
  <homepage-view>
    <homepage--cover>
      <h1>Kairly</h1>

      <p>We stand for exceptional journalism<br /> &amp; great reading experience.</p>
    </homepage--cover>

    <homepage--login>
      <div v-if="invalidCredentials" style="background: LightSalmon; text-align: center; width: 100%;">
        Invalid credentials
      </div>

      <form v-on:submit.prevent="login">
        <div>
          <label>Login</label>
          <input name="username" v-model="username" />
        </div>

        <div>
          <label>Password</label>
          <input name="password" type="password" v-model="password" />
        </div>

        <button type="submit">Sign In</button>
      </form>
    </homepage--login>

    <homepage--values>
      <h2>What we believe in?</h2>

      <p>
        In the world full of fake news, manipulations and attacks on journalism, we stand for <strong>truth</strong>.
      </p>

      <p>In the world full of censorship and propaganda, we stand for <strong>free speach</strong>.</p>

      <p>
        In the world full of distraction and lack of focus, we stand for
        <strong>control of your time and undistracted reading experience</strong>.
      </p>

      <p>
        In the world where journalist are dependent on advertisment or big corporations with their interests,
        we stand for <strong>fair reward for high-quality content</strong>.
      </p>

      <p>Stand with us!</p>
    </homepage--values>

    <homepage--how-it-works>
      <h2>How it works?</h2>
      <p>
        In old times we bought newspapers every day. Each issue of newspaper was prepared by professional editors who selected the
        best articles from proffesional authors. By buying a newspaper, you pay those editors and authors.
      </p>

      <p>
        In modern world of social media we lost professional editors and authors are dependent on advertisment.
        Now it's your friends who are selecting the content in your timeline. The result is not good.
        Exceptional journalism depends on professional editors and authors, who will get paid fairly.
      </p>

      <div>
        <img src="../assets/homepage/kairly-screenshot.png" alt="Kairly Screenshot"/>
        <img src="../assets/homepage/kairly-screenshot2.png" alt="Kairly Screenshot"/>
      </div>

      <p>
        In Kairly readers are subsribing editions and paying for them.
        Those money are then shared between editors and authors.
      </p>
    </homepage--how-it-works>

    <homepage--help-us>
      <h2>How you can help?</h2>
      <p>You can help us create exceptional journalism in different ways.</p>

      <div>
        <section>
          <h3>Readers</h3>
          <p>
            Do you like the project and you want to help us improve the experience for readers?
            Participate in our user tests and private beta program.
          </p>
        </section>

        <section>
          <h3>Editors</h3>
          <p>
            Do you want to change how current journalism and its business models work?
            Start creating editions in our private beta program.
          </p>
        </section>

        <section>
          <h3>Authors</h3>
          <p>
            Do you want to help improve our payments mechanism for authors?
            Start publishing your blogs and tweets in our private beta program.
          </p>
        </section>

        <section>
          <h3>Investors</h3>
          <p>
            Do you want to help us create enviroonment for exceptional journalism?
            Become one of our investors.
          </p>
        </section>
      </div>

      <homepage--help-us--contact-us>
        <a href="mailto:jan.mikula@hotmail.com">Contact Us</a>
      </homepage--help-us--contact-us>
    </homepage--help-us>

  </homepage-view>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

import * as api from '@/api'

export default {
  name: 'Homepage',
  data: function() {
    return {
      invalidCredentials: false,
      username: null,
      password: null
    }
  },
  methods: {
    login() {
      this.invalidCredentials = false
      const { username, password } = this
      api.createToken(username, password)
      .then(this.getProfile)
      .catch(err => this.invalidCredentials = true)
    },

    ...mapActions(['getProfile']),
  }
}
</script>
